import cadquery as cq

# Dimensions estimated from the image geometry
length = 140.0
width = 60.0
height = 20.0
corner_radius = 10.0
edge_fillet = 1.0

# Ventilation slot parameters
slot_cols = 18
slot_rows = 2
slot_width = 3.0
slot_height = 1.2
slot_dist_x = 5.0  # Horizontal spacing (center-to-center)
slot_dist_y = 3.5  # Vertical spacing (center-to-center)

# 1. Create the main base shape (rectangular box)
# We center it on the XY plane for easier symmetry operations
result = cq.Workplane("XY").box(length, width, height)

# 2. Round the vertical corners to create the stadium-like footprint
# Select edges parallel to Z axis
result = result.edges("|Z").fillet(corner_radius)

# 3. Add small fillets to top and bottom edges for the smooth manufactured look
# Select edges NOT parallel to Z (i.e., the horizontal loops)
result = result.edges("#Z").fillet(edge_fillet)

# 4. Create the ventilation slots on the front long face
# We select the face with the maximum Y coordinate. 
# Due to the fillets, this selects the planar sub-face in the middle of the side.
result = (
    result.faces(">Y")
    .workplane()
    .rarray(
        xSpacing=slot_dist_x, 
        ySpacing=slot_dist_y, 
        xCount=slot_cols, 
        yCount=slot_rows
    )
    .rect(slot_width, slot_height)
    .cutBlind(-3.0)  # Cut 3mm deep into the casing
)

# The 'result' variable now contains the final geometry