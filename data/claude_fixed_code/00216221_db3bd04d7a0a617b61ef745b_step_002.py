import cadquery as cq

# Object dimensions based on visual analysis
width = 100.0
height = 150.0
thickness = 3.0
hole_diameter = 5.0

# Hole positioning
# Holes are located on the left side of the plate
# Coordinates are relative to the center of the face (0,0)
hole_x_offset = -(width / 2) + 20.0  # 20mm margin from the left edge

# Bottom hole position (near the corner)
hole_y_bottom = -(height / 2) + 20.0 # 20mm margin from the bottom edge

# Middle hole position
# Visually appears to be slightly above the vertical geometric center
hole_y_mid = 15.0 

# Create the object
# Oriented on the XZ plane to match the upright isometric view in the image
result = (
    cq.Workplane("XZ")
    .box(width, height, thickness)
    .faces(">Y")  # Select the front face (normal to Y-axis)
    .workplane()
    .pushPoints([
        (hole_x_offset, hole_y_bottom),
        (hole_x_offset, hole_y_mid)
    ])
    .circle(hole_diameter / 2)
    .cutThruAll()
)