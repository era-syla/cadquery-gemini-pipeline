import cadquery as cq

# --- Dimensions ---
# Overall bracket dimensions
width = 65.0              # Total width of the bracket
base_length = 75.0        # Length of the horizontal plate (including wall thickness)
wall_height = 45.0        # Height of the vertical plate
thickness = 5.0           # Material thickness

# Rib/Gusset dimensions
rib_size = 25.0           # Length of the rib sides along the plates
rib_thickness = 5.0       # Thickness of the ribs

# Motor mounting dimensions (Modeled after NEMA 23 standard)
center_hole_dia = 38.2    # Diameter of the large central hole
motor_hole_spacing = 47.1 # Distance between motor mounting holes (square pattern)
motor_hole_dia = 5.2      # Diameter of motor mounting holes

# Wall mounting dimensions
wall_hole_spacing = 45.0  # Horizontal distance between wall holes
wall_hole_height = 28.0   # Height of wall holes from the bottom of the bracket
wall_hole_dia = 6.2       # Diameter of wall mounting holes

# --- 1. Create Main L-Bracket Body ---
# We draw the side profile on the YZ plane and extrude it along X (Width).
# Origin (0,0,0) is at the bottom-rear corner.
# Y-axis is Length, Z-axis is Height.
l_profile_pts = [
    (0, 0),
    (0, wall_height),
    (thickness, wall_height),
    (thickness, thickness),
    (base_length, thickness),
    (base_length, 0),
    (0, 0)
]

main_body = (
    cq.Workplane("YZ")
    .polyline(l_profile_pts)
    .close()
    .extrude(width / 2.0, both=True) # Extrude symmetrically centered on X=0
)

# --- 2. Add Triangular Ribs ---
# The ribs are right-angled triangles connecting the inner faces of the L-shape.
# Inner corner is at (thickness, thickness).
rib_pts = [
    (thickness, thickness),
    (thickness + rib_size, thickness),
    (thickness, thickness + rib_size),
    (thickness, thickness)
]

# Right Rib (Positive X side)
# We position the sketch plane so the extrusion fills the space flush with the edge.
right_rib = (
    cq.Workplane("YZ")
    .workplane(offset=width/2.0 - rib_thickness)
    .polyline(rib_pts)
    .close()
    .extrude(rib_thickness)
)

# Left Rib (Negative X side)
# Positioned at the far left edge.
left_rib = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2.0)
    .polyline(rib_pts)
    .close()
    .extrude(rib_thickness)
)

# Combine body and ribs
result = main_body.union(right_rib).union(left_rib)

# --- 3. Cut Base Plate Holes ---
# Center Y for the hole pattern is in the middle of the available flat area
available_length = base_length - thickness
center_y = thickness + (available_length / 2.0)

# Cut Central Motor Pilot Hole
result = (
    result.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .center(0, center_y)
    .circle(center_hole_dia / 2.0)
    .cutThruAll()
)

# Cut 4 Motor Mounting Holes
result = (
    result.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .center(0, center_y)
    .rect(motor_hole_spacing, motor_hole_spacing, forConstruction=True)
    .vertices()
    .circle(motor_hole_dia / 2.0)
    .cutThruAll()
)

# --- 4. Cut Wall Mounting Holes ---
# Cut 2 Wall Holes
result = (
    result.faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .center(0, wall_hole_height)
    .pushPoints([(-wall_hole_spacing/2.0, 0), (wall_hole_spacing/2.0, 0)])
    .circle(wall_hole_dia / 2.0)
    .cutThruAll()
)