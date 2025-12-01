import cadquery as cq

# Visual analysis dimensions:
# - The scene contains two main structures: a stack of two blocks on the left, and a single block on the right.
# - The blocks appear to have a rectangular footprint where the depth is roughly twice the width.
# - The height of each individual block appears roughly equal to its width.
# - The gap between the structures is approximately half the width of a block.

# Define base dimensions
block_width = 10.0   # Short horizontal dimension (X-axis)
block_depth = 20.0   # Long horizontal dimension (Y-axis)
block_height = 10.0  # Vertical dimension (Z-axis)
gap = 5.0            # Spacing between the left stack and right block

# --- Construct the Left Object (Stack) ---

# Bottom block of the stack
# box() creates a shape centered at (0,0,0), so we lift it by height/2 to sit on Z=0
left_bottom = cq.Workplane("XY").box(block_width, block_depth, block_height).translate((0, 0, block_height / 2))

# Top block of the stack
# Lifted to sit on top of the bottom block (center at Z = 1.5 * height)
left_top = cq.Workplane("XY").box(block_width, block_depth, block_height).translate((0, 0, block_height * 1.5))

# --- Construct the Right Object (Single Block) ---

# Calculate offset along the width axis (X-axis)
# Center distance = (width/2) + gap + (width/2) = width + gap
x_offset = block_width + gap

# Single block placed to the right
right_block = cq.Workplane("XY").box(block_width, block_depth, block_height).translate((x_offset, 0, block_height / 2))

# --- Combine into Result ---

# Create a container Workplane and add all solids.
# We do not use union() here because we want to preserve the visible seam 
# between the stacked blocks, exactly as shown in the source image.
result = cq.Workplane("XY")
result = result.union(left_bottom)
result = result.union(left_top)
result = result.union(right_block)