import cadquery as cq
import math

# --- Parameters ---
# Dimensions estimated from the image
disk_diameter = 90.0
disk_thickness = 2.0
hub_diameter = 30.0
hub_height = 18.0       # Total height from bottom
fillet_radius = 8.0     # Smooth transition radius
square_hole_size = 8.0  # Size of the central square hole

# Slot parameters
num_slots = 60
slot_outer_radius = 42.0  # Leaves a ~3mm rim
slot_inner_radius = 24.0  # Starts after the fillet
slot_angle = 3.0          # Degrees (approx 50% duty cycle for 60 slots)

# --- Geometry Generation ---

# 1. Base Structure: Disk + Hub
# Create the base disk
plate = cq.Workplane("XY").circle(disk_diameter / 2.0).extrude(disk_thickness)

# Create the hub cylinder on top of the disk
hub = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness)
    .circle(hub_diameter / 2.0)
    .extrude(hub_height - disk_thickness)
)

# Combine them into one body
result = plate.union(hub)

# 2. Fillet
# Create the smooth transition between the hub and the disk.
# We select the circular edge at the base of the hub.
result = result.faces(">Z[1]").edges().fillet(fillet_radius)

# 3. Center Hole
# Cut a square hole through the entire hub and disk
result = (
    result.faces(">Z")
    .workplane()
    .rect(square_hole_size, square_hole_size)
    .cutThruAll()
)

# 4. Radial Slots
# Define the shape of a single slot (sector)
def create_slot_solid():
    half_angle_rad = math.radians(slot_angle / 2.0)
    
    # Calculate vertices for the sector shape
    # P1: Inner Start, P2: Outer Start, P3: Outer End, P4: Inner End
    x_in = slot_inner_radius
    x_out = slot_outer_radius
    
    p_inner_start = (x_in * math.cos(-half_angle_rad), x_in * math.sin(-half_angle_rad))
    p_outer_start = (x_out * math.cos(-half_angle_rad), x_out * math.sin(-half_angle_rad))
    p_outer_mid   = (x_out, 0) # Midpoint for arc
    p_outer_end   = (x_out * math.cos(half_angle_rad), x_out * math.sin(half_angle_rad))
    p_inner_end   = (x_in * math.cos(half_angle_rad), x_in * math.sin(half_angle_rad))
    p_inner_mid   = (x_in, 0) # Midpoint for arc

    # Construct the wire and extrude
    slot = (
        cq.Workplane("XY")
        .moveTo(*p_inner_start)
        .lineTo(*p_outer_start)
        .threePointArc(p_outer_mid, p_outer_end) # Outer rim arc
        .lineTo(*p_inner_end)
        .threePointArc(p_inner_mid, p_inner_start) # Inner rim arc
        .close()
        .extrude(disk_thickness)
    )
    return slot

# Cut all slots using a loop
for i in range(num_slots):
    angle = i * 360.0 / num_slots
    slot_tool = create_slot_solid().rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(slot_tool)