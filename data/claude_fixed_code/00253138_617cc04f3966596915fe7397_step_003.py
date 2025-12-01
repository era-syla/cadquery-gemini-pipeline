import cadquery as cq

# --- Parameters ---
pitch = 5.08
num_poles = 8
length = num_poles * pitch + 2.0
base_depth = 12.0
base_height = 10.0
top_depth = 8.0
top_height = 5.0
hole_dia = 3.5
cutout_depth = 1.5
cutout_height = 5.0

# --- Geometry Construction ---

# 1. Base Block
base = cq.Workplane("XY").box(length, base_depth, base_height, centered=(True, True, False))

# 2. Top Block
top_offset_y = (base_depth - top_depth) / 2.0

top = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(0, top_offset_y)
    .box(length, top_depth, top_height, centered=(True, True, False))
)

# Combine base and top
result = base.union(top)

# 3. Top Holes
x_positions = [(i - (num_poles - 1) / 2) * pitch for i in range(num_poles)]

for x_pos in x_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x_pos, top_offset_y)
        .hole(hole_dia, depth=top_height + 2.0)
    )

# 4. Front Cutouts
side_slot_width = 2 * pitch - 2.5
center_slot_width = 4 * pitch - 2.5
side_slot_x_offset = 3 * pitch

def cut_front_slot(workplane, x_pos, width):
    return (
        workplane
        .faces("<Y")
        .workplane(centerOption="CenterOfBoundBox")
        .center(x_pos, 0)
        .rect(width, cutout_height)
        .cutBlind(-cutout_depth)
    )

result = cut_front_slot(result, -side_slot_x_offset, side_slot_width)
result = cut_front_slot(result, 0, center_slot_width)
result = cut_front_slot(result, side_slot_x_offset, side_slot_width)

# 5. Finishing Touches
result = result.edges("|Z").chamfer(0.4)