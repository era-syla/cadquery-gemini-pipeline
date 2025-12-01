import cadquery as cq

# Parameters
cone_height = 15
cone_radius_bottom = 10
cone_radius_top = 5
num_cones = 3
z_offset = cone_height
top_hole_radius = 2

# Create the first cone
result = cq.Workplane("XY").add(cq.Solid.makeCone(cone_radius_bottom, cone_radius_top, cone_height))

# Stack the cones
for i in range(1, num_cones):
    cone = cq.Solid.makeCone(cone_radius_bottom, cone_radius_top, cone_height)
    translated_cone = cone.translate((0, 0, i * z_offset))
    result = result.union(translated_cone)

# Create the hole at the top
result = result.faces(">Z").workplane().circle(top_hole_radius).cutThruAll()