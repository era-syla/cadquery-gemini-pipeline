import cadquery as cq

# --- Parameter Definitions ---
# Estimated dimensions based on visual proportions
outer_diameter = 30.0      # Main body diameter
length = 25.0              # Total length of the part
hole_diameter = 16.0       # Diameter of the central hole
slot_count = 6             # Number of slots (hexagonal pattern)
slot_width = 6.0           # Tangential width of the slots
slot_depth_axial = 9.0     # How deep the slots go down the length
slot_depth_radial = 4.5    # How deep the slots cut into the wall

# --- Construction ---

# 1. Create the base cylindrical body
# Start on the XY plane and extrude upwards
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(length)

# 2. Cut the central through-hole
# We select the top face to define the hole concentric to the Z-axis
result = result.faces(">Z").workplane().hole(hole_diameter)

# 3. Create the castellation slots
# We define a rectangular cutter profile and array it radially.
# Calculation for cutter position:
# We want the slot to cut from the outer surface inwards by 'slot_depth_radial'.
# We use a rectangle that is long enough ('cutter_len') to ensure it clears the outer edge.
cutter_len = 20.0  # Arbitrary length large enough to clear the OD
radius = outer_diameter / 2.0

# The inner edge of the cutter needs to be at (radius - slot_depth_radial).
# Since the rectangle is centered, its center should be placed at:
# Center = Inner_Edge + (Length / 2)
cutter_center_radius = (radius - slot_depth_radial) + (cutter_len / 2.0)

result = (
    result.faces(">Z")
    .workplane()
    # Create 6 positions around the center
    .polarArray(cutter_center_radius, 0, 360, slot_count)
    # Define the shape of the cut (Long in Radial X, Width in Tangential Y)
    .rect(cutter_len, slot_width)
    # Cut downwards
    .cutBlind(-slot_depth_axial)
)

# 4. Add chamfer to the hole entrance
# This gives the visual cue of a threaded entry and cleans the edge.
# We select edges on the top face closest to the center axis.
result = (
    result.faces(">Z")
    .edges()
    .chamfer(1.0)
)