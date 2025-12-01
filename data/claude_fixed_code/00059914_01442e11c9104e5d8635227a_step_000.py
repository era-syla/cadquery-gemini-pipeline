import cadquery as cq

# Define dimensions based on visual analysis of the hexagonal nut shape
# The object consists of a hexagonal prism with a cylindrical through-hole.
thickness = 6.0          # Height of the extrusion
outer_diameter = 20.0    # Diameter of the circumscribed circle (across corners)
hole_diameter = 10.0     # Diameter of the central hole

# Create the object
result = (
    cq.Workplane("XY")
    .polygon(6, outer_diameter)                  # Draw the outer hexagon
    .extrude(thickness)                          # Extrude the sketch to create the solid
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)                         # Create the central hole
)