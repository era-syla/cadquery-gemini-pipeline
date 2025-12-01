import cadquery as cq

# --- Object Parameters ---
# Based on standard LEGO brick dimensions (1x12 Beam/Brick)
# All units in millimeters
PITCH = 8.0               # Distance between stud centers
TOLERANCE = 0.2           # Total spacing tolerance (brick is slightly smaller than grid)
STUD_DIAMETER = 4.8
STUD_HEIGHT = 1.7
BRICK_HEIGHT = 9.6        # Standard full brick height

# Configuration: 1 row of 12 studs
NUM_STUDS_LENGTH = 12
NUM_STUDS_WIDTH = 1

# Calculated overall dimensions
# Actual physical dimension is (Count * Pitch) - Tolerance
total_length = (NUM_STUDS_LENGTH * PITCH) - TOLERANCE
total_width = (NUM_STUDS_WIDTH * PITCH) - TOLERANCE

# --- Geometry Creation ---

# 1. Create the main rectangular body
# Using a centered box simplifies the placement of the stud array later
result = cq.Workplane("XY").box(total_length, total_width, BRICK_HEIGHT)

# 2. Add the studs to the top face
result = (
    result
    .faces(">Z")                  # Select the top face (positive Z)
    .workplane()                  # Create a workplane on this face
    .rarray(                      # Create a rectangular array of points
        xSpacing=PITCH,           # Spacing along X axis
        ySpacing=PITCH,           # Spacing along Y axis (unused since count is 1)
        xCount=NUM_STUDS_LENGTH,  # Number of studs along length (12)
        yCount=NUM_STUDS_WIDTH    # Number of studs along width (1)
    )
    .circle(STUD_DIAMETER / 2.0)  # Draw circles at each array point
    .extrude(STUD_HEIGHT)         # Extrude circles to create studs
)