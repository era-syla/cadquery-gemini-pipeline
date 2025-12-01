import cadquery as cq

# Parametric dimensions
length = 10.0
width = 10.0
height = 10.0

# Create the box/cube geometry
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))