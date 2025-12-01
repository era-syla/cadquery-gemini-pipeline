import cadquery as cq

# Parametric dimensions for the bar
length = 500.0  # Total length of the bar
width = 10.0    # Width of the cross-section
height = 10.0   # Height of the cross-section

# Create the rectangular bar geometry
# Oriented along the X-axis by default
result = cq.Workplane("XY").center(0, 0).box(length, width, height)