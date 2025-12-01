import cadquery as cq

# The image shows a 3D solid with an elliptical cross-section, known as an elliptical cylinder.
# It is defined by a major radius, a minor radius, and an extrusion thickness.

# Estimated dimensions based on visual proportions:
# The width (major axis) looks about twice the height (minor axis).
major_radius = 20.0
minor_radius = 10.0
thickness = 15.0

# Generate the elliptical cylinder
result = (
    cq.Workplane("XY")
    .ellipseArc(major_radius, minor_radius, 0, 360)
    .close()
    .extrude(thickness)
)