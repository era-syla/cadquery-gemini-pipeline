import cadquery as cq

# Define parameter values based on visual estimation of the object
# The object is a hollow cylinder with a closed bottom (cup-like shape).
height = 50.0
outer_radius = 30.0
wall_thickness = 3.0

# Create the object
# 1. Start with a solid cylinder on the XY plane.
# 2. Select the top face (in the positive Z direction).
# 3. Use the shell() command with a negative thickness to hollow out the solid from the selected face inwards.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .faces(">Z")
    .shell(wall_thickness)
)