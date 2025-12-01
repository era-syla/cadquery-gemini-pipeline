import cadquery as cq

width = 50
height = 60
depth = 40
pipe_dia = 5
pipe_length = 15

# Create the main box
box = cq.Workplane("XY").box(width, depth, height)

# Create the roof overhang
roof_overhang = cq.Workplane("XY").workplane(offset=height).box(width + 5, depth + 5, 3)

# Add the roof ridge
roof_ridge = cq.Workplane("XY").workplane(offset=height + 3).circle(pipe_dia/2).extrude(width + 5)

# Create the pipe
pipe = cq.Workplane("YZ").workplane(offset=width/2).circle(pipe_dia/2).extrude(pipe_length)

# Combine all parts
result = box.union(roof_overhang).union(roof_ridge).union(pipe)