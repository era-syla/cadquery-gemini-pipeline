import cadquery as cq

# Dimensions based on visual analysis of the image
# The object is a hexagonal prism with a central cylindrical hole.
# There are no visible chamfers or fillets on the edges in this simplified model.
hex_circum_diameter = 20.0  # Diameter of the circumscribed circle (distance across corners)
height = 12.0               # Height/thickness of the nut
hole_diameter = 10.0        # Diameter of the central through-hole

# Generate the CadQuery model
# 1. Start on the XY plane.
# 2. Draw the hexagonal outer profile using 'polygon'.
# 3. Draw the circular inner profile using 'circle' to define the void.
# 4. Extrude the resulting 2D profile to create the 3D solid.
result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_circum_diameter)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)