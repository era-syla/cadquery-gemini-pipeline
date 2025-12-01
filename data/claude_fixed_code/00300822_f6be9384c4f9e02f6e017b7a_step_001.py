import cadquery as cq

# Define parametric dimensions for the rectangular bar
length = 200.0
width = 10.0
height = 10.0

# Create the rectangular prism (box)
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))