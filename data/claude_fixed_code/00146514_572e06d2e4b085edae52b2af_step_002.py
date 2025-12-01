import cadquery as cq

# Analyze the image dimensions
# The object is a long, thin cylinder (a rod).
# Based on visual estimation, the aspect ratio (Height / Diameter) is approximately 25:1.
length = 100.0
radius = 2.0

# Generate the geometry
# Start on the XY plane to orient the cylinder vertically along the Z-axis.
# Draw the circular cross-section and extrude it to the specified length.
result = cq.Workplane("XY").circle(radius).extrude(length)