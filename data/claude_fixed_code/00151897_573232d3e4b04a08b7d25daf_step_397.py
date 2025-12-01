import cadquery as cq

# Dimensions
length = 160.0
width = 80.0
thickness = 4.0
fillet_radius = 20.0

# Create the base rectangular plate centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# Apply fillet to the top-right corner (Positive X, Positive Y quadrant)
# Based on the image, only one corner appears significantly rounded
result = result.edges(">X and >Y and |Z").fillet(fillet_radius)

# Feature 1: Left Side Mounting Holes
# Two small holes near the straight corners on the left
left_hole_offset_x = length / 2 - 8
left_hole_offset_y = width / 2 - 8
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-left_hole_offset_x, left_hole_offset_y),
        (-left_hole_offset_x, -left_hole_offset_y)
    ])
    .hole(4.2)  # Approximately M4 clearance
)

# Feature 2: Center Motor Mount (NEMA 17 style pattern)
# Consists of a large central bore and 4 mounting holes
motor_pos_x = -15.0  # Slightly offset from center
motor_bore_d = 24.0
motor_mount_spacing = 31.0
motor_mount_hole_d = 3.5

# Cut the large central hole
result = (
    result.faces(">Z")
    .workplane()
    .center(motor_pos_x, 0)
    .circle(motor_bore_d / 2)
    .cutThruAll()
)

# Cut the 4 surrounding mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .center(motor_pos_x, 0)
    .rect(motor_mount_spacing, motor_mount_spacing, forConstruction=True)
    .vertices()
    .hole(motor_mount_hole_d)
)

# Feature 3: Right Side Features
# Includes a medium-sized hole and surrounding mounting holes
right_feature_x = 50.0
right_feature_y = -5.0  # Slightly offset in Y
medium_hole_d = 12.0

# Cut the medium hole
result = (
    result.faces(">Z")
    .workplane()
    .center(right_feature_x, right_feature_y)
    .hole(medium_hole_d)
)

# Additional mounting holes on the right side
# Coordinates estimated based on image features relative to corners and medium hole
right_holes_pts = [
    (length/2 - 8, -width/2 + 8),        # Bottom-right corner (Sharp)
    (length/2 - 14, width/2 - 14),       # Top-right corner (Near Fillet)
    (right_feature_x + 10, right_feature_y - 12)  # Small hole near the medium hole
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(right_holes_pts)
    .hole(4.2)
)