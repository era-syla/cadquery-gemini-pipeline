import cadquery as cq
import math

# --- Dimensions (Estimated from image) ---
head_diameter = 22.0
head_height = 12.0
shank_diameter = 16.0
shank_height = 10.0
hex_width_across_flats = 10.0  # Standard Allen key size
hex_depth = 8.0
hole_diameter = 6.0
fillet_top_radius = 2.0
fillet_bottom_radius = 1.5

# Calculate hex circumdiameter for the polygon function
# Diameter = 2 * (Width / sqrt(3))
hex_circum_diameter = 2 * (hex_width_across_flats / math.sqrt(3))

# --- Geometry Construction ---

# 1. Create the main Head cylinder
# We start on the XY plane and extrude upwards
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# 2. Create the Shank (Threaded section base)
# Select the bottom face of the head and extrude downwards.
# Note: faces("<Z") selects the face at Z=0. The workplane created on this face
# will typically have its normal pointing in -Z, so positive extrusion goes down.
result = result.faces("<Z").workplane().circle(shank_diameter / 2.0).extrude(-shank_height)

# 3. Add Fillets
# Fillet the top edge of the head
result = result.faces(">Z").edges().fillet(fillet_top_radius)

# Fillet the bottom edge of the shank
# The image shows a rounded bottom lip
result = result.faces("<Z").edges().fillet(fillet_bottom_radius)

# 4. Create the Hexagonal Socket
# Select the top face (which is now an annulus due to the fillet, but >Z finds it)
result = result.faces(">Z").workplane() \
    .polygon(nSides=6, diameter=hex_circum_diameter) \
    .cutBlind(-hex_depth)

# 5. Create the Center Through Hole
# Cut from the top through the entire part
# We use a depth slightly larger than the total height to ensure a clean cut
total_depth = head_height + shank_height + 5.0
result = result.faces(">Z").workplane() \
    .circle(hole_diameter / 2.0) \
    .cutBlind(-total_depth)