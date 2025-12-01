import cadquery as cq

# Parameters
block_width = 50.0
block_height = 40.0
block_depth = 60.0
hole_diameter = 20.0
bolt_circle_radius = 30.0
bolt_hole_diameter = 5.0
num_bolts = 8
clamp_diameter = 25.0
clamp_width = 25.0
clamp_height = 15.0
tab_width = 10.0
tab_height = 5.0
tab_hole_diameter = 3.0

# Create the main block
result = cq.Workplane("XY")\
    .box(block_width, block_depth, block_height)\
    .faces(">Z").workplane()\
    .hole(hole_diameter)\
    .faces(">X").workplane()\
    .polarArray(bolt_circle_radius, 0, 360, num_bolts)\
    .hole(bolt_hole_diameter)

# Create the clamp
clamp = cq.Workplane("XY")\
    .center(block_width/2 + clamp_width/2, 0)\
    .box(clamp_width, block_depth, clamp_height)\
    .faces(">Z").workplane()\
    .circle(clamp_diameter/2)\
    .cutThruAll()

# Create the clamp top
clamp_top = cq.Workplane("XY")\
    .center(block_width/2 + clamp_width/2, 0)\
    .box(clamp_width, block_depth, clamp_height)\
    .translate((0, 0, block_height - clamp_height))\
    .faces("<Z").workplane()\
    .circle(clamp_diameter/2)\
    .cutThruAll()

# Create the tab
tab = cq.Workplane("XY")\
    .center(block_width/2 + clamp_width + tab_width/2, 0)\
    .box(tab_width, block_depth, tab_height)\
    .translate((0, 0, block_height - tab_height))\
    .faces(">Z").workplane()\
    .hole(tab_hole_diameter)

# Combine the parts
result = result.union(clamp)
result = result.union(clamp_top)
result = result.union(tab)