import cadquery as cq

# Parametric dimensions
base_radius = 10
base_height = 5
middle_radius = 12
middle_height = 7
top_radius = 8
top_height = 6

# Create the base cylinder
base = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# Create the middle truncated cone
middle = cq.Workplane("XY").workplane(offset=base_height).circle(middle_radius).extrude(middle_height)

# Create the top cylinder
top = cq.Workplane("XY").workplane(offset=base_height + middle_height).circle(top_radius).extrude(top_height)

# Fuse the parts together
result = base.union(middle).union(top)