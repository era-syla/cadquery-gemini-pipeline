import cadquery as cq

# --- Parametric Dimensions ---
length = 60.0
width = 30.0
base_height = 12.0
total_height = 32.0

# Features
jaw_len = 28.0           # Length of the raised back section
jaw_overhang_len = 10.0  # Length of the overhang tip
undercut_start_x = 16.0  # X position where the curved undercut begins
tip_underside_h = 24.0   # Z height of the underside of the overhang

# Hole
hole_dist_from_back = 45.0
hole_dia = 6.6
cbore_dia = 12.0
cbore_depth = 4.0

# Groove
groove_width = 12.0
groove_depth = 2.0

# --- Geometry Construction ---

# 1. Base Block
# Create the main rectangular base. 
# Origin is at the back-center-bottom (X=0, Y=0, Z=0).
result = cq.Workplane("XY").box(length, width, base_height, centered=(False, True, False))

# 2. Upper Block (Jaw)
# Create the taller block at the back and unite it with the base.
upper_block = (
    cq.Workplane("XY")
    .box(jaw_len, width, total_height - base_height, centered=(False, True, False))
    .translate((0, 0, base_height))
)
result = result.union(upper_block)

# 3. Curved Undercut
# Create a sketch on the side plane to cut away the material under the overhang.
# We define a "cutter" shape that represents the void to be removed.
# The profile is roughly triangular with a curved hypotenuse.

# Points for the cutter profile
p1 = (undercut_start_x, base_height)      # Start of curve on the shelf
p2 = (jaw_len, base_height)               # Corner inside the block (to be removed)
p3 = (jaw_len, tip_underside_h)           # Underside of the tip vertical face

# Calculate a midpoint for the arc to ensure it bulges correctly (creating a concave cut)
# Midpoint of chord p1-p3
chord_mid_x = (p1[0] + p3[0]) / 2
chord_mid_y = (p1[1] + p3[1]) / 2
# Offset midpoint towards p2 to make the cutter convex (bulging out), 
# which results in a concave surface on the part.
arc_mid = (chord_mid_x + 3.0, chord_mid_y - 3.0)

cutter = (
    cq.Workplane("XZ")
    .moveTo(p1[0], p1[1])
    .lineTo(p2[0], p2[1])
    .lineTo(p3[0], p3[1])
    .threePointArc(arc_mid, p1) # Arc connecting p3 back to p1
    .close()
    .extrude(width, both=True) # Extrude wider than the part to ensure full cut
)

result = result.cut(cutter)

# 4. Counterbored Hole
# Place the hole on the top face of the base (the shelf).
result = (
    result.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .workplane(offset=-(total_height - base_height))
    .center(-length / 2 + hole_dist_from_back, 0)
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
)

# 5. Bottom Groove
# Cut the rectangular slot running along the bottom.
groove_cutter = (
    cq.Workplane("XY")
    .center(length / 2, 0)
    .rect(length + 5.0, groove_width) # Extra length to ensure clean cut at ends
    .extrude(groove_depth)
)

result = result.cut(groove_cutter)