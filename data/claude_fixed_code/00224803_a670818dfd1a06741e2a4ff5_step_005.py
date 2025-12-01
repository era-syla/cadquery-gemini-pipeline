import cadquery as cq

# Dimensions
base_length = 45.0
base_width = 30.0
base_height = 5.0
base_fillet = 2.0

cyl_radius = 9.0
cyl_height = 15.0
cyl_x_offset = 14.0

# The main body (left side hump)
body_width = 22.0
body_height_rel = 8.0  # Height above base
body_end_x = 2.0       # X-coordinate where the wide body transitions to the arm

# The connecting arm (bridge to cylinder)
arm_width = 14.0
arm_height_rel = 8.0   # Same height as body

# 1. Base Plate
# Centered at origin for symmetry in Y
result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .edges("|Z")
    .fillet(base_fillet)
)

# 2. Vertical Cylinder
# Positioned to the right side
cylinder = (
    cq.Workplane("XY")
    .center(cyl_x_offset, 0)
    .circle(cyl_radius)
    .extrude(cyl_height)
)

# 3. Rear Body (The "Hump")
# Starts from left edge of base, goes to body_end_x
# We define coordinates to place the box correctly
x_start = -base_length / 2.0
body_len = body_end_x - x_start
body_center_x = x_start + body_len / 2.0

body = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(body_center_x, 0)
    .box(body_len, body_width, body_height_rel, centered=(True, True, False))
)

# Round the top of the body. Max fillet radius is limited by height (8).
# This creates a "flattened arch" profile.
body = body.edges(">Z").edges("|X").fillet(body_height_rel - 0.01)

# 4. Connection Arm
# Connects the Body to the Cylinder.
# It starts inside the body (to overlap) and goes to the cylinder center.
arm_start_x = body_end_x - 2.0 
arm_len_to_cyl = cyl_x_offset - arm_start_x
arm_center_x = arm_start_x + arm_len_to_cyl / 2.0

arm = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(arm_center_x, 0)
    .box(arm_len_to_cyl, arm_width, arm_height_rel, centered=(True, True, False))
)

# Round the top of the arm. Max fillet is limited by half-width (7).
arm = arm.edges(">Z").edges("|X").fillet(arm_width / 2.0 - 0.01)

# 5. Union all parts
# We unite the base with the cylinder, body, and arm.
result = result.union(cylinder).union(body).union(arm)

# 6. Refinement: Fillets at junctions
# Fillet the vertical step where the wide body meets the narrow arm
result = result.edges("|Z").fillet(2.0)