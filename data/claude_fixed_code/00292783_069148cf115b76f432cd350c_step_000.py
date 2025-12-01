import cadquery as cq

# Parameters
length = 60.0        # Total length of the side plate (Y direction)
width = 50.0         # Total width of the assembly (X direction)
height_back = 60.0   # Height of the rear section (Z direction)
height_front = 25.0  # Height of the front section
thickness = 4.0      # Thickness of the side plates
top_land = 28.0      # Length of the top horizontal edge of the back section
fillet_main = 15.0   # Radius of the large transition curve
fillet_corner = 3.0  # Radius of the small external corners
cyl_radius = 12.0    # Radius of the connecting cylinder

# Derived parameters for cylinder position
# Center the cylinder in the "back" vertical section
cyl_y = length - (top_land / 2.0)
cyl_z = height_front + (height_back - height_front) / 2.0

# Define the profile of a single side plate
# Drawing on YZ plane, extruding along X
# Coordinates are (y, z)
pts = [
    (0, 0),
    (length, 0),
    (length, height_back),
    (length - top_land, height_back),
    (length - top_land, height_front), # This creates the internal corner for the step
    (0, height_front)
]

# Create the basic extruded shape for one plate
plate_shape = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Apply the large fillet to the internal step corner
plate_shape = plate_shape.edges("|X").filter(lambda e: 
    abs(e.Center().y - (length - top_land)) < 1 and 
    abs(e.Center().z - height_front) < 1
).fillet(fillet_main)

# Apply small rounding fillets to the external corners (Top-Back and Front-Top)
plate_shape = plate_shape.edges("|X").filter(lambda e: 
    abs(e.Center().y - length) < 1 and 
    abs(e.Center().z - height_back) < 1
).fillet(fillet_corner)

plate_shape = plate_shape.edges("|X").filter(lambda e: 
    abs(e.Center().y) < 1 and 
    abs(e.Center().z - height_front) < 1
).fillet(fillet_corner)

# Instantiate and position the left and right plates
# Left plate starts at -width/2
plate_left = plate_shape.translate((-width/2, 0, 0))
# Right plate starts at width/2 - thickness
plate_right = plate_shape.translate((width/2 - thickness, 0, 0))

# Create the connecting cylinder
# Extrude along X from -width/2 to width/2
cylinder = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2)
    .center(cyl_y, cyl_z)
    .circle(cyl_radius)
    .extrude(width)
)

# Combine all parts into the final solid
result = plate_left.union(plate_right).union(cylinder)