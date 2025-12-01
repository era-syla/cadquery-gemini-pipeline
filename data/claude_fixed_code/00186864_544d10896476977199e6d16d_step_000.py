import cadquery as cq

# Dimensions estimated from the image
length = 120.0
width = 40.0
thickness = 10.0
fillet_radius = 5.0
hole_diameter = 8.0
num_holes = 5
hole_spacing = 20.0

# Create the 3D object
result = (
    cq.Workplane("XY")
    # 1. Create the base rectangular block
    .box(length, width, thickness)
    # 2. Fillet the four vertical edges
    .edges("|Z")
    .fillet(fillet_radius)
    # 3. Select the top face to place the holes
    .faces(">Z")
    .workplane()
    # 4. Generate a linear array of 5 points along the X-axis
    .rarray(hole_spacing, 1, num_holes, 1)
    # 5. Cut the holes through the object
    .hole(hole_diameter, depth=thickness)
)