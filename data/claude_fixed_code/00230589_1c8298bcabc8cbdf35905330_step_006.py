import cadquery as cq

# Geometric parameters
plate_length = 100.0
plate_width = 100.0
plate_thickness = 10.0
hole_diameter = 5.0
hole_margin = 12.0  # Distance from the edge to the center of the hole

# Create the 3D model
result = (
    cq.Workplane("XY")
    # Create the base rectangular plate centered at the origin
    .box(plate_length, plate_width, plate_thickness, centered=(True, True, False))
    # Select the top face to perform the cut
    .faces(">Z")
    .workplane()
    # Position the hole: centered in X, offset in Y towards the edge
    .pushPoints([(0, -plate_width / 2 + hole_margin)])
    # Cut the hole through the plate
    .hole(hole_diameter)
)