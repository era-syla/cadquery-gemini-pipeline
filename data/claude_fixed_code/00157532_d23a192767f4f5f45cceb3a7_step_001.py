import cadquery as cq

# Object Dimensions
height = 40.0
plate_width = 32.0    # Distance from hinge center to far edge
plate_thickness = 4.0
barrel_outer_dia = 12.0
pin_dia = 6.0
chamfer_size = 12.0   # Size of the corner cuts on the plate
num_knuckles = 3

# Derived Parameters
barrel_radius = barrel_outer_dia / 2.0
pin_radius = pin_dia / 2.0
segment_height = height / 5.0  # 5 segments: 3 knuckles, 2 gaps

# 1. Create Base Profile (Keyhole shape: Barrel + Plate)
# Sketch on XY plane, which will be the cross-section
base_sketch = (
    cq.Workplane("XY")
    .circle(barrel_radius)
    .moveTo(0, -plate_thickness / 2.0)
    .lineTo(plate_width, -plate_thickness / 2.0)
    .lineTo(plate_width, plate_thickness / 2.0)
    .lineTo(0, plate_thickness / 2.0)
    .close()
)

# 2. Extrude to create the main solid block
# This creates the full plate with a solid cylindrical hinge area
result = base_sketch.extrude(height)

# 3. Shape the Plate
# Apply chamfers to the far corners of the plate to create the shield-like shape.
# We select the edges at the far end (X max) that run parallel to the thickness (Y axis).
result = result.edges("|Y and >>X").chamfer(chamfer_size)

# 4. Create Hinge Gaps
# We need to cut away the barrel material in the gaps, but leave the central pin intact.
# We define a "cutting tool" profile that is a large rectangle (to clear material)
# with a circular hole in the center (to preserve the pin).

cut_profile = (
    cq.Workplane("XY")
    .rect(barrel_outer_dia * 2.5, barrel_outer_dia * 2.5)
    .circle(pin_radius)
)

# Create solid tools for the two gaps
# Gaps are located at segment indices 1 and 3 (0-indexed)
gap1 = cut_profile.extrude(segment_height).translate((0, 0, segment_height))
gap2 = cut_profile.extrude(segment_height).translate((0, 0, segment_height * 3))

# Subtract the tools from the main body
result = result.cut(gap1).cut(gap2)

# 5. Apply Fillets
# Add a fillet to the junction where the flat plate meets the cylindrical knuckles
# We select vertical edges (parallel to Z) located near the intersection area.
intersection_x = (barrel_radius**2 - (plate_thickness/2.0)**2)**0.5
result = result.edges("|Z").fillet(1.0)

# Return the result
# show_object(result) # Uncomment for use in CQ-editor