import cadquery as cq

# Parameters for the aluminum extrusion profile
length = 150.0       # Length of the extrusion
width = 20.0         # External width/height of the profile (e.g., 20mm)
hole_diam = 5.0      # Diameter of the central hole
slot_opening = 6.0   # Width of the slot opening
slot_lip_depth = 1.5 # Depth of the initial lip
slot_inner_w = 10.0  # Width of the inner T-cavity
slot_total_d = 5.5   # Total depth of the slot from the face
fillet_radius = 1.0  # Radius for external corners

# 1. Create the base solid
# We create a box centered at the origin
result = cq.Workplane("XY").box(width, width, length)

# 2. Fillet the vertical edges to give it the rounded profile look
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create the central hole
# Select the top face and cut a hole through the part
result = result.faces(">Z").workplane().hole(hole_diam)

# 4. Create the T-slot cutter geometry
# We define the cross-section of the slot for the +X face
# Points are defined relative to the center (0,0)
# The start/end X points are slightly larger than width/2 to ensure a clean cut through the surface
pts = [
    (width/2 + 0.1, slot_opening/2),               # Start outside
    (width/2 - slot_lip_depth, slot_opening/2),    # Lip depth
    (width/2 - slot_lip_depth - 0.5, slot_inner_w/2), # Angled expansion
    (width/2 - slot_total_d, slot_inner_w/2),      # Inner depth
    (width/2 - slot_total_d, -slot_inner_w/2),     # Bottom of cavity
    (width/2 - slot_lip_depth - 0.5, -slot_inner_w/2),# Angled return
    (width/2 - slot_lip_depth, -slot_opening/2),   # Lip return
    (width/2 + 0.1, -slot_opening/2)               # End outside
]

# Create the cutter solid by extruding the profile
# We center the extrusion in Z to align with the main body
slot_cutter = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(length)
    .translate((0, 0, -length/2))
)

# 5. Cut the slots on all four sides
# We rotate the cutter solid 0, 90, 180, 270 degrees and subtract it
for i in range(4):
    angle = i * 90
    rotated_cutter = slot_cutter.val().rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)