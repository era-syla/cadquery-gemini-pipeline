import cadquery as cq

# Dimensions based on standard LEGO brick geometry (2x4)
length = 32.0       # 4 units * 8mm
width = 16.0        # 2 units * 8mm
height = 9.6        # Standard brick height
stud_diam = 4.8     # Standard stud diameter
stud_height = 1.7   # Standard stud height
hole_diam = 3.0     # Estimated diameter for the central holes

# 1. Create the base block
# The box is centered at (0,0,0), so the top face is at Z = height/2
result = cq.Workplane("XY").box(length, width, height)

# 2. Create the studs
# We generate them as a separate solid and union them to avoid face selection issues.
# Grid 4x2, Spacing 8mm
studs = (
    cq.Workplane("XY")
    .workplane(offset=height / 2.0)
    .rarray(8.0, 8.0, 4, 2)
    .circle(stud_diam / 2.0)
    .extrude(stud_height)
)

result = result.union(studs)

# 3. Create and cut the holes
# These are located along the centerline, between the columns of studs.
# Grid 3x1 (3 holes), Spacing 8mm
cutouts = (
    cq.Workplane("XY")
    .workplane(offset=height / 2.0)
    .rarray(8.0, 1.0, 3, 1)
    .circle(hole_diam / 2.0)
    .extrude(-height)
)

result = result.cut(cutouts)