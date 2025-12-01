import cadquery as cq

# --- Parameters ---
length = 90.0           # Overall length of the part
width = 60.0            # Overall width
rail_height = 10.0      # Height of the side rails
plate_thickness = 2.0   # Thickness of the base plate
rail_width = 8.0        # Width of each side rail

# Side groove details
groove_height = 2.0
groove_depth = 1.0
groove_z_center = 5.0   # Vertical center of the groove

# Top square pocket details
pocket_size = 4.0
pocket_depth = 2.0
pocket_offset = 6.0     # Distance from center of pocket to the end face

# End vertical slot details
end_slot_width = 3.0
end_slot_depth = 2.0

# --- Geometry Construction ---

# 1. Define the Profile on XZ Plane
# We trace the perimeter of the cross-section to extrude.
# Coordinates are calculated relative to the center (X=0).
w2 = width / 2.0
rw = rail_width
h = rail_height
pt = plate_thickness
gz_bot = groove_z_center - groove_height / 2.0
gz_top = groove_z_center + groove_height / 2.0
gd = groove_depth

pts = [
    (-w2, 0),                       # Bottom Left
    (w2, 0),                        # Bottom Right
    # Right Side Profile (Upwards)
    (w2, gz_bot),                   # Groove bottom outer
    (w2 - gd, gz_bot),              # Groove bottom inner
    (w2 - gd, gz_top),              # Groove top inner
    (w2, gz_top),                   # Groove top outer
    (w2, h),                        # Top Right
    (w2 - rw, h),                   # Top Right Inner
    (w2 - rw, pt),                  # Inner corner down to plate
    (-w2 + rw, pt),                 # Across plate to left rail
    (-w2 + rw, h),                  # Top Left Inner
    (-w2, h),                       # Top Left
    # Left Side Profile (Downwards)
    (-w2, gz_top),                  # Groove top outer
    (-w2 + gd, gz_top),             # Groove top inner
    (-w2 + gd, gz_bot),             # Groove bottom inner
    (-w2, gz_bot),                  # Groove bottom outer
    # Close back to (-w2, 0)
]

# Create the main body by extruding the profile
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(length / 2.0, both=True)
)

# 2. Cut Square Pockets on Top Rails
# Calculate centers for the 4 pockets
px = w2 - rw / 2.0
py = length / 2.0 - pocket_offset
pocket_centers = [
    (px, py), (px, -py),
    (-px, py), (-px, -py)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pocket_centers)
    .rect(pocket_size, pocket_size)
    .cutBlind(-pocket_depth)
)

# 3. Cut Vertical Slots on Rail Ends
# We perform this on both the front (>Y) and back (<Y) faces.
# Slot centers are aligned with the rail centers in X.
rail_x_centers = [
    w2 - rw / 2.0,
    -(w2 - rw / 2.0)
]

# Iterate over both end faces
for face in [">Y", "<Y"]:
    for x in rail_x_centers:
        result = (
            result.faces(face)
            .workplane()
            .center(x, h / 2.0)
            .rect(end_slot_width, h)
            .cutBlind(-end_slot_depth)
        )