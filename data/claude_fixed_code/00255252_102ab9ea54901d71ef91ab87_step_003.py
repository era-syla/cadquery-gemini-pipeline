import cadquery as cq

# Parametric dimensions
cyl_height = 60.0
cyl_radius = 4.0
spacing_x = 50.0
spacing_y = 50.0

# Create the model: 4 cylinders arranged in a rectangular pattern
result = (
    cq.Workplane("XY")
    .rarray(spacing_x, spacing_y, 2, 2)
    .circle(cyl_radius)
    .extrude(cyl_height)
)