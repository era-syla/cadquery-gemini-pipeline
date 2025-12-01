import cadquery as cq

# --- Dimensions ---
frame_length = 100.0
frame_width = 60.0
tube_size = 4.0         # Square profile size for the tubing
tow_bar_length = 40.0
cross_bar_offset = 15.0 # Distance from center Y to cross bars
wheel_radius = 6.0
wheel_thickness = 4.0
mount_block_len = 10.0  # Length of the block holding the axle

# --- 1. Frame Construction ---

# Calculate offsets for side rails
# Center of side rail X = +/- (width/2 - tube/2)
side_rail_x = (frame_width - tube_size) / 2.0

# Create Side Rails (Longitudinal)
rail_left = cq.Workplane("XY").box(tube_size, frame_length, tube_size).translate((-side_rail_x, 0, 0))
rail_right = cq.Workplane("XY").box(tube_size, frame_length, tube_size).translate((side_rail_x, 0, 0))

# Calculate dimensions for cross rails (fitting between side rails)
inner_width = frame_width - 2 * tube_size
end_rail_y = (frame_length - tube_size) / 2.0

# Create End Rails (Front and Back)
rail_front = cq.Workplane("XY").box(inner_width, tube_size, tube_size).translate((0, end_rail_y, 0))
rail_back = cq.Workplane("XY").box(inner_width, tube_size, tube_size).translate((0, -end_rail_y, 0))

# Create Internal Cross Bars (defining the wheel bay)
cross_bar_front = cq.Workplane("XY").box(inner_width, tube_size, tube_size).translate((0, cross_bar_offset, 0))
cross_bar_back = cq.Workplane("XY").box(inner_width, tube_size, tube_size).translate((0, -cross_bar_offset, 0))

# Union the frame components
frame = rail_left.union(rail_right).union(rail_front).union(rail_back).union(cross_bar_front).union(cross_bar_back)

# --- 2. Tow Bar ---

# Calculate position: Extends from the center of the front face
tow_bar_y = frame_length / 2.0 + tow_bar_length / 2.0
tow_bar = cq.Workplane("XY").box(tube_size, tow_bar_length, tube_size).translate((0, tow_bar_y, 0))

# Add to result
result = frame.union(tow_bar)

# --- 3. Wheel Assembly ---

# Create Mounting Blocks (small blocks on inner side rails)
# Center X of block is shifted inwards from the side rail center by one tube width
block_x = side_rail_x - tube_size
mount_left = cq.Workplane("XY").box(tube_size, mount_block_len, tube_size).translate((-block_x, 0, 0))
mount_right = cq.Workplane("XY").box(tube_size, mount_block_len, tube_size).translate((block_x, 0, 0))

result = result.union(mount_left).union(mount_right)

# Create Wheels
# Wheels are cylinders oriented along X axis.
# We position the workplane at the inner face of the mounting blocks.
# Inner face of block = block center x - tube_size/2
wheel_start_plane_x = block_x - tube_size / 2.0

# Right Wheel: Plane at +X, extrude inwards (-X direction)
wheel_right = cq.Workplane("YZ", origin=(wheel_start_plane_x, 0, 0)).circle(wheel_radius).extrude(-wheel_thickness)

# Left Wheel: Plane at -X, extrude inwards (+X direction)
wheel_left = cq.Workplane("YZ", origin=(-wheel_start_plane_x, 0, 0)).circle(wheel_radius).extrude(wheel_thickness)

result = result.union(wheel_right).union(wheel_left)