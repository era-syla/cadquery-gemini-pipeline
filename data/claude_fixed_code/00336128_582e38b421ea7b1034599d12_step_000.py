import cadquery as cq

# --- Parameters ---
# Extrusion Dimensions
beam_length = 500.0
beam_size = 20.0
slot_width = 6.0
slot_depth = 6.0
center_hole_dia = 5.0
fillet_radius = 1.5

# Hardware Dimensions (Screw and Nut)
screw_offset_x = 30.0
nut_offset_x = 45.0
screw_head_dia = 8.5
screw_head_height = 3.0
screw_shank_dia = 5.0
screw_shank_len = 10.0
nut_width = 10.0
nut_height = 4.0

# --- 1. Create Aluminum Extrusion Profile ---
# Define the 2D profile sketch
profile_sketch = (
    cq.Sketch()
    .rect(beam_size, beam_size)
    .vertices()
    .fillet(fillet_radius)
    .circle(center_hole_dia / 2.0, mode='s')  # Cut center hole
    .reset()
)

# Cut vertical slots (Top and Bottom)
profile_sketch = profile_sketch.push([(0, beam_size / 2.0), (0, -beam_size / 2.0)])
profile_sketch = profile_sketch.rect(slot_width, slot_depth * 2.0, mode='s')

# Cut horizontal slots (Left and Right)
profile_sketch = profile_sketch.reset().push([(-beam_size / 2.0, 0), (beam_size / 2.0, 0)])
profile_sketch = profile_sketch.rect(slot_depth * 2.0, slot_width, mode='s')

# Extrude the profile
beam = cq.Workplane("XY").placeSketch(profile_sketch).extrude(beam_length)

# --- 2. Create Screw (Bolt) ---
screw = (
    cq.Workplane("XY")
    .center(screw_offset_x, 0)
    .circle(screw_head_dia / 2.0)
    .extrude(screw_head_height)
    .faces(">Z")
    .workplane()
    .circle(screw_shank_dia / 2.0)
    .extrude(screw_shank_len)
)

# --- 3. Create Nut ---
nut = (
    cq.Workplane("XY")
    .center(nut_offset_x, 0)
    .rect(nut_width, nut_width)
    .extrude(nut_height)
    .faces(">Z")
    .workplane()
    .circle(screw_shank_dia / 2.0)
    .cutThruAll()
)

# --- Combine Geometry ---
result = beam.union(screw).union(nut)