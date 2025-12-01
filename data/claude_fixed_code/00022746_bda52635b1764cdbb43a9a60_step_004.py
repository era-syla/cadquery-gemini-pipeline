import cadquery as cq

# ---------------------------------------------------------
# Parametric definitions for a 2020 T-Slot Aluminum Profile
# ---------------------------------------------------------
length = 400.0          # Total length of the extrusion
size = 20.0             # Profile width/height (20mm)
fillet_radius = 1.0     # Radius for the outer corner fillets
center_bore_dia = 5.0   # Diameter of the central hole (usually tapped for M5)

# Slot Geometry Parameters
slot_opening = 6.0      # Width of the slot opening at the face
slot_depth = 6.0        # Total depth of the slot from the face
slot_neck_height = 1.5  # Depth of the narrow neck section
slot_inner_width = 9.0  # Width of the wider inner cavity (approximate for T-nut)

# ---------------------------------------------------------
# 1. Create Base Solid
# ---------------------------------------------------------
# Create the main prism centered at the origin
result = cq.Workplane("XY").box(size, size, length)

# Apply fillets to the four longitudinal edges
result = result.edges("|Z").fillet(fillet_radius)

# ---------------------------------------------------------
# 2. Create Center Hole
# ---------------------------------------------------------
# Drill the central bore through the entire length
result = result.faces(">Z").workplane().circle(center_bore_dia / 2.0).cutThruAll()

# ---------------------------------------------------------
# 3. Create T-Slots
# ---------------------------------------------------------
# We define the 2D cross-section of the T-slot "cutter" (the void)
# coordinates are relative to the center of the profile (0,0)
# This definition assumes the slot is on the top face (+Y)

# Coordinates calculation
y_face = size / 2.0
y_neck_bottom = y_face - slot_neck_height
y_slot_bottom = y_face - slot_depth
x_neck = slot_opening / 2.0
x_inner = slot_inner_width / 2.0

# Define points for the T-shape polygon
slot_points = [
    (x_neck, y_face),           # Top right at face
    (x_neck, y_neck_bottom),    # Bottom right of neck
    (x_inner, y_neck_bottom),   # Top right of inner cavity
    (x_inner, y_slot_bottom),   # Bottom right of inner cavity
    (-x_inner, y_slot_bottom),  # Bottom left of inner cavity
    (-x_inner, y_neck_bottom),  # Top left of inner cavity
    (-x_neck, y_neck_bottom),   # Bottom left of neck
    (-x_neck, y_face)           # Top left at face
]

# Create the solid cutter object for one slot
# Extrude half the length in both directions to cover the full beam
cutter_solid = cq.Workplane("XY").polyline(slot_points).close().extrude(length / 2.0, both=True)

# Subtract the cutter from the base solid on all 4 sides
for angle in [0, 90, 180, 270]:
    # Rotate the cutter around the Z-axis
    rotated_cutter = cutter_solid.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)