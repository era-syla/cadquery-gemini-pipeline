import cadquery as cq

# Define dimensions for the object
height = 20.0
width = 8.0
thickness = 1.0

# Create the object
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)                  # Start at the bottom-left tip
    .lineTo(0, height)             # Draw the vertical back edge up to top-left
    .lineTo(width, height * 0.75)  # Draw to the bulge point
    .splineTo((0, 0))              # Draw the curved front edge back to start
    .close()
    .extrude(thickness)            # Extrude to create the solid volume
)