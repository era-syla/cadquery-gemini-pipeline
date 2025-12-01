import cadquery as cq

# Define parameters
outer_radius = 10
inner_radius = 4
thickness1 = 1
thickness2 = 0.5

# Create the base cylinder
base = cq.Workplane("XY").circle(outer_radius).extrude(thickness1)

# Create the hole
hole = cq.Workplane("XY").circle(inner_radius).extrude(thickness1)

# Subtract the hole from the base
result = base.cut(hole)

#Add the lip
lip = cq.Workplane("XY").circle(outer_radius).extrude(thickness2)
result = result.union(lip.translate((0, 0, thickness1)))
# Show the result
#cq.exporters.export(result,'result.stl')