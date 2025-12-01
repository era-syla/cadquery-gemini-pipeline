import cadquery as cq

# Dimensions based on visual analysis of a standard electret microphone capsule
body_diameter = 10.0
body_radius = body_diameter / 2.0
body_height = 6.0
wall_thickness = 0.4
rim_thickness = 0.4
pin_diameter = 0.6
pin_length = 4.0
pcb_recess = 0.5  # Depth of the PCB face from the back rim
pcb_thickness = 1.5

# 1. Main Housing (Cylindrical shell)
# Created by extruding a cylinder and cutting a blind hole from the back (-Z)
housing = (
    cq.Workplane("XY")
    .circle(body_radius)
    .extrude(body_height)
    .faces("<Z")
    .workplane()
    .circle(body_radius - wall_thickness)
    .cutBlind(-(body_height - 0.5))  # Leave 0.5mm for the front face
)

# 2. PCB Insert (Backplate)
# A disc positioned inside the housing recess
pcb = (
    cq.Workplane("XY")
    .circle(body_radius - wall_thickness - 0.05) # Slight tolerance gap
    .extrude(pcb_thickness)
    .translate((0, 0, pcb_recess))
)

# 3. Connector Pins
# Three pins protruding from the PCB face outwards (-Z direction)
# Locations estimated: Top (Signal), Middle (Reference/Power), Bottom (Ground)
pin_locations = [(0, 1.8), (0, -0.2), (0, -3.0)]

pins = (
    cq.Workplane("XY")
    .pushPoints(pin_locations)
    .circle(pin_diameter / 2.0)
    .extrude(-pin_length)
    .translate((0, 0, pcb_recess))
)

# 4. Rim Crimps
# Small deformations on the casing rim to hold the PCB in place
# Located at 45, 135, 225, 315 degrees
crimps = cq.Workplane("XY")
for angle in [45, 135, 225, 315]:
    import math
    x = (body_radius - wall_thickness/2.0) * math.cos(math.radians(angle))
    y = (body_radius - wall_thickness/2.0) * math.sin(math.radians(angle))
    crimp = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(0.4)
        .extrude(0.5)
    )
    if angle == 45:
        crimps = crimp
    else:
        crimps = crimps.union(crimp)

# 5. Text Markings ("M" and "G")
# Engraved into the PCB surface
# Note: Text creation generates a solid which we will cut later
text_m = (
    cq.Workplane("XY")
    .center(0, 3.5)
    .text("M", 1.4, -0.2)
    .translate((0, 0, pcb_recess))
)

text_g = (
    cq.Workplane("XY")
    .center(0, -4.2)
    .text("G", 1.4, -0.2)
    .translate((0, 0, pcb_recess))
)

# 6. Final Assembly
# Union the parts and cut the text
result = housing.union(pcb).union(pins).union(crimps)
result = result.cut(text_m).cut(text_g)