import cadquery as cq

# Parameters
length = 100
width = 20
height = 2
hole_size = 8
hole_spacing = 16
num_holes = 6

# Create the base plate
result = cq.Workplane("XY").box(length, width, height)

# Create the holes
for i in range(num_holes):
    x_pos = (i - (num_holes - 1) / 2) * hole_spacing
    result = result.cut(cq.Workplane("XY").center(x_pos, 0).rect(hole_size, hole_size).extrude(height + 1).translate((0, 0, -(height + 1) / 2)))