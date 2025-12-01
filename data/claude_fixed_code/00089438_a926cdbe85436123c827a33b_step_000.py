import cadquery as cq

# Parametric dimensions
base_length = 60
base_width = 20
base_height = 10
top_length = 20
top_width = 20
top_height = 30
hole_diameter = 5
large_hole_diameter = 10

# Create the base
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Create the top
top = cq.Workplane("XY").workplane(offset=base_height).moveTo(0,0).lineTo(top_length,0).lineTo(0,top_width).close().extrude(top_height)

# Join the base and top
result = base.union(top.translate((0, -base_width/2 + top_width/2, 0)))

# Create holes in the base
hole_locations = [
    (-base_length * 0.25, 0),
    (0, 0),
    (base_length * 0.25, 0)
]

for loc in hole_locations:
    result = result.faces(">Z").workplane().moveTo(loc[0], loc[1]).hole(hole_diameter)

# Create holes in the top
result = result.faces(">Z").workplane().moveTo(top_length * 0.3, 0).hole(hole_diameter)
result = result.faces(">Z").workplane().moveTo(0, top_width * 0.3).circle(large_hole_diameter/2).cutThruAll()