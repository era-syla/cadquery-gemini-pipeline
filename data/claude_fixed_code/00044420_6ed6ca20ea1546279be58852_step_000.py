import cadquery as cq

# Dimensions estimated from the image
height = 80.0
width = 50.0
thickness = 15.0
chamfer_size = 3.0
side_cut_height = 45.0
side_cut_depth = 3.0
top_hole_spacing = 28.0
front_hole_spacing = 40.0
top_hole_dia = 5.0
top_cb_dia = 9.0
top_cb_depth = 5.0
front_hole_dia = 5.0

# 1. Create the main rectangular block
# Oriented with Z as height, X as width, Y as thickness
result = cq.Workplane("XY").box(width, thickness, height)

# 2. Chamfer the vertical edges
# This creates the angled corners seen on the top and bottom profiles
result = result.edges("|Z").chamfer(chamfer_size)

# 3. Create the recess (slot) on the left side
# Select the left face (-X direction)
# Draw a rectangle centered on the face. 
# Width is set larger than thickness to ensure it cuts through the entire depth (Y)
# Height determines the vertical span of the cut.
# cutBlind cuts into the material by the specified depth.
result = (
    result.faces("<X").workplane()
    .rect(thickness * 2, side_cut_height)
    .cutBlind(-side_cut_depth)
)

# 4. Create counterbored holes on the top face
# Select the top face (+Z direction)
# Holes are aligned along the X-axis (width)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-top_hole_spacing / 2.0, 0), (top_hole_spacing / 2.0, 0)])
    .cboreHole(top_hole_dia, top_cb_dia, top_cb_depth)
)

# 5. Create simple holes on the front face
# Select the front face (+Y direction)
# Holes are aligned along the Z-axis (height)
result = (
    result.faces(">Y").workplane()
    .pushPoints([(0, front_hole_spacing / 2.0), (0, -front_hole_spacing / 2.0)])
    .hole(front_hole_dia)
)