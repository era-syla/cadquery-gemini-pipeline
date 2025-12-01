import cadquery as cq

base_length = 80.0
base_width = 60.0
base_height = 10.0
column_height = 80.0
column_width = 10.0
arm_length = 100.0
arm_radius = 10.0
handle_length = 50.0
handle_radius = 3.0

# Base
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Column
column = cq.Workplane("XY").workplane(offset=base_height).box(column_width, column_width, column_height)

# Main body
main_body = (
    cq.Workplane("XY")
    .workplane(offset=base_height + column_height)
    .circle(arm_radius * 1.5)
    .extrude(column_width)
    .faces(">Z")
    .circle(arm_radius * 1.2)
    .cutThruAll()
)

# Arm
arm = (
    cq.Workplane("YZ")
    .workplane(offset=-arm_length)
    .circle(arm_radius)
    .extrude(arm_length)
    .translate((0, base_height + column_height, 0))
)

# Handle
handle = (
    cq.Workplane("XY")
    .workplane(offset=base_height + column_height + column_width/2)
    .circle(arm_radius * 2.0)
    .extrude(column_width/2)
    .faces("<Z")
    .workplane()
    .hole(arm_radius)
)

handle_rod = (
    cq.Workplane("YZ")
    .workplane(offset=-arm_length)
    .circle(handle_radius)
    .extrude(handle_length)
    .translate((0, base_height + column_height, -arm_length))
)

handle_head = (
    cq.Workplane("YZ")
    .workplane(offset=-arm_length - handle_length)
    .circle(handle_radius * 2)
    .extrude(handle_radius)
    .translate((0, base_height + column_height, 0))
)


# Combine all parts
result = base.union(column).union(main_body).union(arm).union(handle).union(handle_rod).union(handle_head)