import cadquery as cq
import math

# -----------------------------------------------------------------------------
# 1. Parameter Definitions
# -----------------------------------------------------------------------------
# Estimate dimensions based on visual proportions
outer_diameter = 100.0
plate_thickness = 5.0
bolt_circle_diameter = 80.0
hole_diameter = 8.0
num_features = 12

# Derived dimensions
outer_radius = outer_diameter / 2.0
bolt_circle_radius = bolt_circle_diameter / 2.0
hole_radius = hole_diameter / 2.0

# -----------------------------------------------------------------------------
# 2. Geometry Construction
# -----------------------------------------------------------------------------

# Create the base disk
result = cq.Workplane("XY").circle(outer_radius).extrude(plate_thickness)

# Define feature positions
# The pattern consists of 12 features equally spaced (30 degrees apart).
# Notches (slots) are at 0, 90, 180, 270 degrees.
# Circular holes are at the remaining positions.
slot_angles = [0, 90, 180, 270]
hole_angles = [a for a in range(0, 360, 30) if a not in slot_angles]

# --- Create Circular Holes ---
# Calculate cartesian coordinates for the holes
hole_points = []
for angle in hole_angles:
    rad = math.radians(angle)
    x = bolt_circle_radius * math.cos(rad)
    y = bolt_circle_radius * math.sin(rad)
    hole_points.append((x, y))

# Cut the holes through the plate
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

# --- Create Edge Notches (Slots) ---
# A notch is modeled as a U-shape slot extending from the bolt circle to the outer edge.
# We construct a "cutter" tool representing the material to remove.

# 1. Cylinder part: forms the rounded bottom of the slot at the bolt circle
cutter_cyl = (
    cq.Workplane("XY")
    .moveTo(bolt_circle_radius, 0)
    .circle(hole_radius)
    .extrude(plate_thickness * 3)
)
cutter_cyl = cutter_cyl.translate((0, 0, -plate_thickness))

# 2. Box part: extends the slot to the outer edge
# Length needs to go from bolt_circle_radius to past the outer_radius
box_len = (outer_radius - bolt_circle_radius) + 10.0 # Extra margin to ensure clean cut
box_width = hole_diameter
box_height = plate_thickness * 3

# Calculate center for the box so its left edge aligns with the bolt circle center
# Left Edge X = Center X - Length/2 = bolt_circle_radius
# Center X = bolt_circle_radius + Length/2
box_center_x = bolt_circle_radius + (box_len / 2.0)

cutter_box = (
    cq.Workplane("XY")
    .box(box_len, box_width, box_height)
)
cutter_box = cutter_box.translate((box_center_x, 0, 0))

# Combine cylinder and box to make the U-shape cutter
slot_cutter = cutter_cyl.union(cutter_box)

# Iterate through slot angles, rotate the cutter, and subtract from the main body
for angle in slot_angles:
    # Rotate the cutter around the Z-axis
    rotated_cutter = slot_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)