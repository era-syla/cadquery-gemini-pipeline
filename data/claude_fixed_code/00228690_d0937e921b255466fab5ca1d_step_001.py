import cadquery as cq

# Estimated dimensions based on the visual proportions of the image
shaft_diameter = 10.0
hex_height = 8.0
shaft_length = 22.0
head_diameter = 16.0
head_height = 4.0
hole_diameter = 4.0

# 1. Create the bottom Hexagonal section
# Using polygon(6, d) where d is the circumscribed diameter.
# Matching this to the shaft diameter aligns the hex corners with the cylinder above.
result = cq.Workplane("XY").polygon(6, shaft_diameter).extrude(hex_height)

# 2. Create the middle Cylindrical Shaft
# Select the top face of the hex section and extrude the shaft
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Create the Top Head
# Select the top face of the shaft and extrude the head
result = (
    result.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 4. Create the Through Hole
# Calculate the Z-position for the center of the hole (roughly middle of the shaft)
hole_z_center = hex_height + (shaft_length / 2.0)

# Select the XZ plane (which has a normal along Y) and offset the origin to the hole height
# Then drill a hole through the entire part
result = (
    cq.Workplane("XZ", origin=(0, 0, hole_z_center))
    .circle(hole_diameter / 2.0)
    .extrude(head_diameter + 5, both=True)
    .rotate((0, 0, 0), (0, 0, 1), 90)
)

result = cq.Workplane("XY").polygon(6, shaft_diameter).extrude(hex_height).faces(">Z").workplane().circle(shaft_diameter / 2.0).extrude(shaft_length).faces(">Z").workplane().circle(head_diameter / 2.0).extrude(head_height)

result = result.faces(">X").workplane(centerOption="CenterOfMass", offset=-hole_z_center).circle(hole_diameter / 2.0).cutThruAll()