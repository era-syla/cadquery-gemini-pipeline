import cadquery as cq

# Dimensions based on visual estimation of proportions
length_x = 50.0
length_y = 35.0
thickness = 20.0
# Radius of the arc connecting the two endpoints. 
# Needs to be larger than half the chord length to form a valid arc.
# A positive radius in radiusArc creates a curve "to the left" of the path,
# which results in a convex shape (bulging away from origin) in this orientation.
arc_radius = 55.0

result = (
    cq.Workplane("XY")
    .lineTo(length_x, 0)
    .radiusArc((0, length_y), -arc_radius)
    .close()
    .extrude(thickness)
)