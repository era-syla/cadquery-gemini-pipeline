import cadquery as cq

# Disk parameters
disk_radius = 25
disk_thickness = 2
disk_inner_radius = 5

# Plate parameters
plate_width = 20
plate_height = 30
plate_thickness = 3
plate_notch_width = 10
plate_notch_height = 5

# Create the disk
disk = cq.Workplane("XY").circle(disk_radius).extrude(disk_thickness)
disk = disk.faces(">Z").workplane().circle(disk_inner_radius).cutThruAll()

# Create the plate
plate = cq.Workplane("XY").rect(plate_width, plate_height).extrude(plate_thickness)
plate = plate.faces("<Z").workplane().rect(plate_notch_width, plate_notch_height).cutThruAll()

# Translate the disk to position it above the plate
disk = disk.translate((0, 0, 40))

# Combine the shapes
result = disk.union(plate)