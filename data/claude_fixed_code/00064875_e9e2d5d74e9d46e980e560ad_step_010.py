import cadquery as cq

# Dimensions estimated from the visual proportions of the image
# The object is a long, thin cylinder.
length = 200.0
diameter = 6.0
radius = diameter / 2.0

# Create the cylindrical rod
# We start on the XY plane, draw the circular profile, and extrude it vertically.
result = cq.Workplane("XY").circle(radius).extrude(length)