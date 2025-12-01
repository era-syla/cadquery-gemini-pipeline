import cadquery as cq

# Geometric analysis:
# The object is a circular ring (annulus) with a rectangular cross-section, commonly known as a washer.
# The visible vertical line on the right side is typical of a rendering seam on a closed periodic surface 
# (where the revolution starts/ends, usually at 0 degrees), rather than a physical split or gap.
#
# Estimated Dimensions:
# - The ring appears relatively thin compared to its diameter.
# - The radial width (difference between outer and inner radius) appears larger than the thickness (height).

outer_radius = 20.0
inner_radius = 18.0
thickness = 1.0

# Create the washer geometry
# We draw two concentric circles on the XY plane and extrude them.
# CadQuery automatically interprets the area between the two nested wires as the solid face.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)