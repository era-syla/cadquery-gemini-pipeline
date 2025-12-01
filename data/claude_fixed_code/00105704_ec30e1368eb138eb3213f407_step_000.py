import cadquery as cq

# Dimensions based on visual analysis
box_width = 80.0
box_depth = 40.0
box_height = 40.0

# Top elliptical cylinder dimensions
ellipse_major_radius = 32.0
ellipse_minor_radius = 14.0
ellipse_height = 25.0

# Drawer face details (groove cut)
drawer_margin = 5.0
groove_width = 1.0
groove_depth = 2.0

# Calculate rectangle dimensions for the groove
rect_outer_w = box_width - 2 * drawer_margin
rect_outer_h = box_height - 2 * drawer_margin
rect_inner_w = rect_outer_w - 2 * groove_width
rect_inner_h = rect_outer_h - 2 * groove_width

# Handle dimensions
handle_radius = 3.0
handle_length = 10.0

# 1. Create the main rectangular body
result = cq.Workplane("XY").box(box_width, box_depth, box_height)

# 2. Add the elliptical cylinder to the top face
# Select the top face (+Z), draw ellipse, and extrude upwards
ellipse_part = (
    cq.Workplane("XY")
    .workplane(offset=box_height/2)
    .ellipse(ellipse_major_radius, ellipse_minor_radius)
    .extrude(ellipse_height)
)
result = result.union(ellipse_part)

# 3. Create the "drawer" look by cutting a groove on the front face
# Select the front face (-Y)
# Draw two rectangles; the area between them forms the groove
# cutBlind(positive) cuts into the material
result = (
    result.faces("<Y")
    .workplane()
    .rect(rect_outer_w, rect_outer_h)
    .rect(rect_inner_w, rect_inner_h)
    .cutBlind(groove_depth)
)

# 4. Add the cylindrical handle to the center of the drawer
# Re-select the front face (-Y). This effectively selects the face of the "island" created by the groove.
# Draw a circle and extrude outwards
handle_part = (
    cq.Workplane("XY")
    .workplane(offset=-box_depth/2)
    .transformed(rotate=(90, 0, 0))
    .circle(handle_radius)
    .extrude(-handle_length)
)
result = result.union(handle_part)