import cadquery as cq

# Parametric dimensions for the rectangular hollow section
length = 100.0
width = 30.0
height = 20.0
wall_thickness = 2.0
corner_radius = 3.0

# Create the 3D model
# 1. Start with a solid box representing the outer boundaries
# 2. Fillet the longitudinal edges to create the rounded profile
# 3. Shell the solid inwards by the wall thickness, removing the end faces to create a tube
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|X")
    .fillet(corner_radius)
    .shell(-wall_thickness, kind="intersection")
)