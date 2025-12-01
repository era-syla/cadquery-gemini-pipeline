import cadquery as cq

# Parameters based on visual estimation of the image
# The object is a long cylindrical rod with a high length-to-diameter ratio.
rod_length = 200.0
rod_diameter = 10.0
chamfer_size = 0.5  # Small chamfer at the ends for a finished look

# Create the main cylindrical shape
# We start on the XY plane, draw a circle, and extrude it to the desired length along the Z axis.
result = cq.Workplane("XY").circle(rod_diameter / 2.0).extrude(rod_length)

# Apply chamfers to the ends
# Select the faces that are perpendicular to the Z axis (top and bottom faces),
# grab their edges, and apply the chamfer.
result = result.faces(">Z").edges().chamfer(chamfer_size)
result = result.faces("<Z").edges().chamfer(chamfer_size)