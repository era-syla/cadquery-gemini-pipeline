import cadquery as cq

# Parametric dimensions
width = 20
height = 20
length1 = 100
length2 = 100

# Create the first block
block1 = cq.Workplane("XY").box(length1, width, height)

# Create the second block
block2 = cq.Workplane("XY").box(length2, width, height)

# Assemble the blocks
result = block1.union(block2.translate((length1, 0, 0)))