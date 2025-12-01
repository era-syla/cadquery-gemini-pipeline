import cadquery as cq

width = 100
length = 150
thickness = 5
hinge_width = 20
hinge_height = 10
hinge_length = 25
lid_angle = 45

# Base
base = cq.Workplane("XY").box(length, width, thickness)

# Lid
lid = cq.Workplane("XY").box(length, width, thickness)

# Hinge
hinge = cq.Workplane("XY").box(hinge_length, hinge_width, hinge_height)

# Positioning
base = base.translate((0, 0, 0))
lid = lid.translate((length/2 - hinge_length/2, 0, hinge_height))
lid = lid.rotate((0, 0, 1), (0, 0, 0), lid_angle)
hinge = hinge.translate((length/2 - hinge_length/2, 0, thickness))

# Combine
result = base.union(lid).union(hinge)

# Add a border to the base
border_width = 3
base_with_border = (
    cq.Workplane("XY")
    .center(0, 0).rect(length + border_width, width + border_width)
    .extrude(thickness/2)
    .faces(">Z")
    .workplane()
    .center(0, 0).rect(length - border_width, width - border_width)
    .cutThruAll()
    .translate((0, 0, thickness/2))
)

base = base_with_border.translate((0, 0, -thickness/2))

# Combine
result = base.union(lid).union(hinge)