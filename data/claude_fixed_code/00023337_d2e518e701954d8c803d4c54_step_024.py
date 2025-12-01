import cadquery as cq

# -- Parameters --
# Main Plate
lobe_large_radius = 10.0
lobe_small_radius = 5.0
center_distance = 35.0
plate_thickness = 3.0
cutout_radius = 25.0

# Bottom Features
boss_radius = 7.0
boss_height = 8.0
pin_radius = 2.5
pin_height = 28.0

# Top Fin (Handle)
fin_base_width = 11.0
fin_top_width = 2.5
fin_height = 11.0
fin_depth = 12.0  # Length along Y axis

# -- Construction --

# 1. Base Plate
# Create the basic shape using a hull of two circles
plate_hull = (
    cq.Workplane("XY")
    .moveTo(0, 0).circle(lobe_large_radius)
    .moveTo(center_distance, 0).circle(lobe_small_radius)
    .hull()
    .extrude(plate_thickness)
)

# Cut a circular profile from one side to create the concave "waist"
# We position the cut circle to graze the tangent line and bite into the material
cut_y_offset = -30.0  # Offset in Y for the center of the cutting circle
cut_x_offset = center_distance / 2.0
plate = plate_hull.cut(
    cq.Workplane("XY")
    .moveTo(cut_x_offset, cut_y_offset)
    .circle(cutout_radius)
    .extrude(plate_thickness)
)

# Apply fillets to the sharp vertical edges created by the cut
# We select vertical edges near the middle of the part
try:
    plate = plate.edges("|Z").fillet(2.0)
except Exception:
    # Fallback if fillet fails (geometry might be tangent)
    pass

# 2. Bottom Boss (Cylinder under the large lobe)
boss = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .circle(boss_radius)
    .extrude(-boss_height)
)

# 3. Long Pin (Cylinder under the small lobe)
pin = (
    cq.Workplane("XY")
    .moveTo(center_distance, 0)
    .circle(pin_radius)
    .extrude(-pin_height)
)

# 4. Top Fin
# We sketch the profile on the XZ plane and extrude symmetrically along Y
# The profile is wide at the base, narrows with concave sides, and has a flat top (to be rounded)
x_base = fin_base_width / 2.0
x_top = fin_top_width / 2.0
z_base = plate_thickness
z_top = plate_thickness + fin_height

# Calculate a mid-point for the concave arc
# We want the waist to pinch in
x_mid = (x_base + x_top) * 0.4
z_mid = (z_base + z_top) * 0.5

fin = (
    cq.Workplane("XZ")
    .moveTo(x_base, z_base)
    .lineTo(-x_base, z_base)
    # Left concave side
    .threePointArc((-x_mid, z_mid), (-x_top, z_top))
    # Top edge
    .lineTo(x_top, z_top)
    # Right concave side
    .threePointArc((x_mid, z_mid), (x_base, z_base))
    .close()
    .extrude(fin_depth / 2.0, both=True)
)

# Round off the top of the fin fully
# Select the top edges running along Y and fillet them
fin = fin.edges(">Z and |Y").fillet(fin_top_width / 2.1)

# -- Assembly --
result = plate.union(boss).union(pin).union(fin)

# Optional: Add a small fillet at the base of the fin for a realistic look
try:
    result = result.edges(
        cq.selectors.BoxSelector((-fin_base_width, -fin_depth, plate_thickness-0.1), 
                                 (fin_base_width, fin_depth, plate_thickness+0.1))
    ).fillet(0.5)
except Exception:
    pass