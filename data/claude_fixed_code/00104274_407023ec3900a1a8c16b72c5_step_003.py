import cadquery as cq

# The image displays a simple rectangular cuboid (box) without any 
# visible features like holes, fillets, or chamfers.
# We will define arbitrary dimensions that approximate the visual aspect ratio.

# Estimated dimensions
length = 60.0  # X-axis dimension
width = 50.0   # Y-axis dimension
height = 25.0  # Z-axis dimension

# Create the box centered at the origin
result = cq.Workplane("XY").box(length, width, height)