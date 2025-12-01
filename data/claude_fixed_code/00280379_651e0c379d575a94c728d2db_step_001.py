import cadquery as cq

# Parametric dimensions
plate_length = 80
plate_width = 40
plate_thickness = 5
hole_diameter = 8
pin_diameter = 12
pin_height = 30
lever_diameter = 5
lever_length = 50

# Create the base plate
base_plate = cq.Workplane("XY").rect(plate_length, plate_width).extrude(plate_thickness)

# Create the top plate with hook
hook_width = 20
hook_height = 15
top_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .center(plate_length / 2, 0)
    .lineTo(hook_width, 0)
    .lineTo(hook_width, hook_height)
    .lineTo(0, hook_height)
    .close()
    .extrude(plate_thickness)
)

# Create the pin
pin = cq.Workplane("XY").circle(pin_diameter / 2).extrude(pin_height)

# Create the lever
lever = cq.Workplane("XY").circle(lever_diameter / 2).extrude(lever_length)

# Create the holes
hole = cq.Workplane("XY").circle(hole_diameter / 2).extrude(plate_thickness)

# Assemble the parts
assembly = (
    cq.Assembly()
    .add(base_plate, name="base_plate")
    .add(top_plate, name="top_plate", loc=cq.Location((0, plate_width + pin_diameter, pin_height + plate_thickness)))
    .add(pin, name="pin1", loc=cq.Location((plate_length / 4, plate_width / 2, plate_thickness)))
    .add(pin, name="pin2", loc=cq.Location((3 * plate_length / 4, plate_width / 2, plate_thickness)))
    .add(pin, name="pin3", loc=cq.Location((plate_length / 4, plate_width / 2 + plate_width + pin_diameter, pin_height + plate_thickness + plate_thickness)))
    .add(pin, name="pin4", loc=cq.Location((3 * plate_length / 4, plate_width / 2 + plate_width + pin_diameter, pin_height + plate_thickness + plate_thickness)))
    .add(lever, name="lever", loc=cq.Location((plate_length, plate_width / 2 , plate_thickness)))
)

result = assembly.toCompound()