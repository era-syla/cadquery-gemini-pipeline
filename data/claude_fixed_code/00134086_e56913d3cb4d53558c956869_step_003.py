import cadquery as cq

# Parameters
outer_diameter = 20.0
inner_diameter = 10.0
height = 25.0

# Create the solid
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height) \
    .faces(">Z").workplane().circle(inner_diameter / 2.0).cutThruAll()