import cadquery as cq

# Parametric dimensions
length = 100.0
width = 20.0
height = 10.0
wall_thickness = 2.0
end_piece_width = 15.0
end_piece_height = 15.0
cutout_length = 30.0
cutout_width = 10.0

# Create the base
base = cq.Workplane("XY").box(length, width, height)

# Create the walls
wall = cq.Workplane("XY").box(length, width - 2 * wall_thickness, height - wall_thickness)

# Cut out the inside
base = base.cut(wall.translate((0, 0, wall_thickness)))

# Create the end pieces
end_piece1 = cq.Workplane("XY").box(end_piece_width, width, end_piece_height)
end_piece2 = cq.Workplane("XY").box(end_piece_width, width, end_piece_height).translate((length - end_piece_width, 0, 0))

# Add the end pieces to the base
base = base.union(end_piece1.translate((-(length/2 - end_piece_width/2), 0, (end_piece_height - height)/2)))
base = base.union(end_piece2.translate(((length/2 - end_piece_width/2), 0, (end_piece_height - height)/2)))

# Create the cutout
cutout = cq.Workplane("XY").box(cutout_length, cutout_width, height)

# Cut out the middle
base = base.cut(cutout)

result = base