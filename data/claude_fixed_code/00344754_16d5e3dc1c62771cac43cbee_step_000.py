import cadquery as cq

# Parametric dimensions
length = 20.0  # Length of the cube
width = 20.0   # Width of the cube
height = 20.0  # Height of the cube
hole_diameter = 4.0  # Diameter of the center hole

# Create the box and drill a hole through the center of the top face
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter, depth=height)
)