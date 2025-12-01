import cadquery as cq

# Dimensions estimated from the image
# The object is a cylindrical bushing or spacer.
outer_diameter = 40.0
height = 60.0
hole_diameter = 12.0

# Calculate radius for the circle creation
outer_radius = outer_diameter / 2.0

# Generate the 3D object
# 1. Start on the XY plane
# 2. Draw the outer circle
# 3. Extrude to create the main cylinder
# 4. Select the top face (>Z)
# 5. Create a hole through the entire part
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)