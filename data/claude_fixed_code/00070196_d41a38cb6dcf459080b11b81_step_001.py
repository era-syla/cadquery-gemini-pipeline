import cadquery as cq

# Analyze the geometry dimensions based on the image
# The object appears to be a vertical prism with a trapezoidal cross-section.
# It has a "front" face that is rectangular with rounded corners (fillets).
# The left side is thicker than the right side.
# There is a hole centered on the front face.

height = 60.0         # Height of the block
width = 35.0          # Width of the front face
depth_left = 25.0     # Thickness of the left side
depth_right = 10.0    # Thickness of the right side
fillet_radius = 4.0   # Radius of the vertical edge fillets
hole_diameter = 6.0   # Diameter of the center hole

# Create the base shape
# We draw the profile on the XY plane and extrude along Z.
# The profile is a trapezoid:
# - Front edge: along X axis
# - Left edge: along Y axis (longer depth)
# - Right edge: along Y axis (shorter depth)
# - Back edge: Connects the back of left and right edges
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),                  # Front-Left corner
        (width, 0),              # Front-Right corner
        (width, depth_right),    # Back-Right corner
        (0, depth_left)          # Back-Left corner
    ])
    .close()
    .extrude(height)
)

# Apply fillets to the vertical edges
# The image shows rounded corners on the vertical faces.
result = result.edges("|Z").fillet(fillet_radius)

# Create the hole
# We select the front face (which corresponds to the face with the minimum Y coordinate)
# and drill a hole through it. The Workplane center defaults to the face center.
result = (
    result.faces("<Y")
    .workplane()
    .hole(hole_diameter)
)