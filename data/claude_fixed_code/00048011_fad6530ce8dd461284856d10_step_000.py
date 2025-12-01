import cadquery as cq

# Object Dimensions
width = 60.0             # Total width (X axis)
depth = 45.0             # Total depth (Y axis)
height = 35.0            # Total height (Z axis)

back_wall_thick = 15.0   # Thickness of the taller back wall
side_wall_height = 20.0  # Height of the side arm rests
side_wall_thick = 15.0   # Width of the side arm rests
base_thick = 8.0         # Thickness of the floor connecting the arms

# Derived Dimensions
front_length = depth - back_wall_thick
pocket_width = width - (2 * side_wall_thick)

# 1. Create the Main Block
# Start with a solid block representing the maximum bounding box
# Positioned centered in X and Y, with Z starting at 0
result = cq.Workplane("XY").box(width, depth, height, centered=(True, True, False))

# 2. Cut the Front Step
# Remove material from the front section to create the lower height of the arms.
# We cut from side_wall_height up to total height.
# We add a small overlap (cut_extension) to ensure the cut clears the front face clean.
cut_extension = 1.0
cut_length = front_length + cut_extension
cut_y_pos = (depth / 2) - back_wall_thick - (cut_length / 2)

step_cutter = (
    cq.Workplane("XY")
    .center(0, cut_y_pos)
    .box(width, cut_length, height - side_wall_height, centered=(True, True, False))
    .translate((0, 0, side_wall_height))
)

result = result.cut(step_cutter)

# 3. Cut the Center Pocket
# Remove material between the side arms, leaving the base floor.
# We cut from base_thick up to side_wall_height.
pocket_height = side_wall_height - base_thick

pocket_cutter = (
    cq.Workplane("XY")
    .center(0, cut_y_pos)
    .box(pocket_width, cut_length, pocket_height, centered=(True, True, False))
    .translate((0, 0, base_thick))
)

result = result.cut(pocket_cutter)