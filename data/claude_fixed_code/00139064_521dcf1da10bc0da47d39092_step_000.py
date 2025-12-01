import cadquery as cq

# --- Parameters ---
# Cylinder Dimensions
cyl_height = 30.0
cyl_od = 12.0
cyl_id = 9.0
cyl_spacing = 13.0
slit_width = 2.5

# Derived values
cyl_radius = cyl_od / 2.0
cyl_hole_radius = cyl_id / 2.0

# Bracket Dimensions
# The bracket width is set to match the total width of the two cylinders
bracket_width = cyl_spacing + cyl_od
bracket_depth = 10.0  # Depth of the C-channel arms
bracket_wall_thick = 2.0
bracket_lip_height = 4.0

# Connector Dimension
# Distance from cylinder center plane (Y=0) to the start of the bracket C-profile
# Ensures a solid block connects the back of the cylinders to the bracket
conn_length = cyl_radius + 2.0 

# --- Modeling ---

# 1. Create the Solid Base for Cylinders
# Two vertical cylinders extruded along Z
cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-cyl_spacing/2.0, 0), (cyl_spacing/2.0, 0)])
    .circle(cyl_radius)
    .extrude(cyl_height)
)

# 2. Create the Connector Block
# A rectangular block that bridges the cylinders and the bracket
# Positioned from Y=0 to Y=conn_length
connector = (
    cq.Workplane("XY")
    .rect(bracket_width, conn_length)
    .extrude(cyl_height)
    .translate((0, conn_length / 2.0, 0))
)

# 3. Create the Bracket (C-Channel)
# The profile is defined on the YZ plane (Side view) and extruded along X (Width)
# Coordinates are (Y, Z) relative to the global origin
y_start = conn_length
y_end = y_start + bracket_depth
z_bot = 0
z_top = cyl_height
t = bracket_wall_thick
lip = bracket_lip_height

# Define points for the C-shape profile
# Starting from bottom-inner corner, going counter-clockwise
profile_pts = [
    (y_start, z_bot),
    (y_end, z_bot),
    (y_end, lip),
    (y_end - t, lip),
    (y_end - t, t),
    (y_start + t, t),              # Back wall inner face
    (y_start + t, z_top - t),
    (y_end - t, z_top - t),
    (y_end - t, z_top - lip),
    (y_end, z_top - lip),
    (y_end, z_top),
    (y_start, z_top),
    (y_start, z_bot)               # Close the loop
]

bracket = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(bracket_width / 2.0, both=True)  # Extrude symmetrically along X
)

# Union the solid components
main_body = cylinders.union(connector).union(bracket)

# 4. Create Cuts (Bores and Slits)

# Bore holes for the cylinders
bores = (
    cq.Workplane("XY")
    .pushPoints([(-cyl_spacing/2.0, 0), (cyl_spacing/2.0, 0)])
    .circle(cyl_hole_radius)
    .extrude(cyl_height)
)

# Slits for the cylinders
# Centered on the cylinder X coordinates
# Positioned to cut the front half (negative Y)
slit_cutter = (
    cq.Workplane("XY")
    .rect(slit_width, cyl_od)
    .extrude(cyl_height)
    .translate((-cyl_spacing/2.0, -cyl_radius, 0))
)

slit_cutter2 = (
    cq.Workplane("XY")
    .rect(slit_width, cyl_od)
    .extrude(cyl_height)
    .translate((cyl_spacing/2.0, -cyl_radius, 0))
)

# Apply cuts to the main body
result = main_body.cut(bores).cut(slit_cutter).cut(slit_cutter2)