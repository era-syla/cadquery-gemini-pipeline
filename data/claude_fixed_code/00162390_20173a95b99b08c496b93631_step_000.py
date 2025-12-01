import cadquery as cq

# Dimensions estimated from the image geometry
# The part consists of a flanged base and a central cylindrical boss.
base_diameter = 20.0
base_height = 5.0
top_diameter = 12.0
top_height = 15.0

# Create the 3D object
result = (
    cq.Workplane("XY")
    # Create the base cylinder (flange)
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    # Create the top cylinder (boss)
    .circle(top_diameter / 2.0)
    .extrude(top_height)
)