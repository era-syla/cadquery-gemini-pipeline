import cadquery as cq

# --- Dimensions & Parameters ---
base_width = 80.0
base_length = 80.0
base_thickness = 10.0
base_fillet_radius = 10.0

mount_depth = 25.0
mount_height = 40.0  # Height of the vertical part above the base
mount_fillet_radius = 10.0 # Vertical edge fillets matching base

saddle_radius = 20.0 # Radius of the top semicircular cutout

# Base Holes (Counterbored)
hole_dia = 6.6
cbore_dia = 12.0
cbore_depth = 4.0
hole_spacing_x = 50.0  # Distance between centers (left-right)
hole_spacing_y = 56.0  # Distance between centers (front-back)

# Top Holes
top_hole_dia = 5.0

# --- Construction ---

# 1. Create the Base Plate
# Centered on XY plane, Z=0 to Z=thickness
base = (
    cq.Workplane("XY")
    .box(base_width, base_length, base_thickness, centered=(True, True, False))
    .edges("|Z")
    .fillet(base_fillet_radius)
)

# 2. Create the Vertical Mount Block
# Positioned at the back edge of the base.
# Base Y range: -40 to 40. Back is Y=+40.
# Mount sits flush with back, depth 25. 
# Mount Y center = 40 - (25/2) = 27.5
mount_y_center = (base_length / 2) - (mount_depth / 2)

mount = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(0, mount_y_center)
    .box(base_width, mount_depth, mount_height, centered=(True, True, False))
)

# Union the parts
result = base.union(mount)

# 3. Fillet the Vertical Edges of the Mount
# We select vertical edges that are above the base height.
# This ensures we get the corners of the mount block, blending them with the base.
result = result.edges("|Z").fillet(mount_fillet_radius)

# 4. Create the Saddle Cutout
# A cylindrical cut along the Y axis from the top of the mount.
# Center of circle is at Z = total height.
total_height = base_thickness + mount_height
saddle_cut = (
    cq.Workplane("XZ", origin=(0, 0, total_height))
    .circle(saddle_radius)
    .extrude(100, both=True) # Extrude along Y axis (normal to XZ)
)

result = result.cut(saddle_cut)

# 5. Create Base Holes (Counterbored)
# Define positions relative to center (0,0)
# Adjust Y positions to fit in the available flat space
# Front holes near Y = -30, Back holes near Y = 5 (in front of mount wall at Y=15)
hx = hole_spacing_x / 2
hy_front = -(base_length / 2) + 12
hy_back = (base_length / 2) - mount_depth - 12

base_hole_pts = [
    (-hx, hy_front), (hx, hy_front),
    (-hx, hy_back), (hx, hy_back)
]

result = (
    cq.Workplane("XY").workplane(offset=base_thickness)
    .pushPoints(base_hole_pts)
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
    .cutThruAll()
)

result = result.union(base.union(mount).cut(saddle_cut))

# Recreate properly
result = base.union(mount)
result = result.edges("|Z").fillet(mount_fillet_radius)
result = result.cut(saddle_cut)

for pt in base_hole_pts:
    result = (
        result.faces("<Z").workplane()
        .center(pt[0], pt[1])
        .cboreHole(hole_dia, cbore_dia, cbore_depth)
    )

# 6. Create Top Holes
# Located on the flat top faces of the mount
# Centered in the material width on each side
# Width from outer edge (40) to saddle edge (20) is 20mm. Center is at 30mm.
tx = saddle_radius + (base_width/2 - saddle_radius)/2
top_hole_pts = [(-tx, mount_y_center), (tx, mount_y_center)]

for pt in top_hole_pts:
    result = (
        result.faces(">Z").workplane()
        .center(pt[0], pt[1])
        .hole(top_hole_dia)
    )