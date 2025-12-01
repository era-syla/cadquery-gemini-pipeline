import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0
width = 50.0
height = 10.0

# Create the solid rectangular box
result = cq.Workplane("XY").box(length, width, height).translate((0, 0, height/2))