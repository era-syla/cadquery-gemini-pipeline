import cadquery as cq

# Overall dimensions
width = 100.0   # Width along X-axis
length = 100.0  # Depth along Y-axis
height = 20.0   # Height along Z-axis

# Feature dimensions (estimated from visual proportions)
# The left raised block width
left_block_w = 25.0

# The wide central channel
channel_w = 30.0
channel_depth = 10.0  # Cuts halfway down

# The strip between the channel and the slot
inner_strip_w = 25.0

# The narrow slot dimensions
slot_w = 4.0
slot_depth = 15.0  # Deeper than the channel

# Calculate X-axis center positions for the cuts
# Assuming the main box is centered at (0,0,0), X ranges from -50 to +50
x_start = -width / 2.0

# Center of the wide channel
# Starts after left block
channel_x_pos = x_start + left_block_w + (channel_w / 2.0)

# Center of the narrow slot
# Starts after left block + channel + inner strip
slot_x_pos = x_start + left_block_w + channel_w + inner_strip_w + (slot_w / 2.0)

# 1. Create the base solid block
result = cq.Workplane("XY").box(width, length, height)

# 2. Define the wide channel geometry (as a negative volume)
# Create a workplane at the top of the box (Z = height/2)
channel_cut = (
    cq.Workplane("XY")
    .workplane(offset=height / 2.0)
    .center(channel_x_pos, 0)
    .rect(channel_w, length)
    .extrude(-channel_depth)
)

# 3. Define the narrow slot geometry (as a negative volume)
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=height / 2.0)
    .center(slot_x_pos, 0)
    .rect(slot_w, length)
    .extrude(-slot_depth)
)

# 4. Subtract the cuts from the base result
result = result.cut(channel_cut).cut(slot_cut)