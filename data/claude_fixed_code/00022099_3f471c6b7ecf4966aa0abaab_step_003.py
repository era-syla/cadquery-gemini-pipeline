import cadquery as cq

# Dimensions estimated from image analysis
disk_diameter = 100.0
disk_thickness = 15.0
boss_diameter = 35.0
boss_height = 4.0
center_hole_diameter = 15.0
mount_hole_diameter = 12.0
mount_pcd = 70.0  # Pitch Circle Diameter for mounting holes

# 1. Create the main base disk
# Start on the XY plane and extrude the main cylinder
result = cq.Workplane("XY").circle(disk_diameter / 2.0).extrude(disk_thickness)

# 2. Cut the mounting holes
# Select the top face of the disk to position the holes
# We do this before adding the boss to easily select the main flat surface
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=mount_pcd / 2.0, startAngle=0, angle=360, count=4)
    .circle(mount_hole_diameter / 2.0)
    .cutThruAll()
)

# 3. Add the central boss
# Select the top face (Z max) again. Extrude the boss upwards.
result = (
    result.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)

# 4. Cut the central hole
# Select the new top face (top of the boss) and cut through the entire assembly
# Depth is total thickness + boss height + slight margin to ensure clean cut
result = (
    result.faces(">Z")
    .workplane()
    .circle(center_hole_diameter / 2.0)
    .cutThruAll()
)