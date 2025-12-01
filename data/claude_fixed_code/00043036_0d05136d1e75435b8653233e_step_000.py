import cadquery as cq

# Geometric parameters estimated from the image
height = 100.0       # Total height of the frame
width = 40.0         # Total width of the frame
border_width = 4.0   # Width of the frame material (the profile width)
depth = 4.0          # Thickness of the frame (extrusion depth)

# Create the 3D object
# We sketch on the XZ plane to orient the frame vertically, matching the image
result = (
    cq.Workplane("XZ")
    .rect(width, height)  # Create the outer boundary
    .extrude(depth)  # Extrude the profile to create the solid frame
    .faces(">Y")
    .workplane()
    .rect(width - 2 * border_width, height - 2 * border_width)  # Create the inner boundary for the hole
    .cutThruAll()  # Cut through to create the frame
)