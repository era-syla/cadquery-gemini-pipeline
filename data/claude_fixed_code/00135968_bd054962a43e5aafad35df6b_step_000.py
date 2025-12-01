import cadquery as cq

# 1. Define Dimensions
# Estimated based on visual proportions from the image
width = 30.0           # Width of the bracket
leg_length = 60.0      # External length of both legs
thickness = 6.0        # Thickness of the material
hole_diam = 10.0       # Diameter of the mounting holes
fillet_radius = 6.0    # Radius of the inner bend

# 2. Create the base L-profile
# We draw the profile on the XZ plane (Side view)
# - X axis corresponds to the horizontal leg direction
# - Z axis corresponds to the vertical leg direction
# - Extrusion happens along the Y axis
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(leg_length, 0)             # Bottom edge
    .lineTo(leg_length, thickness)     # End of horizontal leg
    .lineTo(thickness, thickness)      # Inner corner horizontal
    .lineTo(thickness, leg_length)     # Inner vertical line
    .lineTo(0, leg_length)             # Top of vertical leg
    .close()
    .extrude(width / 2.0, both=True)   # Extrude symmetrically along Y
)

# 3. Add inner fillet
# The inner corner edge is parallel to the Y axis ("|Y")
# It is located spatially near (thickness, 0, thickness)
result = result.edges("|Y").fillet(fillet_radius)

# 4. Create and Cut Holes
# Using explicit cutter bodies is the most robust way to place holes 
# without worrying about local face coordinates.

# Calculate hole center offsets (centered width-wise, inset from leg ends)
hole_offset = width / 2.0 
v_hole_z = leg_length - hole_offset
h_hole_x = leg_length - hole_offset

# Cutter 1: Horizontal cylinder for the vertical leg
# Oriented on YZ plane, extruded along X
hole_cutter_vertical = (
    cq.Workplane("YZ")
    .moveTo(0, v_hole_z)
    .circle(hole_diam / 2.0)
    .extrude(100, both=True) # Extrude enough to cut through the part
)

# Cutter 2: Vertical cylinder for the horizontal leg
# Oriented on XY plane, extruded along Z
hole_cutter_horizontal = (
    cq.Workplane("XY")
    .moveTo(h_hole_x, 0)
    .circle(hole_diam / 2.0)
    .extrude(100, both=True) # Extrude enough to cut through the part
)

# Apply the cuts to the main object
result = result.cut(hole_cutter_vertical).cut(hole_cutter_horizontal)