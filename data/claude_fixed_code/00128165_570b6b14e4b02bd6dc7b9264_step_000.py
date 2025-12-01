import cadquery as cq

width = 80
height = 50
thickness = 5
length = 100

# Base Part
base = cq.Workplane("XY").box(length, width, thickness).translate((0, 0, 0))
base = base.union(cq.Workplane("XY").box(length, thickness, height).translate((0, width/2, -height/2+thickness/2)))

# Additional part
extra_width = 10
extra_length = 20
extra_height = 5
extra_offset_x = 25
extra_offset_y = -10

extra_part = cq.Workplane("XY").box(extra_length, extra_width, extra_height).translate((extra_offset_x, width/2+extra_offset_y, -height+extra_height/2))

# Arm
arm_length = 25
arm_thickness = 2
arm_width = 5

arm = cq.Workplane("XY").box(arm_length, arm_thickness, arm_width).rotate((0,0,0),(0,0,1),90).translate((extra_offset_x+extra_length/2, width/2-extra_offset_y+arm_width*3, -height+thickness*2))
arm = arm.union(cq.Workplane("XY").circle(arm_width/2).extrude(arm_thickness).translate((extra_offset_x+extra_length/2+arm_length, width/2-extra_offset_y+arm_width*3, -height+thickness*2)))
arm = arm.union(cq.Workplane("XY").circle(arm_width/2).extrude(arm_thickness).translate((extra_offset_x+extra_length/2-arm_length/2, width/2-extra_offset_y+arm_width*3, -height+thickness*2)))

# Vertical support
support_width = 10
support_height = 20
support_thickness = 2

support = cq.Workplane("XY").box(support_width, support_thickness, support_height).translate((extra_offset_x+extra_length, width/2-extra_offset_y+support_thickness, -height/2))
support = support.union(cq.Workplane("XY").circle(support_thickness/2).extrude(support_width).translate((extra_offset_x+extra_length, width/2-extra_offset_y+support_thickness+support_width/2, -height+support_height)))

# Connect arm to support
connector_radius = 2.5
connector_thickness = 2

connector = cq.Workplane("XY").circle(connector_radius).extrude(connector_thickness).translate((extra_offset_x+extra_length/2-arm_length/2+5, width/2-extra_offset_y+arm_width*3, -height+thickness*2))

result = base.union(extra_part).union(arm).union(support).union(connector)