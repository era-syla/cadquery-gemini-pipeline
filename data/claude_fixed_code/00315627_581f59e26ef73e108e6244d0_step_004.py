import cadquery as cq

# --- Parameters ---
width = 30.0             # Total width of the part
height = 50.0            # Total height of the part
depth = 25.0             # Total depth of the part
back_thickness = 10.0    # Thickness of the vertical back plate
base_height = 25.0       # Height of the front block section
gap_width = 8.0          # Width of the central gap
fillet_radius = 8.0      # Radius for top corners
slot_width = 8.0         # Width of the oblong hole
slot_length = 18.0       # Length of the oblong hole
serration_pitch = 4.0    # Vertical distance between teeth
serration_height = 2.0   # Vertical size of each tooth cut
serration_depth = 1.0    # Depth of the serration cuts

# --- Construction ---

# 1. Create the main L-shaped body
# Create the vertical back plate
back_plate = cq.Workplane("XY").box(width, back_thickness, height, centered=(True, False, False))

# Create the front horizontal block
front_block = (
    cq.Workplane("XY")
    .center(0, back_thickness)
    .box(width, depth - back_thickness, base_height, centered=(True, False, False))
)

# Combine to form the base shape
result = back_plate.union(front_block)

# 2. Fillet the top corners
# Select top edges parallel to the Y-axis
result = result.edges("|Y").filter(lambda e: e.Center().z > height - 1).fillet(fillet_radius)

# 3. Cut the vertical slot (oblong hole)
# Select the front face of the back plate to sketch on
result = (
    result.faces(">Y").workplane(centerOption="ProjectedOrigin")
    # Position the slot in the center of the upper section
    .center(0, base_height + (height - base_height) / 2)
    .slot2D(slot_length, slot_width, angle=90)
    .cutThruAll()
)

# 4. Cut the central gap in the front block
gap_cutter = (
    cq.Workplane("XY")
    .center(0, back_thickness)
    .box(gap_width, depth - back_thickness, base_height, centered=(True, False, False))
)
result = result.cut(gap_cutter)

# 5. Add serrations to the inner face of the left block
# The left block is in the negative X region. Its inner face is at x = -gap_width/2.
# We cut horizontal grooves into this face.

current_z = 3.0  # Start height for the first serration
while current_z < base_height - 1.0:
    # Create a cutter for a single tooth
    tooth_cutter = (
        cq.Workplane("XY")
        .workplane(offset=current_z)
        # Position X: Centered so it cuts into the material from the gap face
        # Position Y: Centered along the depth of the front block
        .center(-gap_width/2 - serration_depth/2, back_thickness + (depth - back_thickness)/2)
        .box(serration_depth, depth - back_thickness, serration_height, centered=(True, True, True))
    )
    
    result = result.cut(tooth_cutter)
    current_z += serration_pitch