import cadquery as cq

# Parametric dimensions
radius = 15
thickness = 3
hole_radius = 2.5
tab_radius = 5
tab_offset = radius - tab_radius

# Create the base circle
base = cq.Workplane("XY").circle(radius).extrude(thickness)

# Create the tab
tab = cq.Workplane("XY").workplane(offset=thickness).center(radius, 0).circle(tab_radius).extrude(thickness)

# Create the hole in the tab
hole = cq.Workplane("XY").workplane(offset=thickness).center(radius, 0).circle(hole_radius).extrude(thickness)

#Cut geometry
cut = cq.Workplane("XY").workplane(offset=thickness).moveTo(radius, tab_radius).lineTo(radius, -tab_radius).close().extrude(thickness)


# Union the base and tab
result = base.union(tab).cut(hole).cut(cut)