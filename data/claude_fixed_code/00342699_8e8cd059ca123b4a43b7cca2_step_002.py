import cadquery as cq

width = 30
height = 80
thickness = 5
base_height = 20
base_width = width + 2 * thickness
hole_diameter = 5
hole_spacing = 10
hole_count = 3

# Create main box
result = cq.Workplane("XY").box(width, height, thickness)

# Create base structure
base = (
    cq.Workplane("XY")
    .box(base_width, base_height, thickness)
    .translate((0, -base_height / 2, -thickness))
)

result = result.union(base)

# Add bottom extrusion
bottom_extrude = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(-thickness)
    .translate((0, -base_height / 2, -thickness))
)

result = result.union(bottom_extrude)

# Add cylindrical feature
cylinder = (
    cq.Workplane("XY")
    .circle(base_width / 2 - thickness / 2)
    .extrude(base_height / 2)
    .translate((0, -base_height / 2, 0))
)

result = result.union(cylinder)

# Create holes
for i in range(hole_count):
    x_pos = -(hole_spacing * (hole_count - 1) / 2) + i * hole_spacing
    y_pos = height / 2
    hole = (
        cq.Workplane("XY")
        .workplane(offset=thickness / 2)
        .center(x_pos, y_pos)
        .circle(hole_diameter / 2)
        .extrude(-thickness)
    )
    result = result.cut(hole)