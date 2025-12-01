import cadquery as cq

# The image shows a simple solid cylinder (rod).
# Based on visual proportions, the length is significantly larger than the diameter.
# We will use representative dimensions to recreate this geometry.

# Dimensions
length = 80.0  # Length of the cylinder
radius = 5.0   # Radius of the cylinder

# Create the cylindrical rod
# 1. Initialize a workplane (XY plane is standard)
# 2. Draw a circle with the defined radius
# 3. Extrude the circle to the defined length to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(length)