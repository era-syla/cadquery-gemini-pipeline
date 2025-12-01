import cadquery as cq

# -- Parameters --
# Base Plate dimensions
plate_w = 80.0
plate_d = 80.0
plate_t = 5.0

# Mounting Hole parameters
hole_spacing = 60.0  # Center-to-center distance
hole_diam = 5.0
cbore_diam = 9.0
cbore_depth = 2.0

# Central Housing Block dimensions
block_w = 30.0
block_d = 30.0
block_h = 15.0

# Top Cylinder Stack dimensions
cyl1_diam = 22.0
cyl1_h = 4.0
cyl2_diam = 14.0
cyl2_h = 3.0
aperture_diam = 5.0

# Side Connector Feature dimensions
side_l = 20.0  # Length extending from the block
side_w = 18.0  # Width along the side of the block
side_h = 7.0

# Bottom Mount dimensions
bot_block_w = 35.0
bot_block_d = 35.0
bot_block_h = 10.0
bot_fin_w = 70.0  # Width of the bottom plate/fin
bot_fin_d = 35.0
bot_fin_t = 2.0

# -- Construction --

# 1. Base Plate
result = cq.Workplane("XY").box(plate_w, plate_d, plate_t)

# 2. Mounting Holes (Counterbored)
# Select the top face of the plate
result = result.faces(">Z").workplane() \
    .pushPoints([
        (-hole_spacing/2, -hole_spacing/2),
        (-hole_spacing/2, hole_spacing/2),
        (hole_spacing/2, -hole_spacing/2),
        (hole_spacing/2, hole_spacing/2)
    ]) \
    .cboreHole(hole_diam, cbore_diam, cbore_depth)

# 3. Central Block
# Extrude upwards from the top face
result = result.faces(">Z").workplane() \
    .rect(block_w, block_d) \
    .extrude(block_h)

# 4. Cylinder Stack (Lens housing)
# First cylinder
result = result.faces(">Z").workplane() \
    .circle(cyl1_diam / 2) \
    .extrude(cyl1_h)

# Second cylinder
result = result.faces(">Z").workplane() \
    .circle(cyl2_diam / 2) \
    .extrude(cyl2_h)

# 5. Central Aperture
# Cut a hole through the entire stack
result = result.faces(">Z").workplane() \
    .circle(aperture_diam / 2) \
    .cutThruAll()

# 6. Side Connector Feature
# We need to draw on the top face of the base plate again.
# The plate top face is at Z = plate_t / 2.
# We position it so it touches the central block.
# Center X = (block_w/2) + (side_l/2)
pos_x = (block_w / 2) + (side_l / 2)

side_connector = cq.Workplane("XY").workplane(offset=plate_t/2) \
    .center(pos_x, 0) \
    .rect(side_l, side_w) \
    .extrude(side_h)

result = result.union(side_connector)

# 7. Bottom Features
# Select the bottom face of the base plate (Z = -plate_t/2)
# Note: When selecting a bottom face, the normal is pointing down (-Z).
# Positive extrude values will add material downwards.

# Bottom central block
bottom_block = cq.Workplane("XY").workplane(offset=-plate_t/2) \
    .rect(bot_block_w, bot_block_d) \
    .extrude(-bot_block_h)

result = result.union(bottom_block)

# Bottom wide fin/plate
bottom_fin = cq.Workplane("XY").workplane(offset=-plate_t/2 - bot_block_h) \
    .rect(bot_fin_w, bot_fin_d) \
    .extrude(-bot_fin_t)

result = result.union(bottom_fin)

# Return result for visualization
# show_object(result)