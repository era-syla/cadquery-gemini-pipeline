import cadquery as cq

width = 60
length = 80
height = 10
round_radius = 5
support_width = 10
support_height = 5
support_offset = 15
pin_diameter = 10
pin_length = 10

# Create the base
base = cq.Workplane("XY").box(length, width, height)

# Round the edges
base = base.edges("|Z").fillet(round_radius)

# Add the supports
support1 = cq.Workplane("XY").center(support_offset, 0)\
    .box(support_width, width, support_height).translate((0, 0, height/2 + support_height/2))

support2 = cq.Workplane("XY").center(-support_offset, 0)\
    .box(support_width, width, support_height).translate((0, 0, height/2 + support_height/2))

base = base.union(support1).union(support2)

# Add the pin
pin = cq.Workplane("YZ").center(0, height/2)\
    .circle(pin_diameter/2).extrude(pin_length)
pin = pin.translate((length/2, 0, 0))

base = base.union(pin)

result = base