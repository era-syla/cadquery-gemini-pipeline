import cadquery as cq

# Parametric dimensions
base_length = 80.0
base_width = 40.0
base_thickness = 10.0
upright_thickness = 20.0
hole_height = 45.0       # Z-height of the hole center
hole_diameter = 15.0
rib_height = 30.0        # Height of the rib along the upright face
rib_length = 40.0        # Length of the rib along the base
rib_width = 10.0         # Thickness of the rib
fillet_radius = 8.0

# 1. Create the main L-shaped body with rounded top
# We draw the side profile on the XZ plane
main_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_length, 0)
    .lineTo(base_length, base_thickness)
    .lineTo(upright_thickness, base_thickness)
    .lineTo(upright_thickness, hole_height)
    # Create the semi-circle top
    .threePointArc(
        (upright_thickness / 2.0, hole_height + upright_thickness / 2.0),
        (0, hole_height)
    )
    .close()
)

# Extrude symmetrically along Y axis
main_body = main_profile.extrude(base_width / 2.0, both=True)

# 2. Create the triangular support rib
rib_profile = (
    cq.Workplane("XZ")
    .moveTo(upright_thickness, base_thickness)
    .lineTo(upright_thickness, base_thickness + rib_height)
    .lineTo(upright_thickness + rib_length, base_thickness)
    .close()
)

# Extrude rib symmetrically
rib = rib_profile.extrude(rib_width / 2.0, both=True)

# Combine main body and rib
result = main_body.union(rib)

# 3. Cut the through hole
# Select the upright face and cut the hole
result = (
    result.faces("<X")
    .workplane()
    .center(0, hole_height - base_thickness)
    .hole(hole_diameter)
)

# 4. Add fillets to the front corners of the base
# Select vertical edges at the far end of the X axis
result = (
    result.edges("|Z")
    .filter(lambda e: e.Center().x > base_length - 1.0)
    .fillet(fillet_radius)
)