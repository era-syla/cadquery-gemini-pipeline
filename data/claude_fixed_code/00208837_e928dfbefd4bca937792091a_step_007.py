import cadquery as cq

# Dimensions derived from visual analysis of the image
length = 50.0          # Length of the extrusion
outer_radius = 20.0    # Radius of the outer cylindrical surface
inner_radius = 13.0    # Radius of the inner bore
flat_offset = 15.0     # Perpendicular distance from the center axis to the flat bottom face

# 1. Create the base hollow cylinder profile
# We draw on the YZ plane and extrude along the X axis to match the orientation in the image
result = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)

# 2. Create the flat cut at the bottom
# The flat face corresponds to a plane intersecting the cylinder at Z = -flat_offset.
# We create a box representing the material to be removed (everything below Z = -flat_offset).
cut_box_height = 50.0  # Height of the cutter box (needs to be large enough to clear the bottom)
cutter = (
    cq.Workplane("XY")
    .box(length * 2, outer_radius * 3, cut_box_height)
    .translate((length / 2, 0, -flat_offset - (cut_box_height / 2)))
)

# 3. Apply the cut to the base object
result = result.cut(cutter)