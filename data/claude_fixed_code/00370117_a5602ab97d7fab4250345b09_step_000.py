import cadquery as cq

# Parameters
outer_diameter_bottom = 15
outer_diameter_middle = 15
outer_diameter_top = 10
inner_diameter_top = 7
height_bottom = 20
height_middle = 20
height_top = 20


# Create the bottom cylinder
bottom_cylinder = cq.Workplane("XY").circle(outer_diameter_bottom/2).extrude(height_bottom)

# Create the middle cylinder
middle_cylinder = cq.Workplane("XY").circle(outer_diameter_middle/2).extrude(height_middle)

# Create the top cylinder with the inner hole
top_cylinder = (cq.Workplane("XY")
                 .circle(outer_diameter_top/2)
                 .extrude(height_top)
                 .faces(">Z")
                 .circle(inner_diameter_top/2)
                 .cutThruAll())

# Assemble the cylinders
result = (bottom_cylinder
          .union(middle_cylinder.translate((0, 0, height_bottom)))
          .union(top_cylinder.translate((0, 0, height_bottom + height_middle))))


#show_object(result)