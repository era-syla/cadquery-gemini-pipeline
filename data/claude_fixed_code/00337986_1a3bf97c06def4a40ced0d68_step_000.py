import cadquery as cq

# Parametric dimensions
diameter = 25.0  # Diameter of the circumscribed circle for the pentagon
thickness = 2.0  # Thickness of the plate

# Create a regular pentagon extruded to a thickness
# We rotate the workplane by -90 degrees around Z to orient the pentagon 
# with a flat edge at the top and a vertex pointing down.
result = (
    cq.Workplane("XY")
    .polygon(5, diameter)
    .extrude(thickness)
    .rotate((0, 0, 0), (0, 0, 1), -90)
)