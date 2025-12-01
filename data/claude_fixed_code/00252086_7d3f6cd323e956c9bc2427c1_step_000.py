import cadquery as cq

# Parametric dimensions
length = 60.0        # Total length along X
height = 40.0        # Total height along Z
width = 30.0         # Thickness/Depth along Y
step_width = 25.0    # Width of the lower left section
step_height = 20.0   # Height of the lower left section

# Create the 3D model
# Drawing the profile on the XZ plane (Front) so that Z acts as vertical height
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),                  # Bottom-left corner
        (length, 0),             # Bottom edge to bottom-right
        (length, height),        # Right edge to top-right
        (step_width, height),    # Top edge of the higher section
        (step_width, step_height), # Vertical drop of the step
        (0, step_height)         # Top edge of the lower section
    ])
    .close()
    .extrude(width, both=True)
)