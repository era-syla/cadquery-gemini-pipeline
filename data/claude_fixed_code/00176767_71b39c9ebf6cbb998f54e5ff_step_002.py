import cadquery as cq

# --- Parameter Definitions ---
# Base dimensions
base_length = 50.0
base_width = 20.0
base_thickness = 4.0
base_fillet_radius = 5.0

# Mounting holes (countersunk)
hole_spacing = 35.0
hole_diameter = 4.2
csk_diameter = 8.5
csk_angle = 90.0

# Mount/Hinge dimensions (GoPro style)
prong_depth = 15.0       # Dimension along the long axis of the base (profile width)
prong_height_rel = 11.0  # Height from top of base to center of pivot hole
prong_thickness = 3.0
prong_gap = 3.0
pivot_hole_diameter = 5.0

# Calculated parameters
prong_radius = prong_depth / 2.0
z_base_top = base_thickness / 2.0
z_pivot_center = z_base_top + prong_height_rel

# --- Geometry Construction ---

# 1. Create the Base Plate
# Rectangular block with rounded vertical corners
result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
    .edges("|Z")
    .fillet(base_fillet_radius)
)

# 2. Add Mounting Holes
# Select top face and drill countersunk holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)])
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 3. Create the 3-Prong Hinge
# We define a function to create a single prong and then union them.
# The prong profile is a "tombstone" shape (rectangle + semi-circle) on the XZ plane.

def create_prong(y_offset):
    return (
        cq.Workplane("XZ")
        .workplane(offset=y_offset)
        .moveTo(-prong_radius, z_base_top)
        .lineTo(prong_radius, z_base_top)
        .lineTo(prong_radius, z_pivot_center)
        # Create the rounded top using a 3-point arc
        .threePointArc((0, z_pivot_center + prong_radius), (-prong_radius, z_pivot_center))
        .close()
        .extrude(prong_thickness)
        .translate((0, y_offset - prong_thickness / 2.0, 0))
    )

# Calculate Y offsets for the 3 prongs to be centered
# Pattern: [Prong] [Gap] [Prong] [Gap] [Prong]
# Spacing between centers = thickness + gap = 6.0 mm
offsets = [0, -(prong_thickness + prong_gap), (prong_thickness + prong_gap)]

# Generate and union the prongs
prongs_solid = create_prong(offsets[0])
for off in offsets[1:]:
    prongs_solid = prongs_solid.union(create_prong(off))

# Join prongs to the base
result = result.union(prongs_solid)

# 4. Cut the Pivot Hole
# A hole running through all prongs along the Y axis
# We create a cylinder on the XZ plane and cut it out
pivot_cutter = (
    cq.Workplane("XZ")
    .moveTo(0, z_pivot_center)
    .circle(pivot_hole_diameter / 2.0)
    .extrude(base_width + 10.0)
    .translate((0, -(base_width + 10.0) / 2.0, 0))
)

result = result.cut(pivot_cutter)