import cadquery as cq

# Parametric dimensions
width = 10
height = 10
length = 80
hole_diameter = 4.8
hole_spacing = 15
num_holes = 6
end_radius = width / 2
slot_width = 2
slot_depth = 2

# Create the base block
result = cq.Workplane("XY").box(length, width, height)

# Add rounded ends
result = result.faces("<X").workplane().center(0, 0).circle(end_radius).extrude(width/2)
result = result.faces(">X").workplane().center(0, 0).circle(end_radius).extrude(width/2)

# Create the holes
for i in range(num_holes):
    x_pos = -length / 2 + width / 2 + i * hole_spacing
    result = result.faces(">Z").workplane().center(x_pos+hole_spacing/2, 0).circle(hole_diameter / 2).cutThruAll()
    result = result.faces(">Z").workplane().center(x_pos+hole_spacing/2, 0).rect(slot_width, slot_width).cutBlind(slot_depth)