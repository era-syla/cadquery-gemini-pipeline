import cadquery as cq

# Parameters derived from visual analysis
width = 50.0
depth = 50.0
height = 50.0
front_section_length = depth / 2.0  # Split roughly in half
front_section_height = 25.0         # Front section is lower
u_cut_radius = 15.0                 # Radius of the cylindrical cutout
chamfer_size = 8.0                  # Size of the corner chamfers
v_cut_depth = 8.0                   # Depth of the V-groove on the front
v_cut_top_width = 30.0              # Width of the V-groove at the top
v_cut_bottom_width = 12.0           # Width of the V-groove at the bottom

# 1. Create the base block
# We center X and Y for symmetry, keep Z=0 at the bottom
result = cq.Workplane("XY").box(width, depth, height, centered=(True, True, False))

# 2. Create the U-shaped cylindrical cutout
# This runs along the Y-axis on the top face.
# We cut through the entire block first; the front part will be modified later.
result = result.cut(
    cq.Workplane("XZ", origin=(0, 0, height))
    .circle(u_cut_radius)
    .extrude(depth * 1.5, both=True)  # Ensure it cuts through entirely
)

# 3. Create the Front Step
# Remove the top material from the front half of the block (Y < 0)
# This creates the lower platform for the front features
cut_box_height = height - front_section_height
result = result.cut(
    cq.Workplane("XY", origin=(0, -depth / 4.0, front_section_height))
    .box(width, front_section_length, cut_box_height, centered=(True, True, False))
)

# 4. Chamfer the front vertical corners
# Select vertical edges (|Z) that are on the frontmost face (<Y)
result = result.edges("|Z and <Y").chamfer(chamfer_size)

# 5. Create the V-Groove on the front section
# We define a trapezoidal profile on the front face and extrude-cut it backwards
# Origin is at the top-center of the front face
p1 = (-v_cut_top_width / 2.0, 0)
p2 = (-v_cut_bottom_width / 2.0, -v_cut_depth)
p3 = (v_cut_bottom_width / 2.0, -v_cut_depth)
p4 = (v_cut_top_width / 2.0, 0)

result = result.cut(
    cq.Workplane("XZ", origin=(0, -depth / 2.0, front_section_height))
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(front_section_length) # Extrude along +Y towards the back section
)