import cadquery as cq

# The image shows a simple solid cylindrical shape, resembling a disk or puck.
# There are no visible holes, chamfers, or fillets.
# The vertical line on the side is interpreted as the seam of the periodic cylindrical face
# characteristic of CAD rendering engines, rather than a geometric feature.

# Defined dimensions based on visual proportions (Diameter roughly 5-6x Height)
radius = 25.0
height = 10.0

# Create the cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)