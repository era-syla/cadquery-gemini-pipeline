import cadquery as cq

# Define parametric dimensions
height = 40.0
outer_diameter = 50.0
wall_thickness = 2.0

# Calculate derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder geometry
result = (
    cq.Workplane("XY")
    .circle(outer_radius)    # Create outer profile
    .extrude(height)         # Extrude the outer cylinder
    .faces(">Z")             # Select the top face
    .circle(inner_radius)    # Create inner profile
    .cutThruAll()            # Cut through to create hollow cylinder
)