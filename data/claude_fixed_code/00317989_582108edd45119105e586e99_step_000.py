import cadquery as cq

# Parametric dimensions
length = 100.0
width = 50.0
height = 30.0

# Create the rectangular box
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))