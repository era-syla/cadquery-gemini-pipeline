import cadquery as cq

# Parametric dimensions
width = 50
height = 25
depth = 40
slot_width = 8
slot_depth = 20
hole_diameter = 5
corner_radius = 5


# Create the base solid
result = cq.Workplane("XY").box(width, depth, height)

# Cut the slot
result = result.faces(">Z").workplane()\
    .rect(slot_width, depth-2).cutBlind(-height)

#Cut the center rectangular cutout
result = result.faces(">Z").workplane()\
    .rect(width/4, depth/2).cutBlind(-height/2)

#Add the corner fillet
result = result.edges("|Z and <X").fillet(corner_radius)

# Add the hole
result = result.faces(">X").workplane().hole(hole_diameter)