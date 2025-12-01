import cadquery as cq

width = 40
height = 80
depth = 30
panel_width = 5

result = cq.Workplane("XY").box(width, depth, height)