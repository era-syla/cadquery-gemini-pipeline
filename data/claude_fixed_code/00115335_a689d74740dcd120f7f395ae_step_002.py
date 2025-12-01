import cadquery as cq

# Parameters
length = 100
width = 30
height = 20
wall_thickness = 3
circle_radius = 7
angle = 30
segment_length = 30

# Create the base rectangular prism
base = cq.Workplane("XY").box(length, width, height)

# Create the angled segment
angled_segment = cq.Workplane("XY").box(segment_length, width, height)

# Rotate the angled segment
angled_segment = angled_segment.rotate((0, 0, 0), (0, 0, 1), angle)

# Create the second segment
segment2 = cq.Workplane("XY").box(length, width, height)

# Translate the second segment
segment2 = segment2.translate((0, width * 2, 0))
# Translate the angled segment to the end of the base
angled_segment = angled_segment.translate((length / 2, width / 2, 0))


# Create the Y-shape by unioning the base and angled segment
y_shape = base.union(angled_segment).union(segment2)

# Remove material to create the channel
cut_height = height - wall_thickness
cut_width = width - 2 * wall_thickness

cut_base = cq.Workplane("XY").box(length, cut_width, cut_height).translate((0, 0, wall_thickness))
cut_angled_segment = cq.Workplane("XY").box(segment_length, cut_width, cut_height).translate((0, 0, wall_thickness))
cut_segment2 = cq.Workplane("XY").box(length, cut_width, cut_height).translate((0, 0, wall_thickness)).translate((0, width * 2, 0))

cut_angled_segment = cut_angled_segment.rotate((0, 0, 0), (0, 0, 1), angle)
cut_angled_segment = cut_angled_segment.translate((length / 2, width / 2, 0))

cut_shape = cut_base.union(cut_angled_segment).union(cut_segment2)


# Create the hole
hole = cq.Workplane("XY").circle(circle_radius).extrude(height)
hole = hole.translate((length / 2, width / 2, 0))
# Subtract the cut from the Y-shape
result = y_shape.cut(cut_shape).cut(hole)