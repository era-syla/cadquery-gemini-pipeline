import cadquery as cq

# Object Dimensions
length = 200.0
width = 30.0
thickness = 6.0

# Hole Dimensions (Counterbored)
hole_diameter = 5.0        # Through-hole diameter
cbore_diameter = 10.0      # Counterbore diameter
cbore_depth = 2.5          # Depth of the counterbore

# Hole Spacing (Distance between centers)
x_spacing = length - 20.0  # 10mm margin from ends
y_spacing = width - 10.0   # 5mm margin from edges

# Create the part
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-x_spacing/2, -y_spacing/2),
        (x_spacing/2, -y_spacing/2),
        (-x_spacing/2, y_spacing/2),
        (x_spacing/2, y_spacing/2)
    ])
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)