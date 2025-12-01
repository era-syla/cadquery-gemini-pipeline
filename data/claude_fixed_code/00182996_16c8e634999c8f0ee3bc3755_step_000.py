import cadquery as cq

# Create the 3D object
# 1. Start with the rectangular base
# 2. Extrude the central stem
# 3. Extrude the top head/cup
# 4. Cut the blind hole in the cup

result = (
    cq.Workplane("XY")
    .box(60, 40, 5)          # Base: 60mm length, 40mm width, 5mm thickness
    .faces(">Z").workplane() # Workplane on top of the base
    .circle(5)               # Draw stem profile (Radius 5mm / Dia 10mm)
    .extrude(30)             # Extrude stem height (30mm)
    .faces(">Z").workplane() # Workplane on top of the stem
    .circle(10)              # Draw head profile (Radius 10mm / Dia 20mm)
    .extrude(10)             # Extrude head height (10mm)
    .faces(">Z").workplane() # Workplane on top of the head
    .circle(8)               # Draw hole profile (Radius 8mm / Dia 16mm)
    .cutBlind(-8)            # Cut blind hole downwards (Depth 8mm, leaving 2mm bottom)
)