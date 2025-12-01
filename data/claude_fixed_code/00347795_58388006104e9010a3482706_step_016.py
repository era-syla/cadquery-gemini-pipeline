import cadquery as cq

# -- Parametric Dimensions --
cap_diameter = 50.0
cap_height = 12.0
wall_thickness = 1.5

tab_width = 15.0
tab_height = 8.5
tab_protrusion = 5.0
tab_chamfer_size = 2.5
top_fillet_radius = 1.0

# -- Model Construction --

# 1. Main Body: Create the base cylinder
main_body = cq.Workplane("XY").circle(cap_diameter / 2.0).extrude(cap_height)

# 2. Tabs: Create the grip tabs
# Calculate total length of the bar that forms the tabs
tab_total_length = cap_diameter + (2.0 * tab_protrusion)

# Create a box centered on XY, starting from Z=0
tabs = (
    cq.Workplane("XY")
    .box(tab_total_length, tab_width, tab_height, centered=(True, True, False))
)

# Chamfer the top outer edges of the tabs (slope downwards)
# Select edges parallel to Y at the top of the box
tabs = tabs.edges("|Y and >Z").chamfer(tab_chamfer_size)

# Fillet the vertical edges of the tabs for a smoother look
tabs = tabs.edges("|Z").fillet(1.0)

# 3. Combine: Union the cylinder and the tabs
combined_solid = main_body.union(tabs)

# 4. Refine: Fillet the top edge of the cap
# Select the topmost edges (the circular rim) - filter to avoid tab edges
final_solid = combined_solid.faces(">Z").edges("%Circle").fillet(top_fillet_radius)

# 5. Hollow: Shell the solid from the bottom face
# Use a negative offset to shell inwards
result = final_solid.faces("<Z").shell(-wall_thickness)