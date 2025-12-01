import cadquery as cq

# Parameters based on standard 2020 series extrusion joining plate dimensions
thickness = 4.0
side_length = 60.0
hole_diameter = 5.0
chamfer_size = 3.0

# 1. Create the base triangle shape
# We model it initially as a right-angled triangle at the origin (0,0)
# Vertices: (0,0), (60,0), (0,60)
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (side_length, 0), (0, side_length)])
    .close()
    .extrude(thickness)
)

# 2. Chamfer the corners
# Apply chamfer to the vertical edges to create the flattened tips seen in the image
result = result.edges("|Z").chamfer(chamfer_size)

# 3. Create the holes
# The 5-hole pattern creates a 'V' shape.
# Defined here relative to the unrotated L-shape (10mm margin, 20mm spacing)
hole_locations = [
    (10, 10),           # Corner hole
    (30, 10), (50, 10), # Holes along X axis
    (10, 30), (10, 50)  # Holes along Y axis
]

for loc in hole_locations:
    result = result.faces(">Z").workplane().center(loc[0], loc[1]).hole(hole_diameter)

# 4. Rotate to match image orientation
# Rotate 45 degrees around Z axis so the 90-degree corner points down
# and the hypotenuse forms a horizontal top edge.
result = result.rotate((0, 0, 0), (0, 0, 1), 45)