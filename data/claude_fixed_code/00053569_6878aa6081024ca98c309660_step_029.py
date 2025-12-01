import cadquery as cq

# --- Parameters ---
fuselage_length = 50.0
fuselage_diameter = 12.0

wing_span = 180.0
wing_chord_root = 18.0
wing_chord_tip = 9.0
wing_sweep_offset = 8.0  # Moves tip back
wing_z_pos = fuselage_diameter * 0.6  # Mount on top of fuselage

boom_offset_y = 35.0  # Distance from center
boom_diameter = 1.5
boom_length = 65.0    # Total length from wing LE

tail_chord = 10.0
tail_drop_z = 20.0    # Height of V-tail
tail_sweep_x = 10.0   # Sweep of tail leading edge

# --- Helper Functions ---
def airfoil_shape(workplane, chord, thickness_rel=0.12):
    """Draws a simple airfoil shape on the given workplane."""
    # Points approximate a generic cambered airfoil
    pts = [
        (0, 0),
        (chord * 0.25, chord * thickness_rel),
        (chord * 0.5, chord * thickness_rel * 0.9),
        (chord, 0),
        (chord * 0.5, -chord * thickness_rel * 0.2),
        (chord * 0.25, -chord * thickness_rel * 0.3),
        (0, 0)
    ]
    return workplane.polyline(pts).close()

# --- 1. Fuselage ---
# Revolve a teardrop profile around the X-axis
# X-axis: +X is Nose, -X is Tail
p_tail = (-fuselage_length / 2, 0)
p_nose = (fuselage_length / 2, 0)
p_top = (fuselage_length * 0.1, fuselage_diameter / 2) # Peak thickness slightly forward

fuselage = (
    cq.Workplane("XZ")
    .moveTo(*p_tail)
    .spline([p_top, p_nose], 
            tangents=[(1, 0.2), (0, -1)], 
            includeCurrent=True)
    .lineTo(*p_tail)
    .close()
    .revolve(360, (-1, 0, 0), (1, 0, 0))
)

# --- 2. Main Wing ---
# Loft from root profile to tip profile
wing_le_x = 5.0 # Leading edge X position relative to origin

# Root Profile (at center, y=0)
wp_root = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(wing_le_x, wing_z_pos)
)
root_wire = airfoil_shape(wp_root, wing_chord_root).wires().val()

# Tip Profile (at semi-span)
wp_tip = (
    cq.Workplane("XZ")
    .workplane(offset=wing_span / 2)
    .center(wing_le_x + wing_sweep_offset, wing_z_pos)
)
tip_wire = airfoil_shape(wp_tip, wing_chord_tip).wires().val()

# Create Right Wing and Mirror
wing_right = cq.Workplane("XZ").add(root_wire).add(tip_wire).loft()
wing_left = wing_right.mirror(mirrorPlane="XZ")

# --- 3. Winglets ---
# Vertical stabilizers at wingtips
winglet_height = 10.0
winglet_root_p = (wing_le_x + wing_sweep_offset + 2, wing_span / 2, wing_z_pos)

winglet_right = (
    cq.Workplane("XY")
    .workplane(offset=wing_z_pos)
    .center(winglet_root_p[0], winglet_root_p[1])
    .rect(wing_chord_tip * 0.7, 0.8)
    .workplane(offset=winglet_height)
    .center(winglet_root_p[0] + 2, winglet_root_p[1])
    .rect(wing_chord_tip * 0.4, 0.4)
    .loft()
)
winglet_left = winglet_right.mirror(mirrorPlane="XZ")

# --- 4. Tail Booms ---
# Cylinders extending backwards from the wing
boom_start_x = wing_le_x + 5
boom_end_x = boom_start_x - boom_length

# On YZ plane, Local X is Global Y, Local Y is Global Z
boom_right = (
    cq.Workplane("YZ")
    .workplane(offset=boom_start_x)
    .center(boom_offset_y, wing_z_pos)
    .circle(boom_diameter / 2)
    .extrude(boom_end_x - boom_start_x) # Extrude negative X
)
boom_left = boom_right.mirror(mirrorPlane="XZ")

# --- 5. Inverted V-Tail ---
# Connects boom ends to a lower central vertex
tail_root_x = boom_end_x
tail_tip_x = boom_end_x - tail_sweep_x
tail_tip_z = wing_z_pos - tail_drop_z

# Profile at Boom connection (Right side)
tp_boom = (
    cq.Workplane("XZ")
    .workplane(offset=boom_offset_y)
    .center(tail_root_x, wing_z_pos)
)
tail_wire_boom = airfoil_shape(tp_boom, tail_chord, 0.08).wires().val()

# Profile at Bottom Center connection
tp_center = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(tail_tip_x, tail_tip_z)
)
tail_wire_center = airfoil_shape(tp_center, tail_chord, 0.08).wires().val()

# Loft Right Tail Surface
tail_right = cq.Workplane("XZ").add(tail_wire_boom).add(tail_wire_center).loft()
tail_left = tail_right.mirror(mirrorPlane="XZ")

# --- Assembly ---
result = (
    fuselage
    .union(wing_right)
    .union(wing_left)
    .union(winglet_right)
    .union(winglet_left)
    .union(boom_right)
    .union(boom_left)
    .union(tail_right)
    .union(tail_left)
)