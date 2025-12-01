import cadquery as cq

# --- Dimensions ---
body_width = 30.0    # Main body width (X)
body_height = 60.0   # Main body height (Y)
body_thick = 6.0     # Main body thickness (Z)

clip_height = 40.0   # Height of the clip arm (Y)
clip_length = 26.0   # Length of the clip arm along the body (X)
clip_thick = 2.0     # Thickness of the clip arm material
clip_gap = 2.5       # Gap between body front face and clip arm
clip_bend_ext = 1.5  # How far the clip loop extends outwards from the side

tab_height = 8.0     # Height of the side locking tabs
tab_stickout = 2.0   # How far tabs protrude from the side
tab_chamfer = 1.0    # Chamfer size for tabs and body

# --- 1. Main Body ---
# Create the base rectangular block, centered at origin
result = cq.Workplane("XY").box(body_width, body_height, body_thick)

# Apply chamfers to the right-side vertical edges (locking side)
# Selecting edges at X > 0 (right) and parallel to Y axis
result = result.edges(">X and |Y").chamfer(tab_chamfer)

# --- 2. Clip Arm Construction ---
# We sketch the profile of the clip in the XZ plane (Top View) 
# and extrude it along Y (Height).

# Coordinates for the profile path
x_left = -body_width / 2.0
z_back = -body_thick / 2.0
z_front = body_thick / 2.0
z_clip_inner = z_front + clip_gap
z_clip_outer = z_clip_inner + clip_thick

# Calculate bend geometry to loop from back-left corner to front clip position
# The bend creates a U-shape covering the left side
bend_diameter = z_clip_outer - z_back
bend_radius_outer = bend_diameter / 2.0
bend_radius_inner = bend_radius_outer - clip_thick
bend_center_z = z_back + bend_radius_outer

# Draw the U-shape profile
clip_profile = (
    cq.Workplane("XZ")
    .moveTo(x_left, z_back)  # Start at back-left corner of body
    .lineTo(x_left - clip_bend_ext, z_back) # Extend out
    # Outer 180-degree turn
    .threePointArc(
        (x_left - clip_bend_ext - bend_radius_outer, bend_center_z), # Arc mid-point
        (x_left - clip_bend_ext, z_clip_outer)                       # Arc end-point
    )
    .lineTo(x_left + clip_length, z_clip_outer) # Main arm
    .lineTo(x_left + clip_length, z_clip_inner) # Tip thickness
    .lineTo(x_left - clip_bend_ext, z_clip_inner) # Return path
    # Inner 180-degree turn
    .threePointArc(
        (x_left - clip_bend_ext - bend_radius_inner, bend_center_z),
        (x_left - clip_bend_ext, z_back + clip_thick)
    )
    .lineTo(x_left, z_back + clip_thick) # Connect back to body side
    .close()
)

# Extrude the profile symmetrically in Y to create the clip solid
clip_solid = clip_profile.extrude(clip_height / 2.0, both=True)

# Apply fillets to the clip edges for smooth finish
clip_solid = clip_solid.edges("|Y").fillet(0.5)

# --- 3. Clip Tip Lip ---
# Small ridge at the end of the clip for gripping
lip = (
    cq.Workplane("XY")
    .box(2.0, clip_height, 1.0)
    .edges(">X")
    .chamfer(0.5)
    .translate((x_left + clip_length - 1.0, 0, z_clip_inner - 0.5))
)

# --- 4. Side Locking Tabs ---
# Create the locking tabs on the right side (top and bottom)
tab_geo = (
    cq.Workplane("XY")
    .box(tab_stickout, tab_height, body_thick)
    .edges(">X")
    .chamfer(1.0)
)

# Position top and bottom tabs
y_tab_pos = (body_height / 2.0) - (tab_height / 2.0)
x_tab_pos = (body_width / 2.0) + (tab_stickout / 2.0)

tab_top = tab_geo.translate((x_tab_pos, y_tab_pos, 0))
tab_bot = tab_geo.translate((x_tab_pos, -y_tab_pos, 0))

# --- 5. Assembly ---
# Combine all parts into the final result
result = result.union(clip_solid).union(lip).union(tab_top).union(tab_bot)