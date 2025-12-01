import cadquery as cq

# Dimensions inferred from the image analysis
# The object is a C-channel or U-channel profile extruded linearly.
length = 80.0    # Depth of the extrusion
width = 50.0     # Outer width of the C-profile
height = 40.0    # Outer height of the C-profile
thickness = 4.0  # Thickness of the walls

# Create the 3D object
# We draw the C-shaped profile on the XZ plane (Front plane) and extrude it along the Y axis.
# The profile is oriented such that the continuous back wall is on the right (+X)
# and the opening faces the left (-X), matching the visual orientation of a standard C-channel.
result = (
    cq.Workplane("XZ")
    .polyline([
        (width, 0),                             # Bottom-right corner (Outer)
        (0, 0),                                 # Bottom-left tip (Outer)
        (0, thickness),                         # Bottom-left tip (Inner)
        (width - thickness, thickness),         # Bottom inner corner
        (width - thickness, height - thickness),# Top inner corner
        (0, height - thickness),                # Top-left tip (Inner)
        (0, height),                            # Top-left tip (Outer)
        (width, height),                        # Top-right corner (Outer)
    ])
    .close()
    .extrude(length)
)