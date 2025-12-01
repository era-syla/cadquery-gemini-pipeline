import cadquery as cq

# Parametric dimensions
base_width = 50
base_length = 80
base_height = 10
cyl_outer_dia = 30
cyl_inner_dia = 15
cyl_height = 25
hole_dia = 4
hole_offset = 15
corner_radius = 5

# Create the base
base = cq.Workplane("XY").box(base_width, base_length, base_height).edges("|Z and <X").fillet(corner_radius)

# Create the cylinder
cylinder = cq.Workplane("XY").center(0, -base_width/2 + cyl_outer_dia/2).circle(cyl_outer_dia/2).extrude(cyl_height)
cylinder = cylinder.faces(">Z").workplane().circle(cyl_inner_dia/2).cutThruAll()

# Combine the base and cylinder
result = base.union(cylinder)

# Create the cut
cut_wp = cq.Workplane("XY").workplane(offset=base_height)
cut_wp = cut_wp.center(0, -base_width/2 + cyl_outer_dia/2)
cut_wp = cut_wp.moveTo(-cyl_outer_dia/2, -cyl_height/2)
cut_wp = cut_wp.lineTo(0, cyl_height/2)
cut_wp = cut_wp.lineTo(cyl_outer_dia/2, -cyl_height/2)
cut_wp = cut_wp.close()
cut = cut_wp.extrude(-base_width)

result = result.cut(cut)

# Create the holes
hole_center1 = (-base_width/2 + hole_offset, base_length/2 - hole_offset)
hole_center2 = (base_width/2 - hole_offset, base_length/2 - hole_offset)

result = result.faces(">Z").workplane().center(hole_center1[0], hole_center1[1]).circle(hole_dia/2).cutThruAll()
result = result.faces(">Z").workplane().center(hole_center2[0], hole_center2[1]).circle(hole_dia/2).cutThruAll()