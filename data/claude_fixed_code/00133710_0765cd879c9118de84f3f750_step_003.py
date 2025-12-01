import cadquery as cq

# Define parameters
width = 10
height = 100
thickness = 2
hole_diameter = 0.5
hole_spacing = 5

# Create the base plate
result = cq.Workplane("XY").box(width, height, thickness)

# Create the holes
num_holes = int(height / hole_spacing)

for i in range(num_holes):
    y_pos = -height/2 + hole_spacing/2 + i * hole_spacing
    result = result.faces(">Z").workplane().moveTo(0, y_pos).circle(hole_diameter/2).cutThruAll()