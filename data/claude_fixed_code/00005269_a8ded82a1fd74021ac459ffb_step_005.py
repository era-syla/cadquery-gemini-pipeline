import cadquery as cq

# Object parameters estimated from the image
base_width = 30.0
top_width = 22.0
height = 12.0
vertical_corner_radius = 4.0
top_edge_fillet_radius = 1.0

result = (
    cq.Workplane("XY")
    # 1. Define the base rounded rectangle
    .rect(base_width, base_width)
    .extrude(0.001)
    .faces(">Z")
    .workplane()
    .vertices()
    .circle(vertical_corner_radius)
    .extrude(0.001)
)

base = (
    cq.Workplane("XY")
    .rect(base_width, base_width)
    .extrude(0.001)
)

top = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .rect(top_width, top_width)
    .extrude(0.001)
)

result = (
    cq.Workplane("XY")
    .rect(base_width, base_width)
    .workplane(offset=height)
    .rect(top_width, top_width)
    .loft(combine=True)
    .edges("|Z")
    .fillet(vertical_corner_radius)
    .faces(">Z")
    .edges()
    .fillet(top_edge_fillet_radius)
)