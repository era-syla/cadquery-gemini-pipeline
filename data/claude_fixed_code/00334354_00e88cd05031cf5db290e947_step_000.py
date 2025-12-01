import cadquery as cq

# Parameters for dimensions
box_length = 30.0
box_width = 20.0
box_height = 20.0
cylinder_radius = 8.0
cylinder_extrusion = 5.0

# Create the main rectangular body
# box() creates a cube centered at the origin
result = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create the cylindrical protrusion
# Select the face in the positive X direction, create a workplane on it,
# draw a circle, and extrude it outwards
result = (
    result
    .faces(">X")
    .workplane()
    .circle(cylinder_radius)
    .extrude(cylinder_extrusion, combine=True)
)