import cadquery as cq

# Parametric dimensions
width = 50.0
height = 30.0
length = 80.0
base_height = 10.0
groove_width = 10.0
groove_depth = 5.0
hole_diameter = 5.0
hole_offset = 15.0
small_box_height = 10.0
small_box_width = 20.0
small_box_length = 50.0
small_box_offset = 5.0


# Create the base
base = cq.Workplane("XY").box(width, length, base_height)

# Create the main body
main_body = cq.Workplane("XY").box(width, length, height).translate((0, 0, base_height))

# Create the groove
groove = cq.Workplane("XY").box(groove_width, length, groove_depth).translate((0, 0, base_height))

# Create the small box on top
small_box = cq.Workplane("XY").box(small_box_width, small_box_length, small_box_height).translate((0, 0, height + base_height))
cut_box = cq.Workplane("XY").box(small_box_width - 1, small_box_length - 10, small_box_height + 1).translate((0, -5, height + base_height -1 ))


# Create the holes
hole1 = cq.Workplane("XY").circle(hole_diameter / 2).extrude(height + base_height).translate((width / 4, length / 2, 0))
hole2 = cq.Workplane("XY").circle(hole_diameter / 2).extrude(height + base_height).translate((width / 4 - width / 2, length / 2 - length / 2, 0))

hole3 = cq.Workplane("XZ").circle(hole_diameter / 2).extrude(width).translate((-width / 2, height + base_height - small_box_height / 2, length / 2))
hole4 = cq.Workplane("XZ").circle(hole_diameter / 2).extrude(width).translate((-width / 2, height + base_height + small_box_height / 2, length / 2))

# Combine the parts
result = (
    base
    .union(main_body)
    .cut(groove)
    .union(small_box)
    .cut(cut_box)
    .cut(hole1)
    .cut(hole2)
    .cut(hole3)
    .cut(hole4)
)