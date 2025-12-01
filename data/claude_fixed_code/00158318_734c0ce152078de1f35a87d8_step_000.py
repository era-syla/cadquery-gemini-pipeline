import cadquery as cq

# Parametric dimensions for the model
head_diameter = 10.0
head_height = 3.5
body_diameter = 7.0
body_height = 6.0
leg_length = 5.0
leg_width = 2.5      # Dimension of the leg parallel to the flat face
leg_thickness = 1.4  # Dimension of the leg perpendicular to the gap
leg_gap = 2.0        # Space between the legs

# 1. Create the top head (a cylinder)
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# 2. Create the main body (a smaller cylinder extruded from the bottom of the head)
result = result.faces("<Z").workplane().circle(body_diameter / 2.0).extrude(body_height)

# 3. Create the two legs (prongs)
# Calculate the offset from center for the legs
offset_x = (leg_gap + leg_thickness) / 2.0

result = (
    result.faces("<Z")
    .workplane()
    .pushPoints([(offset_x, 0), (-offset_x, 0)])
    .rect(leg_thickness, leg_width)
    .extrude(leg_length)
)

# 4. Refine the geometry
# Apply fillets to the bottom edges of the legs to create the rounded tips shown in the image
# We use a radius slightly less than half the thickness to create a fully rounded tip effect
result = result.edges("|Z").fillet(leg_thickness * 0.48)