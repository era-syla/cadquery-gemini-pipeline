import cadquery as cq

radius = 1
height = 5

result = cq.Workplane("XY").circle(radius).extrude(height)