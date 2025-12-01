import cadquery as cq

# Parameters
cube_size = 20.0
edge_radius = 2.0
hole_diameter = 4.0
hole_depth = 3.0
letter_thickness = 1.0
letter_depth = 0.5

# Create a cube with rounded edges
result = cq.Workplane("XY").box(cube_size, cube_size, cube_size).edges().fillet(edge_radius)

# Add holes for face with 2 holes
offset = cube_size / 4
result = result.faces(">Z").workplane().center(offset, offset).circle(hole_diameter/2).extrude(-hole_depth)
result = result.faces(">Z").workplane().center(-offset, -offset).circle(hole_diameter/2).extrude(-hole_depth)

# Add holes for face with 3 holes
offset = cube_size / 4
result = result.faces(">X").workplane().center(offset, offset).circle(hole_diameter/2).extrude(-hole_depth)
result = result.faces(">X").workplane().center(-offset, -offset).circle(hole_diameter/2).extrude(-hole_depth)
result = result.faces(">X").workplane().center(0, 0).circle(hole_diameter/2).extrude(-hole_depth)

# Add holes for face with 4 holes
offset = cube_size / 4
result = result.faces(">Y").workplane().center(offset, offset).circle(hole_diameter/2).extrude(-hole_depth)
result = result.faces(">Y").workplane().center(-offset, -offset).circle(hole_diameter/2).extrude(-hole_depth)
result = result.faces(">Y").workplane().center(offset, -offset).circle(hole_diameter/2).extrude(-hole_depth)
result = result.faces(">Y").workplane().center(-offset, offset).circle(hole_diameter/2).extrude(-hole_depth)

# Create the letters "CRT"
letter_height = 12.0
letter_offset = 2.0

# Define the letters as shapes
letters = (
    cq.Workplane("XY")
    .text("CRT", letter_height, -letter_depth, font="Arial", halign="center", valign="center")
)

# Position and subtract the letters
letters = letters.translate((0, 0, -cube_size/2 + letter_offset))
result = result.cut(letters)