import cadquery as cq

# Parametric dimensions
cylinder_height = 50.0
cylinder_diameter = 50.0
hole_diameter = 15.0
chamfer_width = 3.0

# Calculate countersink diameter based on hole diameter and desired chamfer width
# A 90-degree countersink angle results in a 45-degree chamfer
csk_diameter = hole_diameter + (2 * chamfer_width)

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(cylinder_diameter / 2.0)
    .extrude(cylinder_height)
    .faces(">Z")
    .workplane()
    .cskHole(hole_diameter / 2.0, csk_diameter / 2.0, 90.0)
)