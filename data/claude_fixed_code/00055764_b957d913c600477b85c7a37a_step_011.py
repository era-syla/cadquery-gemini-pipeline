import cadquery as cq

# Parameters defining the cabinet geometry
# Width: Dimension along the 'Right' face (Longer side in image)
# Depth: Dimension along the 'Left' face (Shorter side with toe kick)
width = 800.0
depth = 500.0
height = 850.0
thickness = 20.0     # Wall thickness
kick_height = 100.0  # Height of the toe kick recess
kick_depth = 50.0    # Depth of the toe kick recess

# 1. Create the main base block
# Aligned such that Width is along X, Depth along Y, Height along Z.
result = cq.Workplane("XY").box(width, depth, height)

# 2. Hollow out the top to create the carcass
# We remove the top face (+Z) and shell inwards by 'thickness'
result = result.faces(">Z").shell(-thickness)

# 3. Create the central divider
# The divider splits the width, creating two compartments side-by-side.
# Dimensions calculations:
# - Width: thickness
# - Length: Fits inside front/back walls (depth - 2*thickness)
# - Height: Fits from floor to top (height - thickness)
divider_height = height - thickness
divider_length = depth - 2 * thickness

divider = (
    cq.Workplane("XY")
    .box(thickness, divider_length, divider_height)
    .translate((0, 0, thickness / 2)) # Shift Z to rest on the internal floor
)

# Union the divider with the main shell
result = result.union(divider)

# 4. Create the Toe Kick Cutout
# The toe kick is a recess on the bottom of the Front face (Left face in image, -Y direction).
# We use a large cutter box positioned to remove the bottom-front corner.
# Cutter dimensions:
# - X: width (cuts across the full width)
# - Y: 2 * kick_depth (centered on edge, cuts 'kick_depth' into the material)
# - Z: 2 * kick_height (centered on edge, cuts 'kick_height' up from bottom)
kick_cutter = (
    cq.Workplane("XY")
    .box(width, kick_depth * 2, kick_height * 2)
    .translate((0, -depth / 2, -height / 2))
)

result = result.cut(kick_cutter)

# 5. Add cosmetic groove/seam on the side panel
# The image shows a horizontal line on the side face (Right face, +X direction) at the toe kick height.
# We cut a shallow groove to represent this.
seam_cutter = (
    cq.Workplane("XY")
    .box(2.0, depth, 2.0) # 2mm thick cutter
    .translate((width / 2, 0, -height / 2 + kick_height))
)

result = result.cut(seam_cutter)