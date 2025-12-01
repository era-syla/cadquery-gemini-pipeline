import cadquery as cq

# Parametric dimensions to match the aspect ratio of the belt model
length = 300.0       # Center-to-center distance between the loop ends
width = 50.0         # Outer width of the belt (diameter of the curved ends)
thickness = 3.0      # Wall thickness of the belt material
height = 15.0        # Height of the extrusion (width of the belt face)

# Create the belt geometry
# We define the shape on the XY plane using slot2D (stadium shape).
# By drawing the outer slot and then the inner slot before extruding,
# CadQuery creates a hollow shape with the defined wall thickness.
result = (
    cq.Workplane("XY")
    .slot2D(length, width)                          # Outer boundary wire
    .extrude(height)                                # Extrude the outer shape
    .faces(">Z")                                    # Select top face
    .workplane()                                    # Create workplane on top face
    .slot2D(length, width - 2 * thickness)          # Inner boundary wire
    .cutThruAll()                                   # Cut through to create hollow belt
)