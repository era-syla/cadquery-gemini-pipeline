import cadquery as cq

# --- Parameters ---
# Defined to match the proportions in the image
r_outer = 50.0
r_inner = 30.0
thickness = 18.0

# Angular dimensions (in degrees)
angle_large_sector = 110.0  # The larger curved piece on the left
angle_small_sector = 50.0   # The smaller piece on the right
gap_angle = 25.0            # The angular gap between the two pieces

# --- Geometry Construction ---

def make_annular_sector(angle):
    """
    Creates an annular sector by creating a rectangular profile on the XZ plane
    (radial-height plane) and revolving it around the Z axis.
    """
    # Calculate dimensions for the 2D profile
    section_width = r_outer - r_inner
    
    # Center point of the rectangle in the sketch plane
    # X corresponds to radial distance, Y corresponds to height (Z) in the Workplane("XZ")
    center_x = r_inner + (section_width / 2.0)
    center_y = thickness / 2.0
    
    # Create the solid sector
    sector = (
        cq.Workplane("XZ")
        .center(center_x, center_y)
        .rect(section_width, thickness)
        .revolve(angle, (0, 0, 0), (0, 0, 1))
    )
    return sector

# 1. Create the large sector (starts at 0 degrees)
large_piece = make_annular_sector(angle_large_sector)

# 2. Create the small sector
small_piece = make_annular_sector(angle_small_sector)

# 3. Rotate the small piece to position it after the large piece plus the gap
# The start angle of the small piece should be: start of large + angle of large + gap
rotation_angle = angle_large_sector + gap_angle
small_piece = small_piece.rotate((0, 0, 0), (0, 0, 1), rotation_angle)

# 4. Combine the two pieces into a single object
result = large_piece.union(small_piece)

# 5. Re-orient the result to match the isometric view in the image
# Rotating so the large piece is on the left and the gap is visible in the front-right
result = result.rotate((0, 0, 0), (0, 0, 1), -160)

# The 'result' variable now contains the final CadQuery object