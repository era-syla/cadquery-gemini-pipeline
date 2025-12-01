import cadquery as cq

# Create the left object: A square tube (hollow box profile)
# Estimated dimensions: 20x20mm base, 20mm height, 1mm wall thickness
square_tube = (
    cq.Workplane("XY")
    .rect(20, 20)           # Outer square profile
    .extrude(20)            # Extrude to create the tube
    .faces(">Z")
    .workplane()
    .rect(18, 18)           # Inner square profile (defines the hole)
    .cutThruAll()           # Cut through to create hollow
    .translate((-15, 0, 0)) # Position to the left
)

# Create the right object: A cylindrical tube
# Estimated dimensions: 20mm outer diameter, 12mm inner diameter (thick walls), 20mm height
cylindrical_tube = (
    cq.Workplane("XY")
    .circle(10)             # Outer circle (radius 10)
    .extrude(20)            # Extrude to create the tube
    .faces(">Z")
    .workplane()
    .circle(6)              # Inner circle (radius 6)
    .cutThruAll()           # Cut through to create hollow
    .translate((15, 0, 0))  # Position to the right
)

# Combine both objects into the final result
result = square_tube.union(cylindrical_tube)