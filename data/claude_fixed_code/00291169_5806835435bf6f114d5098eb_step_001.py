import cadquery as cq

# Parametric dimensions
plate_width = 50.0
plate_height = 60.0
plate_thickness = 2.0
hole_diameter = 12.0
hole_spacing = 30.0
fillet_radius = 6.0

# Create the part
# 1. Start with a rectangular block centered on XY plane
# 2. Fillet the two vertical edges on the negative X side (left side)
# 3. Create two holes along the vertical centerline (Y-axis)
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z and <X")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .pushPoints([(0, hole_spacing / 2), (0, -hole_spacing / 2)])
    .circle(hole_diameter / 2)
    .cutThruAll()
)