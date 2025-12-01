import cadquery as cq

# Parametric dimensions
length = 90.0       # Total length of the part
width = 40.0        # Total width of the part
thickness = 5.0     # Total thickness of the main body
tab_length = 12.0   # Length of the thinner tab section
tab_thickness = 2.5 # Thickness of the tab section
fillet_radius = 6.0 # Radius of the rounded corners

# 1. Create the base block centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Fillet the vertical edges to create rounded corners
# Applying this before the cut ensures the tab also has rounded corners
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create the stepped tab feature
# Remove material from the top face at one end to create the tab
cut_depth = thickness - tab_thickness

# Select the top face and create a cut
# We center the cut rectangle at the edge of the part (+X end)
# The rectangle width is 2*tab_length to span from (L/2 - tab_length) to (L/2 + tab_length)
# The rectangle height is oversized relative to width to ensure clean sides
result = (
    result
    .faces(">Z")
    .workplane()
    .center((length / 2) - tab_length, 0)
    .rect(tab_length, width * 1.2)
    .cutBlind(-cut_depth)
)