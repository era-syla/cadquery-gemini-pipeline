import cadquery as cq

# Parameters defining the geometry
base_diameter = 24.0
base_thickness = 2.0

neck_diameter = 8.0
neck_length = 12.0

body_diameter = 24.0
body_length = 18.0
body_chamfer = 1.5
body_fillet = 0.8

boss_diameter = 6.0
boss_height = 2.0

wire_diameter = 1.5
loop_width_half = 9.0
loop_height = 12.0
loop_leg_spacing_half = 1.5

# 1. Create the main turned parts (Base, Neck, Body, Boss)
# Start with the Base Plate
result = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# Add the Neck
result = result.faces(">Z").workplane().circle(neck_diameter / 2).extrude(neck_length)

# Add the Main Body
result = result.faces(">Z").workplane().circle(body_diameter / 2).extrude(body_length)

# Add the small Boss on top
result = result.faces(">Z").workplane().circle(boss_diameter / 2).extrude(boss_height)

# 2. Apply Details (Chamfers and Fillets)
# Calculate Z-heights for edge selection
z_neck_start = base_thickness
z_body_start = base_thickness + neck_length
z_body_end = z_body_start + body_length

# Chamfer the bottom edge of the Main Body (where it meets the neck)
# We select the edge based on its approximate position
result = result.edges(
    cq.selectors.NearestToPointSelector((body_diameter / 2, 0, z_body_start))
).chamfer(body_chamfer)

# Fillet the top edge of the Main Body
result = result.edges(
    cq.selectors.NearestToPointSelector((body_diameter / 2, 0, z_body_end))
).fillet(body_fillet)

# 3. Create the Wire Loop
# Calculate starting Z height for the loop (top of the boss)
z_loop_start = z_body_end + boss_height

# Define the path for the loop on the XZ plane
# The path starts at the top of the boss, goes up, curves out, and returns
path = (
    cq.Workplane("XZ")
    .moveTo(loop_leg_spacing_half, z_loop_start)
    .lineTo(loop_leg_spacing_half, z_loop_start + 2.5)
    .spline([
        (loop_width_half, z_loop_start + 6.0),
        (0, z_loop_start + loop_height),
        (-loop_width_half, z_loop_start + 6.0),
        (-loop_leg_spacing_half, z_loop_start + 2.5)
    ])
    .lineTo(-loop_leg_spacing_half, z_loop_start)
)

# Create the wire loop by sweeping a circle along the path
loop = (
    cq.Workplane("XY")
    .center(loop_leg_spacing_half, 0)
    .circle(wire_diameter / 2)
    .extrude(1)
    .val()
)

# Use sweep with a wire circle
loop = (
    cq.Workplane("YZ")
    .workplane(offset=loop_leg_spacing_half)
    .center(0, z_loop_start)
    .circle(wire_diameter / 2)
    .sweep(path.val(), isFrenet=True)
)

# Union the loop with the main body
result = result.union(loop)