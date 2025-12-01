import cadquery as cq

# 1. Geometry Dimensions
# Estimated based on visual proportions
total_length = 120.0
total_width = 25.0
total_height = 40.0
bar_thickness = 12.0
leg_thickness = 18.0     # Thickness of the vertical column
cap_overhang = 4.0       # How much the top cap protrudes inwards
cap_height = 8.0         # Height of the top cap section

# Hole dimensions
hole_diameter = 5.5
cbore_diameter = 10.0
cbore_depth = 4.0

# 2. Profile Definitions
# We work on the XZ plane to draw the side profile
# We assume symmetry around the Z-axis (X=0)
x_outer = total_length / 2.0
x_inner_leg = x_outer - leg_thickness
x_inner_cap = x_inner_leg - cap_overhang # The cap extends further inwards

# Define points clockwise starting from bottom-left
pts = [
    (-x_outer, 0),                                # Bottom Left
    (-x_outer, total_height),                     # Top Left Outer
    (-x_inner_cap, total_height),                 # Top Left Inner
    (-x_inner_cap, total_height - cap_height),    # Bottom of Cap Lip (Left)
    (-x_inner_leg, total_height - cap_height),    # Inner Corner under Lip (Left)
    (-x_inner_leg, bar_thickness),                # Top of Base Bar (Left)
    (x_inner_leg, bar_thickness),                 # Top of Base Bar (Right)
    (x_inner_leg, total_height - cap_height),     # Inner Corner under Lip (Right)
    (x_inner_cap, total_height - cap_height),     # Bottom of Cap Lip (Right)
    (x_inner_cap, total_height),                  # Top Right Inner
    (x_outer, total_height),                      # Top Right Outer
    (x_outer, 0)                                  # Bottom Right
]

# 3. Create Solid
# Extrude the profile symmetrically along Y to form the main body
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(total_width / 2.0, both=True)
)

# 4. Add Counterbored Holes
# Calculate the center X position for the holes
# The hole is centered on the top cap face
# Width of top face = x_outer - x_inner_cap = leg_thickness + cap_overhang
top_face_width = leg_thickness + cap_overhang
hole_x_offset = x_outer - (top_face_width / 2.0)

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_x_offset, 0), 
        (hole_x_offset, 0)
    ])
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# Optional: Add small fillets to vertical outer edges for realism (commented out for strict geometry adherence)
# result = result.edges("|Z").fillet(1.0)