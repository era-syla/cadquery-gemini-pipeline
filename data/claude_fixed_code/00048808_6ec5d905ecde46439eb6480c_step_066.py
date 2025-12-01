import cadquery as cq

# 1. Parameter Definitions
# Estimated dimensions based on visual analysis of the ""dogbone"" tensile specimen.
total_length = 150.0
grip_width = 30.0
gauge_width = 12.0
thickness = 8.0
grip_length = 35.0
transition_length = 15.0
hole_diameter = 10.0

# 2. Geometric Calculations
# Calculate coordinates relative to the center origin (0,0)
half_len = total_length / 2.0
half_w_grip = grip_width / 2.0
half_w_gauge = gauge_width / 2.0

# Y-coordinates for the transition sections
y_grip_end = half_len - grip_length
y_gauge_start = y_grip_end - transition_length

# 3. Profile Definition
# Define the points for the 2D profile in clockwise order.
# The shape consists of the wide grips, tapered transitions, and the narrow gauge section.
points = [
    (-half_w_grip, half_len),           # Top-Left corner
    (half_w_grip, half_len),            # Top-Right corner
    (half_w_grip, y_grip_end),          # End of top grip (right side)
    (half_w_gauge, y_gauge_start),      # Start of gauge (right side, after taper)
    (half_w_gauge, -y_gauge_start),     # End of gauge (right side)
    (half_w_grip, -y_grip_end),         # Start of bottom grip (right side, after taper)
    (half_w_grip, -half_len),           # Bottom-Right corner
    (-half_w_grip, -half_len),          # Bottom-Left corner
    (-half_w_grip, -y_grip_end),        # Start of bottom grip (left side)
    (-half_w_gauge, -y_gauge_start),    # End of gauge (left side, after taper)
    (-half_w_gauge, y_gauge_start),     # Start of gauge (left side)
    (-half_w_grip, y_grip_end),         # End of top grip (left side, after taper)
]

# 4. 3D Model Construction
# Create the base body by extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# 5. Adding Holes
# Calculate the center position for the holes within the grip sections
hole_y_pos = half_len - (grip_length / 2.0)

# Cut the mounting holes through the grips
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (0, hole_y_pos),    # Top hole
        (0, -hole_y_pos)    # Bottom hole
    ])
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)