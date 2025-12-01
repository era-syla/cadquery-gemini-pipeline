import cadquery as cq

# --- Parameters ---
# Main Block Dimensions
width_left = 14.0       # Width of the taller left section (tower)
width_right = 6.0       # Width of the shorter right section
gap_width = 12.0        # Width of the U-channel gap
depth = 20.0            # Depth of the block (Z-axis)

# Derived total width
total_width = width_left + gap_width + width_right

# Heights
height_left = 36.0      # Height of the left tower
height_right = 24.0     # Height of the right wall
floor_height = 12.0     # Height of the connecting floor

# Detail Dimensions
notch_size = 4.0        # Size of the notch on the inner top corner of left section
chamfer_size = 6.0      # Size of the chamfer on the back top corner

# Cylinder (Boss) Dimensions
cyl_radius = 7.5
cyl_length = 15.0
flange_radius = 9.5
flange_thickness = 2.0
hole_radius = 5.0

# Position of the cylinder (centered on the left tower horizontally)
cyl_center_x = width_left / 2.0
cyl_center_y = 16.0

# --- Construction ---

# 1. Create the main profile (U-shape with uneven legs and notch)
# Drawing on the XY plane. Z-axis will be the depth.
# Z=0 is the "Back" face, Z=depth is the "Front" face.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(total_width, 0)                          # Bottom edge
    .lineTo(total_width, height_right)               # Right outer vertical
    .lineTo(total_width - width_right, height_right) # Right top
    .lineTo(total_width - width_right, floor_height) # Gap right vertical
    .lineTo(width_left, floor_height)                # Gap floor
    .lineTo(width_left, height_left - notch_size)    # Left inner vertical (up to notch)
    .lineTo(width_left - notch_size, height_left - notch_size) # Notch horizontal step
    .lineTo(width_left - notch_size, height_left)    # Notch vertical step
    .lineTo(0, height_left)                          # Left top
    .close()
    .extrude(depth)
)

# 2. Add Chamfer to the back-top-left edge
# Selecting the edge at Z=0 (Back), Y=max (Top), and on the left side (X < width_left)
result = (
    result.edges("<Z and >Y")
    .chamfer(chamfer_size)
)

# 3. Add Cylinder Boss on the Front Face
# Create a new workplane on the front face (Z=depth)
wp_front = cq.Workplane("XY").workplane(offset=depth)

cylinder = (
    wp_front
    .moveTo(cyl_center_x, cyl_center_y)
    .circle(cyl_radius)
    .extrude(cyl_length)
)
result = result.union(cylinder)

# 4. Add Flange at the end of the cylinder
# Create a workplane at the end of the cylinder
wp_flange = cq.Workplane("XY").workplane(offset=depth + cyl_length)

flange = (
    wp_flange
    .moveTo(cyl_center_x, cyl_center_y)
    .circle(flange_radius)
    .extrude(flange_thickness)
)
result = result.union(flange)

# 5. Cut the Through Hole
# Start from the very front (face of the flange) and cut backwards through the entire object
total_length = depth + cyl_length + flange_thickness
wp_hole = cq.Workplane("XY").workplane(offset=total_length)

result = result.cut(
    wp_hole
    .moveTo(cyl_center_x, cyl_center_y)
    .circle(hole_radius)
    .extrude(-total_length * 1.5) # Negative extrude to cut backwards, with safety margin
)