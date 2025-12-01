import cadquery as cq

# Parameters
thickness = 4.0
height = 30.0
main_length = 240.0   # Inner length of the main back section
leg_length = 60.0     # Inner length of the side legs
bend_radius = 8.0     # Inner radius of the bend

hole_dia_center = 16.0
hole_dia_small = 6.0

# Geometric calculations for the profile
# Origin (0,0) is at the center of the inner back face on the XY plane.
# The U-shape opens towards +Y.
x_inner = main_length / 2.0
x_outer = x_inner + thickness
y_back_inner = 0.0
y_back_outer = -thickness
y_leg = leg_length

# Define the points for the 2D profile (Top-down view)
pts = [
    (-x_outer, y_leg),          # Outer Left Leg Tip
    (-x_outer, y_back_outer),   # Outer Left Corner
    ( x_outer, y_back_outer),   # Outer Right Corner
    ( x_outer, y_leg),          # Outer Right Leg Tip
    ( x_inner, y_leg),          # Inner Right Leg Tip
    ( x_inner, y_back_inner),   # Inner Right Corner
    (-x_inner, y_back_inner),   # Inner Left Corner
    (-x_inner, y_leg)           # Inner Left Leg Tip
]

# Create the base extrusion
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

# Add fillets to create the bends
# Filter inner vertical edges (near Y=0)
result = result.edges("|Z").edges(
    cq.selectors.BoxSelector((-x_inner - 0.1, -0.1, -0.1), (-x_inner + 0.1, 0.1, height + 0.1))
).fillet(bend_radius)

result = result.edges("|Z").edges(
    cq.selectors.BoxSelector((x_inner - 0.1, -0.1, -0.1), (x_inner + 0.1, 0.1, height + 0.1))
).fillet(bend_radius)

# Filter outer vertical edges (near Y=-thickness)
result = result.edges("|Z").edges(
    cq.selectors.BoxSelector((-x_outer - 0.1, y_back_outer - 0.1, -0.1), (-x_outer + 0.1, y_back_outer + 0.1, height + 0.1))
).fillet(bend_radius + thickness)

result = result.edges("|Z").edges(
    cq.selectors.BoxSelector((x_outer - 0.1, y_back_outer - 0.1, -0.1), (x_outer + 0.1, y_back_outer + 0.1, height + 0.1))
).fillet(bend_radius + thickness)

# Cut the large center hole on the front face
# Selecting face <Y picks the outer back face
result = (
    result.faces("<Y").workplane()
    .center(0, 0)
    .circle(hole_dia_center / 2.0)
    .cutThruAll()
)

# Cut the 4 smaller holes on the front face
# Offsets relative to the center of the face
front_hole_offsets = [(-55, 0), (-100, 0), (55, 0), (100, 0)]
result = (
    result.faces("<Y").workplane()
    .pushPoints(front_hole_offsets)
    .circle(hole_dia_small / 2.0)
    .cutThruAll()
)

# Cut the holes on the side legs
# We select the outer face of the right leg (>X) and cut through all to hit the left leg as well
# Using ProjectedOrigin allows us to use global coordinates mapped to the local plane
# Local X corresponds to Global Y, Local Y corresponds to Global Z
side_hole_y1 = leg_length - 15.0
side_hole_y2 = leg_length - 40.0
side_hole_pts = [(side_hole_y1, height / 2.0), (side_hole_y2, height / 2.0)]

result = (
    result.faces(">X").workplane(centerOption="ProjectedOrigin")
    .pushPoints(side_hole_pts)
    .circle(hole_dia_small / 2.0)
    .cutThruAll()
)