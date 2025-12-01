import cadquery as cq

# --- Dimensions & Parameters ---
outer_diameter = 100.0
inner_diameter = 42.0
thickness = 2.0

# Perimeter settings (castle/crenellation pattern)
num_teeth = 30
notch_depth = 3.0
notch_width = 4.0

# Pattern parameters
large_window_w = 14.0
large_window_h = 10.0
large_window_y_offset = -33.0

ring1_radius = 29.0  # Inner slot ring
ring2_radius = 36.0  # Hole ring
ring3_radius = 43.0  # Outer slot ring

# --- Geometry Construction ---

# 1. Base Disc
# Create the main cylindrical body
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(thickness)

# 2. Central Bore
# Cut the large hole in the center
center_hole = cq.Workplane("XY").circle(inner_diameter / 2.0).extrude(thickness)
result = result.cut(center_hole)

# 3. Perimeter Notches
# Create the "castle" gear pattern by cutting rectangular notches around the edge
# The notch cutter is positioned so that it cuts into the edge by 'notch_depth'
import math
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    x = (outer_diameter / 2.0) * math.cos(math.radians(angle))
    y = (outer_diameter / 2.0) * math.sin(math.radians(angle))
    notch_cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(notch_depth * 2, notch_width)
        .extrude(thickness)
    )
    result = result.cut(notch_cutter)

# 4. Large Rectangular Window
# The distinct rectangular feature at the bottom (6 o'clock position)
large_window = (
    cq.Workplane("XY")
    .center(0, large_window_y_offset)
    .rect(large_window_w, large_window_h)
    .extrude(thickness)
)
result = result.cut(large_window)

# 5. Inner Ring: Tangential Slots
# A pattern of rectangular slots oriented tangentially
for i in range(10):
    angle = i * 360.0 / 10
    x = ring1_radius * math.cos(math.radians(angle))
    y = ring1_radius * math.sin(math.radians(angle))
    slot_cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(2.5, 5.0)
        .extrude(thickness)
    )
    result = result.cut(slot_cutter)

# 6. Middle Ring: Circular Holes
# Small holes distributed between the slot rings, offset in angle
for i in range(10):
    angle = 18 + i * 360.0 / 10
    x = ring2_radius * math.cos(math.radians(angle))
    y = ring2_radius * math.sin(math.radians(angle))
    hole_cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(1.5)
        .extrude(thickness)
    )
    result = result.cut(hole_cutter)

# 7. Outer Ring: Radial/Square Slots
# Denser pattern of slots near the perimeter
for i in range(20):
    angle = i * 360.0 / 20
    x = ring3_radius * math.cos(math.radians(angle))
    y = ring3_radius * math.sin(math.radians(angle))
    slot_cutter = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(3.5, 2.5)
        .extrude(thickness)
    )
    result = result.cut(slot_cutter)