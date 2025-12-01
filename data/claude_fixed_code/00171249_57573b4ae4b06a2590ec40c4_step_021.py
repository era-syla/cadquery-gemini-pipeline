import cadquery as cq

# Dimensions based on visual analysis of the image
length = 80.0       # Total length of the block
width = 40.0        # Total width of the block
height = 30.0       # Total height of the block
step_length = 25.0  # Length of the lower step section
cut_depth = 15.0    # Depth of the step cut (resulting step height will be height - cut_depth)
hole_diameter = 16.0 # Diameter of the central hole

# 1. Create the main base block
# We start with a solid rectangular block centered on the XY plane
result = cq.Workplane("XY").box(length, width, height)

# 2. Create the step feature
# We cut away a rectangular volume from the top-left corner
# We select the top face, create a workplane, and center it where the cut should be.
# The cut is on the negative X side.
# Offset calculation: Start at left edge (-length/2) and move inwards by half the cut length.
cut_center_x = -(length / 2) + (step_length / 2)

result = result.faces(">Z").workplane() \
    .center(cut_center_x, 0) \
    .rect(step_length, width) \
    .cutBlind(-cut_depth)

# 3. Create the hole
# We select the highest face (">Z") which is now the top face of the remaining taller section.
# The workplane() method automatically sets the origin (0,0) to the center of this new face.
# We then drill a hole through the block.
result = result.faces(">Z").workplane() \
    .circle(hole_diameter / 2) \
    .cutThruAll()

# The 'result' variable now contains the final geometry