import cadquery as cq

# Define parametric dimensions
length = 60.0    # Length of the block (X axis)
width = 40.0     # Width of the block (Y axis)
height = 35.0    # Height of the block (Z axis)
notch_width = 20.0  # Width of the cutout
notch_depth = 10.0  # Depth of the cutout into the block

# Create the base block centered at the origin
# box() generates a solid with dimensions centered at (0,0,0)
result = cq.Workplane("XY").box(length, width, height)

# Create the rectangular notch on the back edge
# 1. Select the top face (positive Z)
# 2. Create a workplane on that face
# 3. Move the cursor to the center of the back edge (positive Y boundary)
#    Since the box is centered, the back edge is at y = width/2
# 4. Draw a rectangle to act as the cutting profile.
#    We make the rectangle extend beyond the edge to ensure a clean cut.
# 5. Perform a blind cut downwards through the entire height of the block.
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, width / 2.0 - notch_depth / 2.0)
    .rect(notch_width, notch_depth)
    .cutBlind(-height)
)