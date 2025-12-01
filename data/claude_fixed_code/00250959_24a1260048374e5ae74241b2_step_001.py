import cadquery as cq

# Dimensions
height = 100.0  # Vertical length
width = 50.0    # Horizontal width
depth = 20.0    # Depth of the box
thickness = 2.0 # Wall thickness
fillet_radius = 5.0

# Create the shell geometry
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .edges("|Z")  # Select vertical edges
    .fillet(fillet_radius)
    .shell(-thickness) # Shell inwards to create walls
)