import cadquery as cq

# --- Object Dimensions & Parameters ---
length = 450.0          # Total estimated length
width = 60.0            # Main body width
thickness = 3.0         # Plate thickness

# Left End (Rounded Tapered Tip)
tip_radius = 20.0       # Radius of the semi-circle at the left tip
taper_length = 90.0     # Length of the tapered transition section

# Right End (Rectangular)
right_hole_offset = 35.0 # Distance of the right mounting center from the right edge
right_corner_fillet = 5.0

# Mounting Hole Configuration (Left and Right ends)
main_hole_dia = 20.0    # Diameter of the large center holes
screw_pcd = 32.0        # Pitch Circle Diameter for the small mounting holes
screw_hole_dia = 3.5    # Diameter of the small mounting holes

# --- 1. Base Geometry Construction ---
# We define the profile starting from the left tip (origin at tip center)
# The path is drawn clockwise.

result = (
    cq.Workplane("XY")
    # Start at the top of the rounded tip
    .moveTo(0, tip_radius)
    # Line to the start of the straight section (top edge)
    .lineTo(taper_length, width / 2.0)
    # Line along the top edge to the right end
    .lineTo(length, width / 2.0)
    # Line down the right edge
    .lineTo(length, -width / 2.0)
    # Line back along the bottom edge
    .lineTo(taper_length, -width / 2.0)
    # Line to the bottom of the rounded tip
    .lineTo(0, -tip_radius)
    # Close with an arc for the rounded tip
    .threePointArc((-tip_radius, 0), (0, tip_radius))
    .close()
    .extrude(thickness)
)

# --- 2. Fillets ---
# Apply fillets to the two corners at the far right end
# We select edges parallel to Z located at the maximum X coordinate
result = result.edges("|Z and (>X[-4:])").fillet(right_corner_fillet)

# --- 3. Mounting Patterns ---
# Function to create the standard mounting pattern (Center hole + 4 surrounding screws)
def cut_mounting_pattern(part, center_x, center_y):
    # Cut large center hole
    part = part.faces(">Z").workplane().center(center_x, center_y).circle(main_hole_dia / 2.0).cutThruAll()
    # Cut surrounding screw holes (4 holes, rotated 45 degrees for X-orientation)
    part = (
        part.faces(">Z").workplane()
        .center(center_x, center_y)
        .polarArray(screw_pcd / 2.0, 45, 360, 4)
        .circle(screw_hole_dia / 2.0)
        .cutThruAll()
    )
    return part

# Apply to Left End (Origin)
result = cut_mounting_pattern(result, 0, 0)

# Apply to Right End
right_center_x = length - right_hole_offset
result = cut_mounting_pattern(result, right_center_x, 0)

# --- 4. Edge Details (Notches) ---
# Create small rectangular notches on the side edges as seen in the image
notch_w = 4.0
notch_d = 2.0

# Notches near the taper transition
result = result.faces(">Z").workplane().center(taper_length + 15, width/2).rect(notch_w, notch_d*2).cutThruAll()
result = result.faces(">Z").workplane().center(taper_length + 15, -width/2).rect(notch_w, notch_d*2).cutThruAll()

# Notches near the right mounting area
result = result.faces(">Z").workplane().center(right_center_x - 50, width/2).rect(notch_w, notch_d*2).cutThruAll()
result = result.faces(">Z").workplane().center(right_center_x - 50, -width/2).rect(notch_w, notch_d*2).cutThruAll()

# --- 5. Additional Holes ---
# Scattered small holes along the body for assembly/alignment
extra_holes = [
    (taper_length - 15, 12),   # On taper
    (taper_length - 15, -12),  # On taper
    (taper_length + 50, 0),    # Centerline
    (length / 2.0, 15),        # Offset
    (length / 2.0, -15),       # Offset
    (right_center_x - 80, 0)   # Near right end
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(extra_holes)
    .circle(1.6) # ~3.2mm holes
    .cutThruAll()
)