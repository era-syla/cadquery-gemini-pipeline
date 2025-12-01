import cadquery as cq

# Parameters defining the dimensions of the block
length = 50.0  # Dimension along the X axis
width = 50.0   # Dimension along the Y axis
height = 15.0  # Dimension along the Z axis

# Create a simple rectangular box
# centered=True is the default, placing the center of mass at (0,0,0)
result = cq.Workplane("XY").box(length, width, height, centered=True)