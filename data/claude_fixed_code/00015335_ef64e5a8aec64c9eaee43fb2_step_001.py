import cadquery as cq

# Dimensions estimated from the visual aspect ratio of the image
length = 120.0  # The long dimension
width = 30.0    # The shorter dimension
thickness = 2.0 # The thin vertical dimension

# Create a simple rectangular plate (cuboid)
# .box() centers the object at the origin
result = cq.Workplane("XY").box(length, width, thickness)