import cadquery as cq

width = 50
height = 20
depth = 30
finger_width = 5
finger_count = 5
gap = 2

# Create a function to generate the finger part
def create_finger_part(width, height, depth, finger_width, finger_count, gap):
    finger_total_width = (finger_count * finger_width) + ((finger_count - 1) * gap)
    base_width = width + (2 * depth)
    base_length = finger_total_width + (2 * depth)

    base = cq.Workplane("XY").box(base_length, base_width, height)

    cut_width = base_length
    cut_length = finger_width
    cut_height = height
    
    cut_part = cq.Workplane("XY").box(cut_length, width, height).translate((depth, 0, 0))

    result = base
    for i in range(finger_count):
        x_offset = i * (finger_width + gap)
        result = result.cut(cq.Workplane("XY").box(cut_length, width, height).translate((depth + x_offset, 0, 0)))

    result = result.cut(cq.Workplane("XY").box(base_length, width+depth, height).translate((0, width-depth, 0)))

    return result

# Create the first finger part
finger_part_1 = create_finger_part(width, height, depth, finger_width, finger_count, gap)

# Create the second finger part and rotate it
finger_part_2 = create_finger_part(width, height, depth, finger_width, finger_count, gap).rotate((0, 0, 0), (0, 0, 1), 180).translate((0, width*2, 0))

# Create the connecting beams
beam_width = 5
beam_height = 5
beam_length = width + (2 * depth) - (finger_width+depth)/2

beam1 = cq.Workplane("XY").box(beam_length, beam_width, beam_height) \
    .translate(((width + depth - beam_length)/2, width-depth/2, 0))

beam2 = cq.Workplane("XY").box(beam_length, beam_width, beam_height) \
    .translate(((width + depth - beam_length)/2, width-depth/2, 0)) \
    .rotate((0, 0, 0), (0, 0, 1), 180).translate((0, width*2, 0))

# Combine all parts
result = finger_part_1.union(finger_part_2).union(beam1).union(beam2)