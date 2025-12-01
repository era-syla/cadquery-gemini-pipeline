import cadquery as cq

# Object Dimensions estimated from the image
head_diameter = 20.0
shaft_diameter = 10.0
head_rim_height = 2.5
taper_height = 6.0
shaft_length = 30.0
chamfer_size = 1.0

# Derived dimensions
head_radius = head_diameter / 2.0
shaft_radius = shaft_diameter / 2.0

# 1. Create the cylindrical rim of the head
# We start on the XY plane and extrude upwards
result = cq.Workplane("XY").circle(head_radius).extrude(head_rim_height)

# 2. Create the conical transition (taper)
# We select the top face of the rim, draw the base circle,
# create an offset workplane for the top of the cone, draw the target circle,
# and create a loft between them.
taper = (
    cq.Workplane("XY").workplane(offset=head_rim_height)
    .circle(head_radius)
    .workplane(offset=taper_height)
    .circle(shaft_radius)
    .loft()
)
result = result.union(taper)

# 3. Create the main shaft
# Select the small circular face at the top of the taper and extrude the shaft
shaft = (
    cq.Workplane("XY").workplane(offset=head_rim_height + taper_height)
    .circle(shaft_radius)
    .extrude(shaft_length)
)
result = result.union(shaft)

# 4. Add the chamfer at the end of the shaft
# Select the circular edge at the very top (highest Z) and apply chamfer
result = result.edges("|Z").chamfer(chamfer_size)