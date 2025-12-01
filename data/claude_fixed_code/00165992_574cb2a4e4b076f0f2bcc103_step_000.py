import cadquery as cq

# ==========================================
# Parameter Definitions
# ==========================================
# Main body dimensions
width = 40.0            # Total width (Y-axis depth)
wall_th = 8.0           # Base and wall thickness
arch_ir = 15.0          # Inner radius of the arch
arch_or = arch_ir + wall_th  # Outer radius (23.0)

# Left Tab dimensions
l_tab_len = 30.0        # Length extending from the arch center line roughly
l_tab_overlap = 5.0     # Overlap to ensure fusion
l_tab_effective_len = l_tab_len - arch_or # Extension beyond arch radius

# Right Flange dimensions
r_base_len = 12.0       # Horizontal section length on right
r_flange_h = 50.0       # Total height of vertical flange
r_flange_th = 10.0      # Thickness of vertical flange

# Feature dimensions
hole_dia = 6.0
cbore_dia = 11.0
cbore_depth = 3.0
slot_width = 12.0
slot_depth = 15.0
fillet_rad_neck = 6.0
fillet_rad_corner = 8.0

# ==========================================
# Solid Construction
# ==========================================

# 1. Central Arch
# Created as a semi-cylinder on the XZ plane, extruded along Y.
# Center of the semi-circle is at (0,0,0).
arch = (
    cq.Workplane("XZ")
    .circle(arch_or)
    .extrude(width / 2, both=True)
    # Cut the inner tunnel
    .cut(
        cq.Workplane("XZ")
        .circle(arch_ir)
        .extrude(width, both=True)
    )
    # Cut off the bottom half (Z < 0)
    .cut(
        cq.Workplane("XY")
        .rect(arch_or * 3, width * 2)
        .extrude(-arch_or)
    )
)

# 2. Left Tab
# A box overlapping with the left side of the arch.
# Position X: extends from -arch_or outwards.
l_pos_x = -(arch_or + l_tab_effective_len/2) + (l_tab_overlap/2)
left_tab = (
    cq.Workplane("XY")
    .workplane(offset=wall_th / 2)
    .rect(l_tab_effective_len + l_tab_overlap, width)
    .extrude(wall_th, both=True)
    .translate((l_pos_x, 0, 0))
)

# 3. Right Base Section
# A horizontal connector on the right side.
r_base_x = (arch_or + r_base_len/2) - (l_tab_overlap/2)
right_base = (
    cq.Workplane("XY")
    .workplane(offset=wall_th / 2)
    .rect(r_base_len + l_tab_overlap, width)
    .extrude(wall_th, both=True)
    .translate((r_base_x, 0, 0))
)

# 4. Right Vertical Flange
r_flange_x = arch_or + r_base_len + r_flange_th/2
right_flange = (
    cq.Workplane("XY")
    .workplane(offset=r_flange_h / 2)
    .rect(r_flange_th, width)
    .extrude(r_flange_h, both=True)
    .translate((r_flange_x, 0, 0))
)

# Union the parts into the main body
result = arch.union(left_tab).union(right_base).union(right_flange)

# ==========================================
# Fillets and Refinements
# ==========================================

# 1. Neck Fillets (Connection between flat tabs and arch cylinder)
# Selecting edges at Z=wall_th, roughly at X = +/- arch_or
# Using a BoxSelector to isolate these intersection edges.
neck_selector = cq.selectors.BoxSelector(
    (-arch_or - 5, -width, wall_th - 1),
    (arch_or + 5, width, wall_th + 1)
)
result = result.edges(neck_selector).fillet(fillet_rad_neck)

# 2. Internal Corner of Right L-Bracket
# Intersection of right base and vertical flange
l_corner_selector = cq.selectors.BoxSelector(
    (r_flange_x - r_flange_th, -width, wall_th - 1),
    (r_flange_x, width, wall_th + 1)
)
# Note: Previous fillet might have consumed adjacent edges, try/except or direct selection
try:
    result = result.edges(l_corner_selector).fillet(4.0)
except:
    pass

# 3. External Corner Fillets (Left Tab)
result = result.edges("|Z").edges("<X").fillet(fillet_rad_corner)

# 4. Top Corner Fillets (Right Flange)
result = result.edges("|Y").edges(">Z").edges(">X").fillet(5.0)

# ==========================================
# Holes and Cuts
# ==========================================

# 1. Top Countersunk Hole
result = (
    result
    .faces(">Z").workplane()
    .center(0, 0)
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
)

# 2. Left Tab Mounting Holes
# Two holes aligned along the Y-axis
hole_spacing = 20.0
result = (
    result
    .faces(">Z").workplane()
    .center(-(arch_or + l_tab_effective_len/2), 0)
    .pushPoints([(0, -hole_spacing/2), (0, hole_spacing/2)])
    .hole(hole_dia)
)

# 3. Vertical Flange Slot (U-Shape)
# We draw the profile on the YZ plane and cut through the flange.
slot_profile = (
    cq.Workplane("YZ")
    .workplane(offset=r_flange_x + r_flange_th + 1)
    .moveTo(-slot_width/2, r_flange_h + 1)
    .lineTo(-slot_width/2, r_flange_h - slot_depth)
    .threePointArc(
        (0, r_flange_h - slot_depth - slot_width/2), 
        (slot_width/2, r_flange_h - slot_depth)
    )
    .lineTo(slot_width/2, r_flange_h + 1)
    .close()
    .extrude(-r_flange_th - 5)
)

result = result.cut(slot_profile)