import cadquery as cq

# -- Dimensions and Parameters --
thickness = 5.0
radius_top = 8.5
radius_mid = 13.0
radius_corner = 11.0
radius_leg = 8.5

dia_small_hole = 5.0
dia_large_hole = 6.5

# -- Coordinates --
# Vertical section (aligned roughly with Y axis)
pt_top = (0, 95)
pt_upper_hole = (0, 80) # Hole only, width interpolated
pt_mid = (0, 45)
pt_corner = (0, 0)

# Angled leg section
pt_leg = (40, -15)

# -- Geometry Construction --

# 1. Vertical Section
# Created by hulling circles at the key points to form the tapered profile
vert_solid = (
    cq.Workplane("XY")
    .moveTo(*pt_corner).circle(radius_corner).extrude(thickness)
    .union(cq.Workplane("XY").moveTo(*pt_mid).circle(radius_mid).extrude(thickness))
    .union(cq.Workplane("XY").moveTo(*pt_top).circle(radius_top).extrude(thickness))
)

# 2. Leg Section
# Created by hulling the corner circle and the leg tip circle
leg_solid = (
    cq.Workplane("XY")
    .moveTo(*pt_corner).circle(radius_corner).extrude(thickness)
    .union(cq.Workplane("XY").moveTo(*pt_leg).circle(radius_leg).extrude(thickness))
)

# 3. Combine Solids
# Union the two parts to handle the corner transition smoothly
base_shape = vert_solid.union(leg_solid)

# 4. Create Holes
# Group hole locations by size
small_holes = [pt_top, pt_upper_hole]
large_holes = [pt_mid, pt_corner, pt_leg]

# Cut the holes through the base shape
result = (
    base_shape
    .faces(">Z").workplane()
    .pushPoints(small_holes).hole(dia_small_hole)
    .pushPoints(large_holes).hole(dia_large_hole)
)