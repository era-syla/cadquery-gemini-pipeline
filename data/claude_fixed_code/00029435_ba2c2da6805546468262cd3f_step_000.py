import cadquery as cq

# Object Parameters
length = 80.0          # Total length of the bracket
height = 40.0          # Height of the vertical leg
width = 30.0           # Depth of the horizontal leg
thickness = 4.0        # Material thickness
hole_dia = 8.0         # Diameter of the holes
fillet_radius = 8.0    # Radius of the rounded corners
bend_radius_inner = 2.0 # Inner radius of the bend
bend_radius_outer = bend_radius_inner + thickness

# Hole positioning
hole_spacing = 25.0    # Spacing from center for outer holes
hole_z_pos = 25.0      # Height of holes on vertical leg
hole_y_pos = 18.0      # Depth of holes on horizontal leg

# 1. Create the base L-profile geometry
# Draw profile on YZ plane (Side view) and extrude along X (Length)
# Origin is placed at the bottom-back corner
result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, height)            # Vertical back line
    .lineTo(thickness, height)    # Top thickness
    .lineTo(thickness, thickness) # Inner vertical line
    .lineTo(width, thickness)     # Inner horizontal line
    .lineTo(width, 0)             # Front vertical line
    .close()
    .extrude(length / 2.0, both=True) # Extrude symmetrically centered on Origin
)

# 2. Apply fillets to the bend
# Inner bend fillet: Select the internal edge at the corner
result = result.edges(
    cq.selectors.BoxSelector(
        (-length, thickness - 0.1, thickness - 0.1),
        (length, thickness + 0.1, thickness + 0.1)
    )
).fillet(bend_radius_inner)

# Outer bend fillet: Select the external edge at the origin
result = result.edges(
    cq.selectors.BoxSelector(
        (-length, -0.1, -0.1),
        (length, 0.1, 0.1)
    )
).fillet(bend_radius_outer)

# 3. Round the plate corners
# Vertical leg: Top corners (Edges parallel to X, at max Z)
result = result.edges("|X").edges(">Z").fillet(fillet_radius)

# Horizontal leg: Front corners (Edges parallel to X, at max Y)
result = result.edges("|X").edges(">Y").fillet(fillet_radius)

# 4. Cut Holes
# Vertical Leg: 3 holes
# Select the back face (<Y direction)
result = (
    result.faces("<Y").workplane()
    .pushPoints([
        (-hole_spacing, hole_z_pos), 
        (0, hole_z_pos), 
        (hole_spacing, hole_z_pos)
    ])
    .hole(hole_dia)
)

# Horizontal Leg: 2 holes (Assuming symmetry with outer vertical holes)
# Select the bottom face (<Z direction)
result = (
    result.faces("<Z").workplane()
    .pushPoints([
        (-hole_spacing, hole_y_pos), 
        (hole_spacing, hole_y_pos)
    ])
    .hole(hole_dia)
)