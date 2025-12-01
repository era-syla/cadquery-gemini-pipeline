import cadquery as cq

# Object dimensions
width = 50.0
length = 50.0
height = 20.0

# Cut dimensions
# A sphere radius slightly larger than the height creates the through-hole effect
# when centered at the top face.
sphere_radius = 20.5 

# 1. Create the base block
# We center x and y, but align z=0 to the bottom for easier vertical positioning
base = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# 2. Create the sphere for subtraction
# The sphere is positioned at the center of the top face (0, 0, height)
sphere_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .sphere(sphere_radius)
    .translate((0, 0, height))
)

# 3. Apply the boolean cut to create the spherical void
result = base.cut(sphere_cut)