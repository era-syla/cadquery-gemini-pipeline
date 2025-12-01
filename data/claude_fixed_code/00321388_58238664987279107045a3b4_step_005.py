import cadquery as cq

# Parameters
thickness = 3
arm_length = 30
arm_width = 15
center_hole_radius = 5
outer_hole_radius = 8


# Create the basic arm shape
arm = cq.Workplane("XY").box(arm_length, arm_width, thickness)
arm = arm.faces(">Z").workplane().center(arm_length/2, 0).circle(outer_hole_radius).cutThruAll()
arm = arm.faces(">Z").workplane().center(-arm_length/2, 0).circle(outer_hole_radius).cutThruAll()


# Create the center hole
center_hole = cq.Workplane("XY").circle(center_hole_radius).extrude(thickness)

# Assemble the final shape
result = arm
result = result.union(arm.rotate((0,0,0),(0,0,1), 120))
result = result.union(arm.rotate((0,0,0),(0,0,1), 240))
result = result.cut(center_hole)


# Display the result
#show_object(result)