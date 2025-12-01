import cadquery as cq

# --- Parameters ---
height = 12.0           # Thickness of the part (Z direction)
inner_radius = 16.0     # Inner radius of the central arc
wall_thickness = 8.0    # Thickness of the curved section
outer_radius = inner_radius + wall_thickness

leg_length = 22.0       # Length of the straight leg sections
inner_step = 2.0        # Offset for the wider opening between legs

# Right Leg Parameters (Hole and Chamfer)
hole_diameter = 6.0
hole_dist_from_end = 8.0
chamfer_size = 5.0

# Left Leg Parameters (C-Slot)
slot_radius = 3.5
slot_opening_width = 4.0
slot_dist_from_end = 8.0

# --- Geometry Construction ---

# 1. Define the main profile sketch
# Coordinates: Center of arc is (0,0). Y is up. Legs extend in -Y.
# Right leg X range: [inner_radius + inner_step, outer_radius]
# Left leg X range:  [-outer_radius, -(inner_radius + inner_step)]

leg_inner_x = inner_radius + inner_step

# Points for the right side
p_r_inner_start = (inner_radius, 0)
p_r_step = (leg_inner_x, 0)
p_r_inner_end = (leg_inner_x, -leg_length)
p_r_outer_end = (outer_radius, -leg_length)
p_r_outer_start = (outer_radius, 0)

# Points for the left side (mirrored)
p_l_outer_start = (-outer_radius, 0)
p_l_outer_end = (-outer_radius, -leg_length)
p_l_inner_end = (-leg_inner_x, -leg_length)
p_l_step = (-leg_inner_x, 0)
p_l_inner_start = (-inner_radius, 0)

# Create the base solid
base = (
    cq.Workplane("XY")
    .moveTo(*p_r_inner_start)
    .lineTo(*p_r_step)
    .lineTo(*p_r_inner_end)
    .lineTo(*p_r_outer_end)
    .lineTo(*p_r_outer_start)
    .threePointArc((0, outer_radius), p_l_outer_start)  # Outer Arc
    .lineTo(*p_l_outer_end)
    .lineTo(*p_l_inner_end)
    .lineTo(*p_l_step)
    .lineTo(*p_l_inner_start)
    .threePointArc((0, inner_radius), p_r_inner_start)  # Inner Arc
    .close()
    .extrude(height)
)

# 2. Add Right Leg Features
# Chamfer the outer corner at the end of the right leg
# Select the vertical edge closest to the outer corner point
base = base.edges("|Z").edges(cq.selectors.NearestToPointSelector((outer_radius, -leg_length, height/2))).chamfer(chamfer_size)

# Create the hole in the right leg (Axis along X)
hole_y = -leg_length + hole_dist_from_end
hole_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=outer_radius + 5)  # Offset to outside right
    .moveTo(hole_y, height/2)            # Local coordinates (Y_global, Z_global)
    .circle(hole_diameter / 2)
    .extrude(-(outer_radius * 2 + 10))   # Cut through the part towards -X
)
base = base.cut(hole_cutter)

# 3. Add Left Leg Features (Slot)
# Calculate position for the slot center
slot_y = -leg_length + slot_dist_from_end
slot_x = -(leg_inner_x + outer_radius) / 2  # Center of the left leg width

# Create the keyhole/slot cutter
# Union of a circle and a rectangle extending to the tip
slot_circle = (
    cq.Workplane("XY")
    .moveTo(slot_x, slot_y)
    .circle(slot_radius)
    .extrude(height)
)

# Rectangle to open the slot to the end
# Centered rect moved down so its top aligns with circle center
rect_len = 20.0
slot_channel = (
    cq.Workplane("XY")
    .moveTo(slot_x, slot_y - rect_len/2) 
    .rect(slot_opening_width, rect_len)
    .extrude(height)
)

result = base.cut(slot_circle).cut(slot_channel)