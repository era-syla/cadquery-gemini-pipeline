import cadquery as cq

# Parameters
nut_width = 10.0
nut_height = 6.0
thread_diameter = 6.0
thread_pitch = 1.0
washer_diameter = 15.0
washer_height = 2.0
chamfer_size = 1.0

# Create the basic nut shape
nut = cq.Workplane("XY").polygon(6, nut_width).extrude(nut_height)

# Chamfer the edges
nut = nut.edges("|Z").chamfer(chamfer_size)

# Create the central hole
nut = nut.faces(">Z").workplane().hole(thread_diameter)

# Create the washer
washer = cq.Workplane("XY").circle(washer_diameter / 2.0).extrude(washer_height)

# Position and add the washer to the nut
washer = washer.translate((0, 0, nut_height))
result = nut.union(washer)

# Add thread (simplified, just a visual representation)
# helical_cut = cq.Workplane("XY").circle(thread_diameter/2).extrude(nut_height, taper=thread_pitch)
# result = result.cut(helical_cut)

# Show the result
# cq.exporters.export(result,'nut.stl') # uncomment to export to STL