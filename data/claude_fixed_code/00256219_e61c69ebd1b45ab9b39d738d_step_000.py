import cadquery as cq

# --- Parameter Definitions ---
# Main Chassis Dimensions
length = 90.0
width = 30.0
chassis_height = 12.0

# Cab Dimensions
cab_length = 32.0
cab_height = 28.0
windshield_chamfer = 8.0

# Bed Dimensions
bed_length = length - cab_length
bed_height = 15.0
bed_wall_thickness = 3.0
bed_internal_depth = 10.0

# Wheel Dimensions
wheel_radius = 11.0
wheel_thickness = 6.0
axle_radius = 2.5
axle_length = wheel_thickness + 2.0
wheel_base_offset = 20.0 # Distance from ends to axles
z_axle_offset = -2.0 # Vertical position of axle relative to chassis center

# --- Geometry Construction ---

# 1. Base Chassis
chassis = cq.Workplane("XY").box(length, width, chassis_height)

# 2. Truck Cab
cab_center_x = -length/2 + cab_length/2
cab_center_z = chassis_height/2 + cab_height/2

cab = (cq.Workplane("XY")
       .workplane(offset=cab_center_z)
       .center(cab_center_x, 0)
       .box(cab_length, width, cab_height)
       )

# Chamfer the top-front edge for the windshield
cab = cab.edges("|Z and <X").chamfer(windshield_chamfer)

# 3. Cargo Bed
bed_center_x = length/2 - bed_length/2
bed_center_z = chassis_height/2 + bed_height/2

bed_block = (cq.Workplane("XY")
             .workplane(offset=bed_center_z)
             .center(bed_center_x, 0)
             .box(bed_length, width, bed_height)
             )

# Cut the interior of the bed
bed_cutout = (cq.Workplane("XY")
              .workplane(offset=chassis_height/2 + bed_height)
              .center(bed_center_x, 0)
              .rect(bed_length - 2*bed_wall_thickness, width - 2*bed_wall_thickness)
              .extrude(-bed_internal_depth)
              )

bed = bed_block.cut(bed_cutout)

# Add decorative indentations to bed sides
detail_width = (bed_length - 4*bed_wall_thickness) / 3
detail_height = bed_height - 6.0
detail_cut_depth = 1.0

detail_centers = []
start_x = bed_center_x - bed_length/2 + bed_wall_thickness + detail_width/2
for i in range(3):
    x = start_x + i * (detail_width + bed_wall_thickness/2)
    detail_centers.append(x)

for side_sign in [1, -1]:
    for x in detail_centers:
        cut_tool = (cq.Workplane("XZ")
                    .workplane(offset=side_sign * width/2)
                    .center(x, bed_center_z)
                    .rect(detail_width, detail_height)
                    .extrude(-side_sign * detail_cut_depth)
                    )
        bed = bed.cut(cut_tool)

# 4. Assemble Main Body
body = chassis.union(cab).union(bed)

# 5. Wheels
wheel_master = (cq.Workplane("XY")
                .circle(wheel_radius)
                .extrude(wheel_thickness)
                .faces(">Z").edges().fillet(1.5)
                )

axle_hub = (cq.Workplane("XY")
            .circle(axle_radius)
            .extrude(axle_length)
            .translate((0,0,-1))
            )
wheel_assembly = wheel_master.union(axle_hub)

# Position Wheels
front_axle_x = cab_center_x
rear_axle_x = bed_center_x

wheel_configs = [
    (front_axle_x, width/2, -90),
    (front_axle_x, -width/2, 90),
    (rear_axle_x, width/2, -90),
    (rear_axle_x, -width/2, 90),
]

wheels_union = None
for (x, y, rot) in wheel_configs:
    w = wheel_assembly.rotate((0,0,0), (1,0,0), rot).translate((x, y, z_axle_offset))
    
    if wheels_union is None:
        wheels_union = w
    else:
        wheels_union = wheels_union.union(w)

# 6. Bumpers / Magnets
front_bumper = (cq.Workplane("YZ")
                .circle(3.5)
                .extrude(3.0)
                .translate((-length/2 - 3.0, 0, -chassis_height/4))
                )

rear_bumper = (cq.Workplane("YZ")
               .circle(4.5)
               .extrude(2.0)
               .faces(">X").edges().fillet(1.0)
               .translate((length/2, 0, -chassis_height/4))
               )

# --- Final Assembly ---
result = body.union(wheels_union).union(front_bumper).union(rear_bumper)