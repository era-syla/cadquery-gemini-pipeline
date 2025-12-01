import cadquery as cq

# --- Dimensions & Parameters ---
# Estimated dimensions based on visual proportions
plate_width = 240.0
plate_height = 150.0
thickness = 3.0

# Feature positions relative to center (0,0)
# Right-side rectangular cutout
rect_w = 80.0
rect_h = 55.0
rect_center_x = 60.0
rect_center_y = 10.0
rect_mount_w = 90.0  # Width between mounting holes
rect_mount_h = 65.0  # Height between mounting holes

# Top-Left Gauge
gauge_x = -75.0
gauge_y = 35.0
gauge_dia = 36.0
gauge_mount_offset = 26.0  # Vertical distance for screw holes

# Mid-Left Switch
switch_x = -75.0
switch_y = -5.0
switch_dia = 12.0

# Bottom Row Components
bottom_row_y = -45.0
pot_dia = 18.0
pot_positions_x = [-75.0, -30.0, 15.0]

# Corner Mounting
corner_margin = 10.0
mount_x_offset = (plate_width / 2) - corner_margin
mount_y_offset = (plate_height / 2) - corner_margin

# --- Geometry Construction ---

# 1. Base Plate
result = cq.Workplane("XY").box(plate_width, plate_height, thickness)

# 2. Rectangular Cutout Assembly (Right)
# Main rectangular hole
result = (
    result.faces(">Z")
    .workplane()
    .center(rect_center_x, rect_center_y)
    .rect(rect_w, rect_h)
    .cutThruAll()
)

# Mounting holes for the rectangle
result = (
    result.faces(">Z")
    .workplane()
    .center(rect_center_x, rect_center_y)
    .rect(rect_mount_w, rect_mount_h, forConstruction=True)
    .vertices()
    .circle(2.0)  # M4 clearance approx
    .cutThruAll()
)

# 3. Top-Left Gauge Assembly
# Main large hole
result = (
    result.faces(">Z")
    .workplane()
    .center(gauge_x, gauge_y)
    .circle(gauge_dia / 2)
    .cutThruAll()
)

# Gauge mounting screw holes (Top and Bottom)
result = (
    result.faces(">Z")
    .workplane()
    .center(gauge_x, gauge_y)
    .pushPoints([(0, gauge_mount_offset), (0, -gauge_mount_offset)])
    .circle(2.0)
    .cutThruAll()
)

# 4. Mid-Left Switch Hole
result = (
    result.faces(">Z")
    .workplane()
    .center(switch_x, switch_y)
    .circle(switch_dia / 2)
    .cutThruAll()
)

# 5. Bottom Row Holes (Potentiometers/Switches)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(x, bottom_row_y) for x in pot_positions_x])
    .circle(pot_dia / 2)
    .cutThruAll()
)

# 6. Corner Mounting Holes
# Top Corners (Simple circular holes)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-mount_x_offset, mount_y_offset), (mount_x_offset, mount_y_offset)])
    .circle(2.5)  # approx 5mm diameter
    .cutThruAll()
)

# Bottom Corners (Keyhole slots)
# We construct a keyhole shape solid and cut it from the main body
def create_keyhole_cutter(x_pos, y_pos):
    # Keyhole parameters
    large_r = 4.0
    small_r = 2.5
    slot_length = 6.0
    
    # Create the large circle
    large_circle = (
        cq.Workplane("XY")
        .center(x_pos, y_pos)
        .circle(large_r)
        .extrude(thickness * 2)
    )
    
    # Create the small circle
    small_circle = (
        cq.Workplane("XY")
        .center(x_pos, y_pos + slot_length)
        .circle(small_r)
        .extrude(thickness * 2)
    )
    
    # Create the connecting rectangle
    rect_connector = (
        cq.Workplane("XY")
        .center(x_pos, y_pos + slot_length/2)
        .rect(small_r * 2, slot_length)
        .extrude(thickness * 2)
    )
    
    # Union all parts and translate
    profile = large_circle.union(small_circle).union(rect_connector)
    return profile.translate((0, 0, -thickness/2))

# Generate and apply keyhole cuts
keyhole_left = create_keyhole_cutter(-mount_x_offset, -mount_y_offset)
keyhole_right = create_keyhole_cutter(mount_x_offset, -mount_y_offset)

result = result.cut(keyhole_left).cut(keyhole_right)

# Final Result
# result is ready