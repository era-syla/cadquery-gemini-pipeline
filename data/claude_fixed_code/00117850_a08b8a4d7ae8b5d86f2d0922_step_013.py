import cadquery as cq

# Parametric dimensions
plate_width = 50
plate_height = 50
plate_thickness = 5
hole_size = 5
hole_offset = 7.5

# Create the base plate
plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Create the hole
hole = cq.Workplane("XY").center(-plate_width/2 + hole_offset, plate_height/2 - hole_offset).box(hole_size, hole_size, plate_thickness)

# Subtract the hole from the plate
result = plate.cut(hole)