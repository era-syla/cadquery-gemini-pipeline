import cadquery as cq

# Parameters
bottom_radius = 5
top_radius = 1
height = 50
top_cylinder_radius = 0.5
top_cylinder_height = 5

# Create the frustum
frustum = cq.Workplane("XY").circle(bottom_radius).workplane(offset=height).circle(top_radius).loft()

# Create the top cylinder
top_cylinder = cq.Workplane("XY").circle(top_cylinder_radius).extrude(top_cylinder_height)

# Move the top cylinder to the top of the frustum
top_cylinder = top_cylinder.translate((0, 0, height))

# Combine the frustum and the top cylinder
result = frustum.union(top_cylinder)