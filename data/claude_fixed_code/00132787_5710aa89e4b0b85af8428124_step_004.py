import cadquery as cq

# Parametric dimensions
box_width = 50
box_length = 80
box_height = 60
leg_diameter = 4
leg_height = 10
leg_offset_x = 10
leg_offset_y = 15

# Create the main box
box = cq.Workplane("XY").box(box_width, box_length, box_height)

# Create the legs
leg1 = cq.Workplane("XY").moveTo(box_width/2 - leg_offset_x, box_length/2 - leg_offset_y).circle(leg_diameter/2).extrude(leg_height)
leg2 = cq.Workplane("XY").moveTo(-box_width/2 + leg_offset_x, box_length/2 - leg_offset_y).circle(leg_diameter/2).extrude(leg_height)
leg3 = cq.Workplane("XY").moveTo(box_width/2 - leg_offset_x, -box_length/2 + leg_offset_y).circle(leg_diameter/2).extrude(leg_height)
leg4 = cq.Workplane("XY").moveTo(-box_width/2 + leg_offset_x, -box_length/2 + leg_offset_y).circle(leg_diameter/2).extrude(leg_height)

# Translate the legs to the correct position under the box
leg1 = leg1.translate((0,0,-box_height/2 - leg_height/2))
leg2 = leg2.translate((0,0,-box_height/2 - leg_height/2))
leg3 = leg3.translate((0,0,-box_height/2 - leg_height/2))
leg4 = leg4.translate((0,0,-box_height/2 - leg_height/2))

# Combine the box and the legs
result = box.union(leg1).union(leg2).union(leg3).union(leg4)