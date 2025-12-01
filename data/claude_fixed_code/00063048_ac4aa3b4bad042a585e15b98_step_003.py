import cadquery as cq

# Based on the image analysis, the object is a simple rectangular plate.
# The visual proportions suggest a length-to-width ratio of approximately 2:1.
# The thickness is small compared to the planar dimensions.

# Define parameters
length = 100.0
width = 50.0
thickness = 2.0

# Create the rectangular plate centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)