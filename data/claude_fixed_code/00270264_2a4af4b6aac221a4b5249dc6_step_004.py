import cadquery as cq
import math

# --- Parameters ---
width = 25.0
depth = 19.0
case_height = 8.0
standoff_height = 0.5

# Display Segment Parameters
digit_center_offset = 6.35  # Distance of digit center from global center
segment_length = 4.2
segment_width = 0.7
slant_angle = 8.0  # Degrees
digit_scale_y = 3.4  # Vertical scale for positioning segments
digit_scale_x = 3.2  # Horizontal scale for positioning segments

# Pin Parameters
pin_pitch = 2.54
row_spacing = 15.24
pin_length = 4.0
pins_per_row = 9
pin_size = 0.5

# --- Helper Functions ---

def create_segment_shape(length, width, vertical=False):
    """Creates a hexagonal segment face centered at origin"""
    l = length
    w = width
    half_l = l / 2.0
    half_w = w / 2.0
    
    # Points for horizontal hexagon
    pts = [
        (-half_l, 0),
        (-half_l + half_w, half_w),
        (half_l - half_w, half_w),
        (half_l, 0),
        (half_l - half_w, -half_w),
        (-half_l + half_w, -half_w),
        (-half_l, 0)
    ]
    
    # Create face
    wp = cq.Workplane("XY").polyline(pts).close()
    
    if vertical:
        wp = wp.rotate((0,0,0), (0,0,1), 90)
        
    return wp

# --- Build Geometry ---

# 1. Main Body Block
# Positioned above Z=0 by standoff_height
main_body = (
    cq.Workplane("XY")
    .box(width, depth, case_height)
    .translate((0, 0, case_height/2 + standoff_height))
)

# 2. Corner Standoffs (Feet)
# Small cylinders at the corners to lift the body
fx = width/2 - 1.2
fy = depth/2 - 1.2
feet = (
    cq.Workplane("XY")
    .rect(2*fx, 2*fy, forConstruction=True)
    .vertices()
    .circle(1.2)
    .extrude(standoff_height + 1.0) # Overlap into body
)
body = main_body.union(feet)

# 3. Create Segments for Boolean Cut
shear_factor = math.tan(math.radians(slant_angle))

# Relative positions of segments A-G (dx_factor, dy_factor, is_vertical)
# Layout based on standard 7-segment topology
segment_layout = [
    (0, 2, False),    # A (Top)
    (1, 1, True),     # B (Top Right)
    (1, -1, True),    # C (Bottom Right)
    (0, -2, False),   # D (Bottom)
    (-1, -1, True),   # E (Bottom Left)
    (-1, 1, True),    # F (Top Left)
    (0, 0, False)     # G (Middle)
]

# Top Z position for cutting
top_z = case_height + standoff_height

# Generate segments for two digits
for sign in [-1, 1]:
    cx = sign * digit_center_offset
    
    # Generate 7 segments
    for dx_f, dy_f, is_vert in segment_layout:
        # Calculate raw position
        raw_dx = dx_f * digit_scale_x
        raw_dy = dy_f * digit_scale_y
        
        # Apply slant shear (X shifts based on Y)
        shear_x = raw_dy * shear_factor
        
        final_x = cx + raw_dx + shear_x
        final_y = raw_dy
        
        # Create segment and extrude downward
        seg = (
            create_segment_shape(segment_length, segment_width, is_vert)
            .translate((final_x, final_y, top_z))
            .extrude(-0.6)
        )
        body = body.cut(seg)
        
    # Generate Decimal Point
    # Positioned to the right of the digit, aligned with bottom
    dp_y = -2 * digit_scale_y
    dp_x = cx + digit_scale_x + 1.5 + (dp_y * shear_factor)
    
    dp = (
        cq.Workplane("XY")
        .center(dp_x, dp_y)
        .circle(0.45)
        .translate((0, 0, top_z))
        .extrude(-0.6)
    )
    body = body.cut(dp)

# 4. Pins
# Generate array of pins
pins = (
    cq.Workplane("XY")
    .workplane(offset=standoff_height)
    .rarray(pin_pitch, row_spacing, pins_per_row, 2)
    .rect(pin_size, pin_size)
    .extrude(-pin_length)
)

# 5. Final Assembly
result = body.union(pins)

# Export or Display logic would go here, 'result' holds the final solid.