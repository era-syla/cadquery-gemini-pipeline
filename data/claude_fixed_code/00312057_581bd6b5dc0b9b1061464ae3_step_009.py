import cadquery as cq

# Define parametric dimensions
radius = 10.0
height = 10.0

# Create a cylinder by drawing a circle on the XY plane and extruding it
result = cq.Workplane("XY").circle(radius).extrude(height)

# Display the result
show_object(result)