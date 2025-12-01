import cadquery as cq

# Parametric dimensions
major_radius = 20.0  # Distance from center of torus to center of tube
minor_radius = 2.0   # Radius of the tube itself

# Create the torus geometry
# We sketch a circle on the XZ plane offset by the major radius,
# then revolve it around the Z-axis.
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)