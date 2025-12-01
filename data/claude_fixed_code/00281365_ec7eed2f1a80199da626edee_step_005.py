import cadquery as cq

# Parameters
width = 50.0
height = 50.0
thickness = 30.0
bulge = 4.0          # Curvature of the sides
boss_dia = 36.0
boss_height = 2.0
hole_dia = 16.0
groove_width = 8.0
groove_depth = 5.0

# Define key points for the cushion profile
p_tr = (width / 2, height / 2)
p_tl = (-width / 2, height / 2)
p_bl = (-width / 2, -height / 2)
p_br = (width / 2, -height / 2)

# Midpoints for the arcs (bulging outwards)
m_top = (0, height / 2 + bulge)
m_left = (-width / 2 - bulge, 0)
m_bot = (0, -height / 2 - bulge)
m_right = (width / 2 + bulge, 0)

# 1. Main Body: Extrude a square with arced sides (cushion shape)
result = (
    cq.Workplane("XY")
    .moveTo(*p_tr)
    .threePointArc(m_top, p_tl)
    .threePointArc(m_left, p_bl)
    .threePointArc(m_bot, p_br)
    .threePointArc(m_right, p_tr)
    .close()
    .extrude(thickness)
)

# 2. Boss: Extrude a circle on the front face
result = (
    result.faces(">Z")
    .workplane()
    .circle(boss_dia / 2)
    .extrude(boss_height)
)

# 3. Hole: Cut a hole through the center
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_dia / 2)
    .cutThruAll()
)

# 4. Groove: Cut a V-shaped notch along the bottom
# Calculate the lowest Y coordinate of the geometry
y_min = -height / 2 - bulge

result = (
    result.faces(">Z")
    .workplane()
    # Draw a triangle for the cutter profile starting below the part
    .moveTo(-groove_width / 2, y_min - 1.0)
    .lineTo(0, y_min + groove_depth)
    .lineTo(groove_width / 2, y_min - 1.0)
    .close()
    .extrude(-thickness - boss_height - 2)
)