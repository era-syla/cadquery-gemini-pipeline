import cadquery as cq

# Dimensions for the small block
block_width = 20.0
block_height = 30.0
block_length = 40.0

# Dimensions for the long bar
bar_width = 20.0
bar_height = 30.0
bar_length = 200.0

# Dimensions for the cutouts
cutout_width = 5.0
cutout_height = 5.0
cutout_depth = bar_width
cutout_spacing = 15.0
cutout_offset = 10.0

# Create the small block
block = cq.Workplane("XY").box(block_width, block_length, block_height)

# Create the long bar
bar = cq.Workplane("XY").box(bar_width, bar_length, bar_height)

# Create the cutouts on the long bar
cutouts = (
    cq.Workplane("XY")
    .workplane(offset=bar_height / 2)
    .pushPoints([(cutout_offset, 0), (cutout_offset + cutout_spacing, 0), (cutout_offset + 2 * cutout_spacing, 0)])
    .box(cutout_width, cutout_depth, cutout_height, centered=(True, True, False))
)

# Subtract the cutouts from the long bar
bar = bar.cut(cutouts)

# Assemble the parts
result = block.translate((-60, 0, 0)).union(bar)

# Show the result
cq.exporters.export(result,'model.stl')