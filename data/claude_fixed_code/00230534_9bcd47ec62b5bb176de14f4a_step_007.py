import cadquery as cq

# Define dimensions based on visual analysis of the image
# The object is a simple cylinder with a high aspect ratio (rod-like).
radius = 5.0
height = 60.0

# Create the cylinder
# 1. Start on the XY plane (ground).
# 2. Draw a circle for the base.
# 3. Extrude it vertically to the specified height.
result = cq.Workplane("XY").circle(radius).extrude(height)