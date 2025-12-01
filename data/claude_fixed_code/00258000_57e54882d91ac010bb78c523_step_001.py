import cadquery as cq

# Define parameters for the box dimensions
length = 60.0
width = 40.0
height = 50.0
fillet_radius = 3.0

# Create the box and fillet all edges
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z")
    .fillet(fillet_radius)
)