import cadquery as cq
import math

# --- Parameters ---
tire_od = 50.0          # Outer diameter of the tire
tire_width = 25.0       # Width of the tire
rim_recess_dia = 40.0   # Diameter of the inner rim cavity
rim_depth_front = 6.0   # Depth of the rim face from the front
web_thickness = 4.0     # Thickness of the spoke web
hub_dia = 12.0          # Diameter of the central hub
hub_height = 8.0        # Height of the hub (relative to web bottom)
axle_hole_dia = 4.0     # Central axle hole diameter
num_spokes = 6          # Number of spokes
spoke_gap_angle = 42.0  # Angle of the cutout (determines spoke thinness)

# Derived dimensions
web_z_bottom = tire_width - rim_depth_front - web_thickness
web_z_top = tire_width - rim_depth_front

# --- 1. Main Body Construction ---
# Create the base cylinder (Tire)
result = cq.Workplane("XY").circle(tire_od / 2.0).extrude(tire_width)

# Cut the front recess for the rim
result = result.faces(">Z").workplane() \
    .circle(rim_recess_dia / 2.0).cutBlind(-rim_depth_front)

# Cut the back recess (hollow out the back of the wheel)
# Leaves the 'web' between web_z_bottom and web_z_top
back_cut_depth = web_z_bottom
result = result.faces("<Z").workplane() \
    .circle(rim_recess_dia / 2.0).cutBlind(back_cut_depth)

# --- 2. Central Hub ---
# Create the hub cylinder centered on the web
# It starts at the bottom of the web and protrudes slightly past the web face
hub = cq.Workplane("XY").workplane(offset=web_z_bottom) \
    .circle(hub_dia / 2.0).extrude(hub_height)

# Round off the top of the hub (Dome shape)
hub = hub.faces(">Z").edges().fillet(2.0)

# Union the hub to the main body
result = result.union(hub)

# --- 3. Spoke Cutouts ---
# We define a single cutout shape (a sector with rounded corners) 
# and pattern it to create the spokes.

r_inner = (hub_dia / 2.0) + 1.5  # Offset from hub
r_outer = (rim_recess_dia / 2.0) - 1.5 # Offset from rim wall
angle_rad = math.radians(spoke_gap_angle / 2.0)

# Calculate points for the cutout profile (centered on X-axis)
p_in_start  = (r_inner * math.cos(-angle_rad), r_inner * math.sin(-angle_rad))
p_out_start = (r_outer * math.cos(-angle_rad), r_outer * math.sin(-angle_rad))
p_out_end   = (r_outer * math.cos(angle_rad), r_outer * math.sin(angle_rad))
p_in_end    = (r_inner * math.cos(angle_rad), r_inner * math.sin(angle_rad))

# Intermediate points for arcs
p_out_mid = (r_outer, 0)
p_in_mid  = (r_inner, 0)

# Create the 2D wire for the cutout
cutter_profile = cq.Workplane("XY") \
    .moveTo(*p_in_start) \
    .lineTo(*p_out_start) \
    .threePointArc(p_out_mid, p_out_end) \
    .lineTo(*p_in_end) \
    .threePointArc(p_in_mid, p_in_start) \
    .close()

# Extrude the profile to create a solid cutting tool
# Make it tall enough to cut through the web
cutter_solid = cutter_profile.extrude(10.0)

# Create spoke cutouts by rotating and cutting
for i in range(num_spokes):
    angle = i * (360.0 / num_spokes)
    rotated_cutter = cutter_solid.val().rotate(cq.Vector(0,0,0), cq.Vector(0,0,1), angle).translate(cq.Vector(0, 0, web_z_bottom - 1.0))
    result = result.cut(rotated_cutter)

# --- 4. Final Details ---
# Cut the axle hole through everything
result = result.faces(">Z").workplane().circle(axle_hole_dia / 2.0).cutThruAll()

# Optional: Chamfer the outer tire edges for realism
result = result.edges(">Z or <Z").chamfer(1.0)