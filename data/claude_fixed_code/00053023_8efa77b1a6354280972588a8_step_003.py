import cadquery as cq

# Based on the image analysis:
# 1. The object is a rectangular prism (box).
# 2. It appears to have a square cross-section (length equals width).
# 3. The height is roughly 1.6 times the width.
# 4. The object is hollowed out from the top face, creating a container-like shape.
# 5. The walls have a noticeable, uniform thickness.
# 6. There are no visible fillets or chamfers; edges are sharp.

# Estimated Dimensions
length = 50.0       # X dimension
width = 50.0        # Y dimension
height = 80.0       # Z dimension
wall_thickness = 5.0

# Generate the geometry
# Step 1: Create the main solid block centered at the origin.
# Step 2: Select the top face (+Z direction).
# Step 3: Use the shell command to hollow out the solid. 
#         A negative thickness adds material inwards (keeping outer dims) 
#         and removes the selected face(s).
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .shell(wall_thickness)
)