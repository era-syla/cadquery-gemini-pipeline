import cadquery as cq

# --- Dimensions & Parameters ---
width = 60.0          # Total width of the bracket
height = 60.0         # Total height
depth = 60.0          # Total depth
thickness = 6.0       # Thickness of the main walls
flange_len = 16.0     # Length of the mounting flanges (flat areas)
fillet_outer = 8.0    # Radius for outer corners
fillet_inner = 3.0    # Radius for transition fillets
pocket_depth = 4.0    # Depth of the side recesses
pocket_rim = 5.0      # Thickness of the rim around the side pocket
hole_dia = 5.5        # Mounting hole diameter
cb_dia = 10.0         # Counterbore diameter
cb_depth = 3.0        # Counterbore depth
hole_spacing = 40.0   # Center-to-center distance between holes

# --- 1. Create Base Profile (Wedge Shape) ---
# We define the profile in the YZ plane (Side View) and extrude along X.
# (0,0) corresponds to the bottom-rear corner.
# The profile includes the back wall, bottom wall, and the slanted front face.

pts = [
    (0, 0),                           # Bottom-Rear
    (0, height),                      # Top-Rear
    (thickness, height),              # Top-Front of vertical wall
    (thickness, height - flange_len), # Start of slope
    (depth - flange_len, thickness),  # End of slope
    (depth, thickness),               # Front-Top of horizontal wall
    (depth, 0)                        # Front-Bottom
]

result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(width)
    .translate((-width / 2.0, 0, 0))  # Center geometry on the X-axis
)

# --- 2. Fillet Main Outer Corners ---
# Round the top corners of the vertical back plate.
# We select edges parallel to Y (thickness) located near the top (Z=height).
result = result.edges("|Y").fillet(fillet_outer)

# Round the front corners of the horizontal bottom plate.
# We select edges parallel to Z (thickness) located near the front (Y=depth).
result = result.edges("|Z").fillet(fillet_outer)

# --- 3. Create Side Pockets (Recesses) ---
# We create a triangular prism shape to subtract from the sides.
# The coordinates are offset inwards by 'pocket_rim'.

y_base = thickness + pocket_rim
z_base = thickness + pocket_rim
y_tip = depth - flange_len - pocket_rim * 1.5
z_tip = height - flange_len - pocket_rim * 1.5

pocket_shape = (
    cq.Workplane("YZ")
    .polyline([(y_base, z_base), (y_base, z_tip), (y_tip, z_base), (y_base, z_base)])
    .close()
    .extrude(pocket_depth)
)

# Add fillets to the pocket corners (edges along the extrusion axis X)
pocket_shape = pocket_shape.edges("|X").fillet(3.0)

# Subtract the pocket from both the right (+X) and left (-X) sides.
# Calculate translation vectors to position the pockets correctly on the faces.
pos_right = (width / 2.0 - pocket_depth, 0, 0)
pos_left = (-width / 2.0, 0, 0)

result = result.cut(pocket_shape.translate(pos_right))
result = result.cut(pocket_shape.translate(pos_left))

# --- 4. Drill Mounting Holes ---
# Vertical Flange Holes (Back Plate)
# Workplane on XZ plane, offset in Y to the front face of the back plate.
result = (
    cq.Workplane("XZ")
    .workplane(offset=thickness)
    .pushPoints([
        (-hole_spacing / 2.0, height - flange_len / 2.0), 
        (hole_spacing / 2.0, height - flange_len / 2.0)
    ])
    .cboreHole(hole_dia, cb_dia, cb_depth)
    .cutThruAll()
)

result = result.union(
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(width)
    .translate((-width / 2.0, 0, 0))
)

# Horizontal Flange Holes (Bottom Plate)
# Workplane on XY plane, offset in Z to the top face of the bottom plate.
result = (
    cq.Workplane("XZ")
    .workplane(offset=thickness)
    .pushPoints([
        (-hole_spacing / 2.0, height - flange_len / 2.0), 
        (hole_spacing / 2.0, height - flange_len / 2.0)
    ])
    .cboreHole(hole_dia, cb_dia, cb_depth)
)

result = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .pushPoints([
        (-hole_spacing / 2.0, depth - flange_len / 2.0), 
        (hole_spacing / 2.0, depth - flange_len / 2.0)
    ])
    .cboreHole(hole_dia, cb_dia, cb_depth)
)

# --- 5. Fillet Transition Edges ---
# Smooth the internal edges where the slanted face meets the vertical and horizontal flanges.

# Edge near vertical flange (Upper transition)
# Select edges inside a small bounding box around the transition line.
result = result.edges(cq.selectors.BoxSelector(
    (-width, thickness - 1, height - flange_len - 1),
    (width, thickness + 1, height - flange_len + 1)
)).fillet(fillet_inner)

# Edge near horizontal flange (Lower transition)
result = result.edges(cq.selectors.BoxSelector(
    (-width, depth - flange_len - 1, thickness - 1),
    (width, depth - flange_len + 1, thickness + 1)
)).fillet(fillet_inner)