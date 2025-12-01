import cadquery as cq

# The image shows a simple cube with no visible additional features like holes or fillets.
# Since no specific dimensions are provided, we will create a cube with equal side lengths.
side_length = 10.0

# Create a box (cube) centered at the origin
result = cq.Workplane("XY").box(side_length, side_length, side_length)