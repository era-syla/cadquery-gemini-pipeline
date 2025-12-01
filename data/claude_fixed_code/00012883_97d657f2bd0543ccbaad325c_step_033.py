import cadquery as cq

# Geometric parameters estimated from the image
height = 300.0       # Total vertical length of the profile
leg_width = 25.0     # Width of the legs (outer dimension)
thickness = 2.5      # Thickness of the material

# Create the L-shaped profile sketch on the XY plane
# The shape is drawn starting from the outer corner at (0,0)
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),                       # Outer corner
        (leg_width, 0),               # End of first leg
        (leg_width, thickness),       # Inner edge of first leg
        (thickness, thickness),       # Inner corner
        (thickness, leg_width),       # Inner edge of second leg
        (0, leg_width)                # End of second leg
    ])
    .close()
    .extrude(height)                  # Extrude vertically to form the 3D object
)