import cadquery as cq

# Parameters for the geometry
outer_radius = 22.0
inner_radius = 19.5
cyl_height = 18.0
base_height = 2.5
wing_span = 70.0  # Total width across wings
wing_width = 24.0 # Width of the strap loops
boss_radius = 3.0
boss_hole_dia = 2.5
slot_length = 20.0
slot_width = 3.5

# 1. Create the Base
# The base is a union of the central circular footprint and the rectangular wings.
base = (
    cq.Workplane("XY")
    .rect(wing_span, wing_width)
    .extrude(base_height)
)

circle_part = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_height)
)

base = base.union(circle_part)

# Fillet the corners
base = base.edges("|Z").fillet(1.5)

# Cut the strap slots in the wings
# Positioned symmetrically along the X-axis
slot_offset = 26.0
base = (
    base.faces(">Z").workplane()
    .pushPoints([(slot_offset, 0), (-slot_offset, 0)])
    .slot2D(slot_length, slot_width, angle=90)
    .cutThruAll()
)

# 2. Create the Main Cylinder Body
# A hollow cylinder sitting on top of the base
body = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(cyl_height)
)

# Combine base and body
result = base.union(body)

# 3. Internal Mounting Bosses
# Located along the X-axis, merged with the inner wall
boss_offset = inner_radius - boss_radius
bosses = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .pushPoints([(boss_offset, 0), (-boss_offset, 0)])
    .circle(boss_radius)
    .extrude(cyl_height - 2.0)
)

# Union bosses to the main body
result = result.union(bosses)

# Cut mounting holes in the bosses
result = (
    result.faces(">Z").workplane()
    .pushPoints([(boss_offset, 0), (-boss_offset, 0)])
    .hole(boss_hole_dia)
)

# 4. Internal Rib
# A stiffening rib running along the floor (X-axis) connecting the area between bosses
rib = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .rect(boss_offset * 2, 2.0)
    .extrude(2.0)
)
result = result.union(rib)

# 5. Features and Cutouts

# Side Window (Rectangular cutout on the Right/+X side)
# We cut from the YZ plane inwards
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=outer_radius + 5)
    .center(0, base_height + 5.0)
    .rect(12.0, 6.0)
    .extrude(-10.0)
)

# Front Slot (Vertical slot on the Front/-Y side)
# Modeled as a slot shape cut from the XZ plane
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=-outer_radius - 5)
    .center(0, base_height + 3.0)
    .slot2D(8.0, 4.0, angle=90)
    .extrude(10.0)
)

# Top Rim Notch (Small relief on the top edge, Front/-Y side)
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=-outer_radius - 5)
    .center(0, base_height + cyl_height)
    .rect(4.0, 3.0)
    .extrude(10.0)
)