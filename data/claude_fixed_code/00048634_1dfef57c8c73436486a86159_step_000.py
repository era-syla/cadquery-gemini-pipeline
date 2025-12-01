import cadquery as cq

# Define dimensions based on visual analysis of the image
# The object appears to be a square plate with a central circular hole.
plate_width = 80.0
plate_height = 80.0
plate_thickness = 10.0
hole_diameter = 40.0

# Create the object
# 1. Start with a Workplane on the XY plane
# 2. Create a box (rectangular plate) centered at the origin
# 3. Select the top face (Z-positive) to perform the cut
# 4. Create a hole through the center of the selected face
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)