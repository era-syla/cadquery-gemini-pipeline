import cadquery as cq

# Object dimensions
width = 50.0       # Total width of the profile
height = 30.0      # Height of the peaks
length = 50.0      # Extrusion length
thickness = 6.0    # Thickness of the wall
fillet_radius = 5.0 # Radius of the curves

# Define the points for the centerline of the 'M' profile
# Coordinates are defined relative to the center of the base
pts = [
    (-width/2, 0),               # Bottom Left
    (-width/4, height),          # Top Left Peak
    (0, height * 0.3),           # Middle Valley (slightly raised)
    (width/4, height),           # Top Right Peak
    (width/2, 0)                 # Bottom Right
]

# Generate the 3D object
result = (
    cq.Workplane("XY")
    .spline(pts)
    .offset(thickness / 2)
    .extrude(length)
)