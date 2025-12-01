import cadquery as cq

# --- Dimensions ---
height = 100.0
thickness = 2.0

# Widths (relative to the straight back edge at x=0)
width_stem = 4.0
width_head = 9.0
width_foot_tip = 10.0

# Vertical positions for features
y_top = height
y_head_straight_bottom = 85.0  # Bottom of the straight part of the head
y_stem_top = 70.0              # Top of the constant width stem
y_foot_start = 25.0            # Where the stem starts widening for the foot
y_foot_tip = 8.0               # Height of the sharp tip of the foot
y_bottom = 0.0

# --- Geometry Construction ---

# Define points for the profile (Counter-Clockwise starting from Bottom-Right)
# Back edge is aligned with X=0
pts = [
    (0, y_bottom),                  # Bottom-Right
    (0, y_top),                     # Top-Right
    (-width_head, y_top),           # Top-Left (Head top)
    (-width_head, y_head_straight_bottom), # Head bottom straight
    (-width_stem, y_stem_top),      # Stem top (taper end)
    (-width_stem, y_foot_start),    # Stem bottom (foot start)
    (-width_foot_tip, y_foot_tip),  # Foot tip
    (-width_stem, y_bottom)         # Foot bottom base
]

# Create the base profile
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
)

# --- Apply Fillets to Smooth the Shape ---
# We use nearestTo to robustly select the vertices to fillet

# 1. Round the top head
result = result.vertices(f"(x<-{width_head-0.1}) and (y>{y_top-0.1})").fillet(6.0)
result = result.vertices(f"(x>-0.1) and (y>{y_top-0.1})").fillet(2.0)

# 2. Smooth transition from Head to Stem (S-curve)
result = result.vertices(f"(x<-{width_head-0.1}) and (y>{y_head_straight_bottom-0.1}) and (y<{y_head_straight_bottom+0.1})").fillet(8.0)
result = result.vertices(f"(x<-{width_stem-0.1}) and (x>-{width_stem+0.1}) and (y>{y_stem_top-0.1}) and (y<{y_stem_top+0.1})").fillet(8.0)

# 3. Smooth transition from Stem to Foot
result = result.vertices(f"(x<-{width_stem-0.1}) and (x>-{width_stem+0.1}) and (y>{y_foot_start-0.1}) and (y<{y_foot_start+0.1})").fillet(15.0)

# 4. Sharper details on the Foot
# Tip of the foot - small radius so it's not razor sharp but distinct
result = result.vertices(f"(x<-{width_foot_tip-0.1}) and (y>{y_foot_tip-0.1}) and (y<{y_foot_tip+0.1})").fillet(1.0)
# Bottom return corner
result = result.vertices(f"(x<-{width_stem-0.1}) and (x>-{width_stem+0.1}) and (y<0.1)").fillet(2.0)


# --- Extrusion ---
result = result.extrude(thickness)