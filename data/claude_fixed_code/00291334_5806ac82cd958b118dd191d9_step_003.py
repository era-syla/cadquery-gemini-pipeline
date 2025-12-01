import cadquery as cq

# Dimensions
major_radius = 40.0  # Radius from the center of the torus to the center of the tube
minor_radius = 4.0   # Radius of the tube (thickness)

# Create the torus geometry
# We define a workplane on the XZ plane, offset the center by the major radius,
# draw the cross-section circle, and revolve it around the vertical axis (Z-axis).
result = (
    cq.Workplane("XZ")
    .move(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)