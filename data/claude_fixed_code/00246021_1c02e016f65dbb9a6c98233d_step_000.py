import cadquery as cq

# --- Geometric Parameters ---
cube_size = 20.0       # Size of the square end blocks
shaft_length = 12.0    # Distance between the two blocks
shaft_diameter = 10.0  # Diameter of the connecting cylinder
hole_diameter = 6.0    # Diameter of the through-hole
chamfer_size = 1.5     # Size of the chamfer on cube edges
neck_fillet = 3.0      # Radius of the fillet between shaft and cubes
hole_fillet = 2.0      # Radius of the fillet at the hole openings

# --- Construction ---

# Calculate the offset for the cube centers relative to the origin (0,0,0)
# The assembly is centered at the origin.
block_offset = shaft_length / 2.0 + cube_size / 2.0

# 1. Create the Left Cube
# We create a box on the XY plane and translate it along -X
left_block = (
    cq.Workplane("XY")
    .box(cube_size, cube_size, cube_size)
    .translate((-block_offset, 0, 0))
)

# 2. Create the Right Cube
# Translate along +X
right_block = (
    cq.Workplane("XY")
    .box(cube_size, cube_size, cube_size)
    .translate((block_offset, 0, 0))
)

# 3. Create the Connecting Shaft
# A cylinder oriented along the X-axis. 
# Workplane("YZ") has X as its normal.
shaft = (
    cq.Workplane("YZ")
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    .translate((-shaft_length / 2.0, 0, 0))
)

# 4. Combine parts into a single solid
result = left_block.union(right_block).union(shaft)

# 5. Apply Chamfers
# Select all linear edges. This applies chamfers to the cubes as seen in the image.
result = result.edges("|X or |Y or |Z").chamfer(chamfer_size)

# 6. Apply Neck Fillets
# Select the circular edges where the shaft meets the cubes.
# These edges are located at x = +/- shaft_length/2.
result = result.edges(">X or <X").fillet(neck_fillet)

# 7. Cut the Center Hole
# Select the face with normal +X (the rightmost face), draw a circle, and cut through all.
result = (
    result.faces(">X")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 8. Apply Hole Fillets
# Select the circular edges of the hole on the far left and right faces.
result = result.faces(">X or <X").edges("%CIRCLE").fillet(hole_fillet)