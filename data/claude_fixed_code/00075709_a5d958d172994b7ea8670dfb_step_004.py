import cadquery as cq

# Dimensions estimated from the image
outer_diameter = 20.0
inner_diameter = 12.0
height = 20.0
slot_width = 5.0

# 1. Create the base hollow cylinder (tube)
# We draw two concentric circles on the XY plane and extrude them.
# The area between the circles forms the solid wall.
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)

# 2. Create the geometry to cut the slot
# We create a rectangular box positioned to intersect one side of the cylinder wall.
# By positioning the center at (radius, 0), the box covers the wall from the
# inner radius to the outside.
cutter = (
    cq.Workplane("XY")
    .rect(outer_diameter, slot_width)
    .extrude(height)
    .translate((outer_diameter / 2.0, 0, 0))
)

# 3. Subtract the cutter from the base to form the final result
result = base.cut(cutter)