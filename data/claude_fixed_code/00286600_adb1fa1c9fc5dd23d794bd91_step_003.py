import cadquery as cq

# Parametric dimensions
height = 100.0
radius = 20.0

# Create the cylinder
# We start on the XY plane, draw a circle, and extrude it upwards to create a cylinder.
result = cq.Workplane("XY").circle(radius).extrude(height)

# Display the result
show_object(result)