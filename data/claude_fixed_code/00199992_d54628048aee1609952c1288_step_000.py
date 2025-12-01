import cadquery as cq

# Parametric dimensions
chip_length = 25.0
chip_width = 7.5
chip_height = 3.0
notch_width = 2.5
notch_depth = 1.0
pin_count = 12
pin_spacing = 2.54
pin_width = 0.7
pin_length = 10.0
pin_offset = 1.25

# Create the main body
chip_body = cq.Workplane("XY").box(chip_length, chip_width, chip_height)

# Create the notch
notch = cq.Workplane("XY").workplane(offset=chip_height).center(chip_length/2 - notch_width/2, chip_width/2).rect(notch_width, notch_depth).extrude(-chip_height)

# Cut the notch from the body
chip_body = chip_body.cut(notch)

# Create a function to generate a single pin
def create_pin(x_pos):
    pin = cq.Workplane("XY").workplane(offset=-pin_length).rect(pin_width, pin_width).extrude(pin_length)
    pin = pin.translate((x_pos, chip_width/2 - pin_offset, 0))
    return pin

# Create the pins
pins = None
for i in range(pin_count):
    x_pos = -chip_length/2 + (i * pin_spacing) + (pin_spacing/2)
    pin = create_pin(x_pos)
    if pins is None:
        pins = pin
    else:
        pins = pins.union(pin)

pins2 = None
for i in range(pin_count):
    x_pos = -chip_length/2 + (i * pin_spacing) + (pin_spacing/2)
    pin = create_pin(x_pos)
    pin = pin.rotate((0,0,0),(0,0,1),180)
    if pins2 is None:
        pins2 = pin
    else:
        pins2 = pins2.union(pin)


# Combine the body and pins
result = chip_body.union(pins).union(pins2)