import cadquery as cq

# Parametric dimensions
plate_length = 100.0
plate_width = 80.0
plate_height = 5.0
hole_diameter = 4.0
corner_radius = 5.0

# Define the points for the plate outline
points = [
    (0, 0),
    (plate_length, 0),
    (plate_length, plate_width),
    (plate_length/2, plate_width),
    (0, plate_width/2)
]

# Create the plate outline using a polygon
plate = cq.Workplane("XY").polyline(points).close()

# Extrude the plate to create the solid
plate_solid = plate.extrude(plate_height)

# Define hole locations
hole_locations = [
    (-10, 10),
    (10, 10),
    (-10, 30),
    (10, 30),
    (-10, 50),
    (10, 50),
    (plate_length - 10, 10),
    (plate_length - 30, 10),
    (plate_length - 10, plate_width - 10),
    (plate_length - 30, plate_width - 10),
    (plate_length/2-10, plate_width - 10),
    (plate_length/2+10, plate_width - 10),
    (plate_length/2, plate_width - 30),
    (0,0),
    (plate_length,0),
    (0,plate_width/2),
    (plate_length, plate_width)
]

# Create holes
for x, y in hole_locations:
    plate_solid = plate_solid.faces(">Z").workplane().center(x, y).hole(hole_diameter)

# Add corner fillets
result = plate_solid.edges("|Z").fillet(corner_radius)