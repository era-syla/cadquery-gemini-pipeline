import cadquery as cq

# Dimensions estimated from the image
# The object is a hollow cylinder (tube) with a moderate wall thickness.
length = 50.0
outer_diameter = 30.0
inner_diameter = 20.0  # Resulting in a 5mm wall thickness

# Create the tube
# 1. Establish a workplane (XY).
# 2. Draw the outer circle.
# 3. Draw the inner circle.
# 4. Extrude the region between the two circles to create the tube.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length, combine='cut')
)