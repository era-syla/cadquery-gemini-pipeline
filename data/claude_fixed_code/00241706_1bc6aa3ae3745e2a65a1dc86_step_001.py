import cadquery as cq

# Geometric parameters derived from visual analysis of the image
height = 10.0           # Vertical thickness of the extrusion
wall_width = 10.0       # Width of the solid profile
inner_radius = 12.0     # Radius of the inner arc curves
straight_length = 50.0  # Length of the straight sections (center-to-center)
gap_width = 20.0        # Size of the opening cut in the side

# Derived dimensions
outer_radius = inner_radius + wall_width
outer_diameter = 2 * outer_radius
inner_diameter = 2 * inner_radius

# Step 1: Create the base hollow stadium (racetrack) shape.
# We use the slot2D method which creates a shape defined by center-to-center length and diameter.
# We create the outer shape and subtract the inner shape to form the closed loop profile, then extrude.
result = (
    cq.Workplane("XY")
    .slot2D(straight_length, outer_diameter)
    .slot2D(straight_length, inner_diameter, mode='s') # Subtract the inner slot
    .extrude(height)
)

# Step 2: Cut the gap in one of the straight sections.
# The slot is centered at (0,0) and aligned with the X-axis.
# The straight walls are located at +/- Y. We will cut the wall at negative Y.
cut_y_center = -(inner_radius + wall_width / 2)

# We create a box at the location of the cut and subtract it from the main body.
# The box dimensions are oversized in depth and height to ensure a clean cut through the wall.
result = result.cut(
    cq.Workplane("XY")
    .center(0, cut_y_center)       # Move to the center of the wall to be cut
    .box(gap_width, wall_width * 2, height * 2) # Create the cutting tool (Box is centered at cursor)
)