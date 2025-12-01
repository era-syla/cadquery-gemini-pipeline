import cadquery as cq

# Parameters for the hexagonal flange
thickness = 10.0
outer_diameter = 120.0    # Circumscribed diameter of the hexagon (corner-to-corner)
center_hole_dia = 50.0
bolt_circle_dia = 90.0
bolt_hole_dia = 8.0
fillet_radius = 8.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create basic hexagonal shape
    .polygon(nSides=6, diameter=outer_diameter)
    .extrude(thickness)
    # Apply fillets to the vertical edges (corners of the hexagon)
    .edges("|Z")
    .fillet(fillet_radius)
    # Select the top face to cut holes
    .faces(">Z")
    .workplane()
    # Cut the central large hole
    .hole(center_hole_dia)
    # Create the pattern for mounting holes
    .polarArray(radius=bolt_circle_dia/2.0, startAngle=0, angle=360, count=6)
    # Cut the mounting holes
    .hole(bolt_hole_dia)
)