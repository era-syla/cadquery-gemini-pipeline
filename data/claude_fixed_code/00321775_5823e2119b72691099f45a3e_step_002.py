import cadquery as cq
import math

# --- Parameters ---
# Bracket Dimensions
bracket_width = 30.0    # Depth
bracket_thick = 2.5
hump_width = 30.0       # Inner width
hump_height = 20.0      # Inner height
flange_length = 15.0
slot_length = 10.0
slot_width = 4.0

# Top Clamp Dimensions
hub_diameter = 22.0
hub_height = 8.0
arm_length = 32.0       # Length from center axis
arm_width = 22.0
hex_socket_size = 6.0   # Flat-to-flat

# Hardware Dimensions
bolt_diameter = 8.0
spring_height = 10.0
spring_wire_dia = 1.0
spring_pitch = 2.0

# --- Geometry Construction ---

# 1. Base Bracket
# Define the path for the bent sheet metal profile (XZ plane)
# Origin at the bottom center of the hump
half_hump = hump_width / 2.0
total_ext = half_hump + flange_length

# Points for the inner bottom line
pts = [
    (-total_ext, 0),
    (-half_hump, 0),
    (-half_hump, hump_height),
    (half_hump, hump_height),
    (half_hump, 0),
    (total_ext, 0)
]

# Create profile, thicken, and extrude
bracket = (
    cq.Workplane("XZ")
    .polyline(pts)
    .offset2D(bracket_thick)
    .extrude(bracket_width)
)

# Center the bracket along Y-axis
bracket = bracket.translate((0, -bracket_width/2.0, 0))

# Cut slots in the flanges
slot_center_x = half_hump + flange_length/2.0

# Create cutting tool for slots
slot_cutter = (
    cq.Workplane("XY")
    .workplane(offset=bracket_thick)
    .pushPoints([(-slot_center_x, 0), (slot_center_x, 0)])
    .slot2D(slot_length, slot_width)
    .extrude(-20)
)

# Cut center hole for bolt
center_hole_cutter = (
    cq.Workplane("XY")
    .workplane(offset=hump_height + bracket_thick)
    .circle(bolt_diameter/2.0 + 0.5)
    .extrude(-hump_height - 20)
)

bracket = bracket.cut(slot_cutter).cut(center_hole_cutter)


# 2. Top Clamp Piece
# Position: Above the bracket with space for the spring
top_z_start = hump_height + bracket_thick + spring_height

# Create the Hub and Arm shapes
# Hub
hub = (
    cq.Workplane("XY")
    .workplane(offset=top_z_start)
    .circle(hub_diameter/2.0)
    .extrude(hub_height)
)

# Arm (extending to -X)
arm = (
    cq.Workplane("XY")
    .workplane(offset=top_z_start)
    .center(-arm_length/2.0, 0)
    .rect(arm_length, arm_width)
    .extrude(hub_height)
)

# Union to form basic shape
clamp = hub.union(arm)

# Cut Hex Socket in Hub
hex_radius = hex_socket_size / math.cos(math.radians(30))
clamp = (
    clamp.faces(">Z")
    .workplane()
    .polygon(6, hex_radius)
    .cutBlind(-3.0)
)

# Cut Serrations on Arm
serration_pitch = 1.5
serration_depth = 1.0
start_x = -hub_diameter/2.0 - 1.0
end_x = -arm_length + 1.0
num_serrations = int(abs(end_x - start_x) / serration_pitch)

# Create serrations
for i in range(num_serrations):
    pos_x = start_x - i * serration_pitch
    z_pos = top_z_start + hub_height
    
    # Triangle cutter profile
    tooth = (
        cq.Workplane("XZ")
        .workplane(offset=-bracket_width/2.0)
        .moveTo(pos_x, z_pos)
        .lineTo(pos_x + serration_pitch/2.0, z_pos - serration_depth)
        .lineTo(pos_x + serration_pitch, z_pos)
        .close()
        .extrude(bracket_width)
    )
    clamp = clamp.cut(tooth)


# 3. Bolt
bolt = (
    cq.Workplane("XY")
    .workplane(offset=top_z_start + hub_height)
    .circle(bolt_diameter/2.0)
    .extrude(-(hub_height + spring_height + hump_height + 10))
)


# 4. Spring
spring_base_z = hump_height + bracket_thick
spring_radius = bolt_diameter/2.0 + 1.0

# Generate Helix Wire
helix_wire = cq.Wire.makeHelix(
    pitch=spring_pitch, 
    height=spring_height, 
    radius=spring_radius, 
    center=cq.Vector(0, 0, spring_base_z)
)

# Create profile and sweep
spring = (
    cq.Workplane("XZ", origin=(spring_radius, 0, spring_base_z))
    .circle(spring_wire_dia/2.0)
    .sweep(helix_wire, isFrenet=True)
)

# Combine all parts into result
result = bracket.union(clamp).union(bolt).union(spring)