import cadquery as cq

# Dimensions estimated from the image
total_length = 120.0
height = 30.0
width = 15.0
thickness = 2.0

# Feature parameters
split_position = 60.0  # Length of the L-section (left side)
slot_lower_height = 6.0
slot_gap = 4.0

# Step 1: Create the base U-channel profile
# We draw the cross-section on the YZ plane and extrude along the X axis.
# Orientation:
# - Front wall is at Y=0
# - Back wall is at Y=width
# - Floor is at Z=0
pts = [
    (0, height),                    # Top of front wall
    (0, 0),                         # Bottom of front wall
    (width, 0),                     # Bottom of back wall
    (width, height),                # Top of back wall
    (width - thickness, height),    # Inner top of back wall
    (width - thickness, thickness), # Inner bottom of back wall
    (thickness, thickness),         # Inner bottom of front wall
    (thickness, height)             # Inner top of front wall
]

# Extrude the base shape
# The profile is on YZ, extrusion goes along positive X
result = cq.Workplane("YZ").polyline(pts).close().extrude(total_length)

# Step 2: Cut the front wall on the left side to form the L-profile section
# We remove the material of the front wall (Y approx 0) from X=0 to X=split_position.
# Z range: from thickness (top of floor) to height.
cut_left_len = split_position
cut_left_height = height - thickness
cut_left_center_x = split_position / 2.0
cut_left_center_z = thickness + (cut_left_height / 2.0)

# Create a cutting box positioned to remove the front flange
# Y size is slightly larger than thickness to ensure a clean cut through the wall at Y=0
cut_box_1 = cq.Workplane("XY").box(cut_left_len, thickness * 2.1, cut_left_height).translate((cut_left_center_x, 0, cut_left_center_z))
result = result.cut(cut_box_1)

# Step 3: Cut the slot in the front wall on the right side
# Region: X from split_position to total_length
slot_len = total_length - split_position
slot_center_x = split_position + (slot_len / 2.0)
slot_center_z = slot_lower_height + (slot_gap / 2.0)

# Create a cutting box for the slot
cut_box_2 = cq.Workplane("XY").box(slot_len, thickness * 2.1, slot_gap).translate((slot_center_x, 0, slot_center_z))
result = result.cut(cut_box_2)