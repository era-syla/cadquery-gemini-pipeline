import cadquery as cq

# Define dimensions based on visual analysis of the image
# The object corresponds to a washer or spacer with a central hole.
outer_radius = 15.0  # Estimated outer radius
inner_radius = 5.0   # Estimated inner radius (approx 1/3 of outer)
thickness = 4.0      # Estimated thickness

# Generate the 3D object
# We draw two concentric circles on the XY plane.
# CadQuery automatically interprets the inner circle as a hole during extrusion.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)