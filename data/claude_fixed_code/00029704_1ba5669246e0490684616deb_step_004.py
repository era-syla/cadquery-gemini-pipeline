import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 150.0
width = 25.0
thickness = 4.0
fillet_radius = 2.0
chamfer_size = 0.5  # Slight chamfer on top edges

# Slot configuration (Transverse cuts)
slot_width = 5.0
slot_depth = 1.0
# Slot positions determined by visual analysis of segments:
# Pattern from center: Center Land -> Slot -> Land -> Slot -> Land -> Slot -> End Land
# Estimated pitch centers: 12.5mm, 32.5mm, 52.5mm
slot_offsets = [12.5, 32.5, 52.5]

# Hole configuration (Countersunk)
hole_diameter = 4.5  # Clearance for M4 screw
csk_diameter = 9.0
csk_angle = 90.0
# Hole positions: Center and centered in the end lands
# End land range: 55mm to 75mm -> Center at 65mm
hole_offsets = [0, 65] 

# --- Geometry Construction ---

# 1. Create the base rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Fillet the vertical corners
result = result.edges("|Z").fillet(fillet_radius)

# 3. Chamfer the top perimeter edges
# We do this before cutting slots/holes to keep the chamfer only on the outer contour
result = result.faces(">Z").edges().chamfer(chamfer_size)

# 4. Cut the transverse slots
# Generate symmetric points for slots
slot_points = [(x, 0) for x in slot_offsets] + [(-x, 0) for x in slot_offsets]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_points)
    .rect(slot_width, width * 1.2)
    .cutBlind(-slot_depth)
)

# 5. Create countersunk holes
# Generate symmetric points for holes
hole_points = [(0, 0)] + [(x, 0) for x in hole_offsets if x != 0] + [(-x, 0) for x in hole_offsets if x != 0]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)