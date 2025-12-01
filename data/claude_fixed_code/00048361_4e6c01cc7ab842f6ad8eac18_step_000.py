import cadquery as cq

# The image shows a simple rectangular prism or cube with no holes, fillets, or chamfers.
# Since no dimensions are provided, we will assume a uniform cube of size 10.

length = 10.0
width = 10.0
height = 10.0

# Create a box centered at the origin on the XY plane
result = cq.Workplane("XY").box(length, width, height)