import cadquery as cq

# Analyze the image:
# The object is a simple rectangular prism (a box or plate).
# It has no visible holes, chamfers, or fillets.
# The orientation suggests it is standing upright, with length > height > thickness.

# Define dimensions based on visual estimation of aspect ratios
length = 100.0   # The longest dimension (horizontal)
height = 50.0    # The vertical dimension, approx half the length
thickness = 8.0  # The thinnest dimension (depth)

# Create the 3D object
# We use the XY plane as the base. 
# To match the "standing" orientation shown in the image:
# - X axis corresponds to Length
# - Y axis corresponds to Thickness
# - Z axis corresponds to Height
# The box method creates a centered cuboid.
result = cq.Workplane("XY").box(length, thickness, height)