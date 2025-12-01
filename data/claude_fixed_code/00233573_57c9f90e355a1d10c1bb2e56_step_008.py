import cadquery as cq

# --- Parameter Definitions ---
# Dimensions estimated from the visual proportions of the image
plate_thickness = 8.0
plate_base_radius = 24.0

# Lobe (the protruding ears) parameters
lobe_count = 5
lobe_radius = 10.0
lobe_offset = 26.0  # Distance from center to the center of the lobe circles

# Pin parameters
pin_radius = 4.0
pin_height = 12.0

# Central hole pattern parameters
hole_count = 8
hole_pattern_radius = 10.0
hole_radius = 0.8

# --- Geometry Construction ---

# 1. Create the main plate
# We start with the central circular disk
base_disk = cq.Workplane("XY").circle(plate_base_radius).extrude(plate_thickness)

# Create the lobes. We generate them as separate cylinders and union them.
# startAngle=90 places the first lobe at the "top" (12 o'clock) position to match the image.
lobes = cq.Workplane("XY")
for i in range(lobe_count):
    angle = 90 + i * (360 / lobe_count)
    x = lobe_offset * cq.Vector(1, 0, 0).rotateZ(angle * 3.14159 / 180).x
    y = lobe_offset * cq.Vector(1, 0, 0).rotateZ(angle * 3.14159 / 180).y
    lobe = cq.Workplane("XY").center(x, y).circle(lobe_radius).extrude(plate_thickness)
    base_disk = base_disk.union(lobe)

# Combine the base disk and the lobes to form the complete base shape
plate_body = base_disk

# 2. Add the pins
# The pins are extruded from the top surface of the plate at the lobe locations
for i in range(lobe_count):
    angle = 90 + i * (360 / lobe_count)
    x = lobe_offset * cq.Vector(1, 0, 0).rotateZ(angle * 3.14159 / 180).x
    y = lobe_offset * cq.Vector(1, 0, 0).rotateZ(angle * 3.14159 / 180).y
    pin = cq.Workplane("XY").workplane(offset=plate_thickness).center(x, y).circle(pin_radius).extrude(pin_height)
    plate_body = plate_body.union(pin)

# Union the pins to the main body
body_with_pins = plate_body

# 3. Create the central hole pattern
# We select the top face of the result and cut the pattern of small holes through the part
result = body_with_pins
for i in range(hole_count):
    angle = i * (360 / hole_count)
    x = hole_pattern_radius * cq.Vector(1, 0, 0).rotateZ(angle * 3.14159 / 180).x
    y = hole_pattern_radius * cq.Vector(1, 0, 0).rotateZ(angle * 3.14159 / 180).y
    result = result.faces(">Z").workplane().center(x, y).circle(hole_radius).cutThruAll()