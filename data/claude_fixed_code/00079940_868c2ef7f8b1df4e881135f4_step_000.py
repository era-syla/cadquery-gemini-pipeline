import cadquery as cq

# The image displays a simple cylindrical primitive.
# There are no visible holes, chamfers, or fillets.
# The vertical line represents the seam of the cylindrical face in the rendering.

# Estimated dimensions based on aspect ratio
radius = 10.0
height = 30.0

# Create the cylinder by drawing a circle on the XY plane and extruding it
result = cq.Workplane("XY").circle(radius).extrude(height)