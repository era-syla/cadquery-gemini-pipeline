import cadquery as cq

# --- Parameter Definitions ---
# Estimated dimensions based on visual analysis of the image
plate_length = 120.0
plate_height = 40.0
plate_thickness = 3.0
corner_radius = 5.0

# Slot parameters
slot_length = 25.0       # Total vertical length of the slot
slot_width = 4.0         # Width of the slot
slot_x_offset = 45.0     # Distance from center to slot center

# --- Geometry Construction ---

# 1. Create the base rectangular plate centered on the XY plane
result = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# 2. Apply fillets to the four vertical corners
# Select edges parallel to the Z-axis ("|Z")
result = result.edges("|Z").fillet(corner_radius)

# 3. Create the two vertical slots
# Select the top face (Z > 0) to sketch on
# Push two points symmetric about the origin for the slot locations
# Use slot2D to create vertical slots
# Cut through the entire thickness of the plate
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-slot_x_offset, 0), (slot_x_offset, 0)])
    .slot2D(slot_length, slot_width, 90)
    .cutThruAll()
)