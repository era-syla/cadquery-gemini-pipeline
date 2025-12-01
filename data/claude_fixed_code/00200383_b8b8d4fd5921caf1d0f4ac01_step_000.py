import cadquery as cq

# The image shows a simple 3D sphere.
# Since no specific dimensions are provided, a default radius is used.
radius = 10.0

# Create the sphere centered at the origin
result = cq.Workplane("XY").sphere(radius)