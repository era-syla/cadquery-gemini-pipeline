import cadquery as cq

# Define dimensions based on visual analysis of the image
plate_length = 140.0
plate_width = 50.0
plate_thickness = 10.0
hole_diameter = 8.0

# Hole pattern parameters
# Vertical distance from horizontal center line to the hole rows
y_offset = 12.5  

# Horizontal distances from vertical center line to the hole columns
x_inner = 40.0  # Distance to the inner columns
x_outer = 55.0  # Distance to the outer columns

# Define the coordinates for the 8 holes
# The pattern consists of two 2x2 grids separated by a central gap
points = [
    # Left group (4 holes)
    (-x_outer, y_offset), (-x_outer, -y_offset),
    (-x_inner, y_offset), (-x_inner, -y_offset),
    
    # Right group (4 holes)
    (x_inner, y_offset),  (x_inner, -y_offset),
    (x_outer, y_offset),  (x_outer, -y_offset),
]

# Generate the 3D object
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)