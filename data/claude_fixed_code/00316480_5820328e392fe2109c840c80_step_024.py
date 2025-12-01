import cadquery as cq

# Parametric dimensions
base_width = 60.0
base_depth = 20.0
base_height = 40.0

top_feature_width = 30.0
top_feature_depth = 15.0
wall_thickness = 3.0
wall_height = 10.0
arch_height = 4.0

# 1. Create the base block
# Centered at (0,0,0)
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# 2. Add the side walls (Left and Right)
# Calculate positions
# The walls sit on top of the base (Z = base_height/2)
# They are flush with the back face (Y = base_depth/2)
# Center Y for the walls:
wall_y_center = (base_depth / 2) - (top_feature_depth / 2)
# Center X for the walls (offset from center by half width minus half thickness):
wall_x_offset = (top_feature_width - wall_thickness) / 2

# Define centers for the two walls
wall_centers = [
    (-wall_x_offset, wall_y_center),
    (wall_x_offset, wall_y_center)
]

# Draw and extrude the side walls
result = (
    base.faces(">Z").workplane()
    .pushPoints(wall_centers)
    .rect(wall_thickness, top_feature_depth)
    .extrude(wall_height)
)

# 3. Add the arched back wall
# We draw this profile on the XZ plane located at the back face of the object
# The "XZ" workplane has a normal of (0, -1, 0), pointing towards the front.
# We set the origin to the back face. Positive extrusion will go "forward" (into the model).

z_start = base_height / 2

result = (
    result.faces(">Z").workplane(centerOption="CenterOfMass")
    .center(0, wall_y_center)
    .moveTo(-top_feature_width/2, 0)
    .lineTo(-top_feature_width/2, wall_height)
    # Create the arch
    .threePointArc(
        (0, wall_height + arch_height), 
        (top_feature_width/2, wall_height)
    )
    .lineTo(top_feature_width/2, 0)
    .close()
    # Extrude upward by wall thickness to create the back wall
    .extrude(wall_thickness)
)