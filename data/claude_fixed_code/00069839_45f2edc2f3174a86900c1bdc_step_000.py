import cadquery as cq

# The image shows a regular hexagonal prism.
# Visually estimating the dimensions:
# The height appears to be roughly 1.5 times the width (diameter).
# We will use a circumscribed diameter of 20 and a height of 30.

diameter = 20.0
height = 30.0

result = (
    cq.Workplane("XY")
    .polygon(6, diameter)
    .extrude(height)
)