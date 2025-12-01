import cadquery as cq

# Parameters
base_width = 30.0
base_height = 10.0
button_diameter = 15.0
button_height = 8.0
neck_diameter = 12.0
neck_height = 5.0
hole_diameter = 4.0
hole_offset = 5.0

# Base
base = cq.Workplane("XY").box(base_width, base_width, base_height)

# Button
button = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(button_diameter / 2.0)
    .extrude(button_height)
)

# Neck
neck = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(neck_diameter / 2.0)
    .extrude(neck_height)
)


# Combine base, neck, and button
result = base.union(neck).union(button)

# Holes
hole_locations = [
    (-base_width / 2.0 + hole_offset, -base_width / 2.0 + hole_offset),
    (-base_width / 2.0 + hole_offset, base_width / 2.0 - hole_offset),
    (base_width / 2.0 - hole_offset, -base_width / 2.0 + hole_offset),
    (base_width / 2.0 - hole_offset, base_width / 2.0 - hole_offset),
]

for x, y in hole_locations:
    hole = (
        cq.Workplane("XY")
        .moveTo(x, y)
        .circle(hole_diameter / 2.0)
        .extrude(base_height)
    )
    result = result.cut(hole)