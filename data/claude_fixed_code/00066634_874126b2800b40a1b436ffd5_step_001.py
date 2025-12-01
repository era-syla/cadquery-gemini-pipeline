import cadquery as cq

# Define dimensions based on the image analysis
# The object is a simple cylinder with a high aspect ratio (rod-like)
height = 100.0
radius = 6.0

# Generate the cylinder
# 1. Create a workplane on the XY plane
# 2. Draw a circle for the base
# 3. Extrude the circle to the specified height
result = cq.Workplane("XY").circle(radius).extrude(height)