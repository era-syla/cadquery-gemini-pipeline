import cadquery as cq

# --- Parameters ---
# Main Chassis Dimensions
chassis_length = 80.0
chassis_width = 40.0
chassis_height = 20.0
chassis_corner_fillet = 2.0
chassis_top_fillet = 1.5

# Cabin (Roof) Dimensions
cabin_length = 45.0
cabin_width = 30.0
cabin_height = 15.0
cabin_curve_radius = 12.0  # Controls the slope of the roof

# Wheel Dimensions
wheel_radius = 11.0
wheel_width = 10.0
wheel_chamfer = 2.0
axle_radius = 4.0
axle_length = 4.0  # Exposed length between chassis and wheel
wheel_x_pos = 28.0 # Distance from center to wheel axles
wheel_z_pos = -4.0 # Vertical offset from center

# --- Construction ---

# 1. Main Chassis Body
# Create a rectangular box centered at the origin
result = cq.Workplane("XY").box(chassis_length, chassis_width, chassis_height)

# Fillet the vertical edges to round the corners of the car body
result = result.edges("|Z").fillet(chassis_corner_fillet)

# Fillet the top perimeter loop for a smoother look
result = result.faces(">Z").edges().fillet(chassis_top_fillet)

# 2. Cabin / Roof
# Create the cabin box on top of the chassis
# Calculated Z offset to place it exactly on the top face
cabin_z_offset = chassis_height / 2.0

cabin = (
    cq.Workplane("XY")
    .workplane(offset=cabin_z_offset)
    .box(cabin_length, cabin_width, cabin_height)
)

# Apply a large fillet to the front and back top edges to create the curved aerodynamic profile
# Select edges that are on top (>Z) and parallel to the Y-axis (|Y)
cabin = cabin.edges(">Z and |Y").fillet(cabin_curve_radius)

# Union the cabin to the main chassis
result = result.union(cabin)

# 3. Wheels and Axles
def create_wheel_assembly(is_right_side):
    """
    Creates a wheel and axle assembly.
    is_right_side: True for +Y side, False for -Y side
    """
    direction = 1.0 if is_right_side else -1.0
    overlap = 2.0 # Amount axle goes inside the chassis to ensure solid union
    
    # Create Axle
    # Starts inside the chassis and extends outwards
    axle_total_len = overlap + axle_length + wheel_width/2.0
    axle_start = -direction * overlap
    
    axle = (
        cq.Workplane("XZ")
        .workplane(offset=axle_start)
        .circle(axle_radius)
        .extrude(direction * axle_total_len)
    )
    
    # Create Wheel
    # Positioned at the end of the axle_length
    wheel_start = direction * axle_length
    
    wheel = (
        cq.Workplane("XZ")
        .workplane(offset=wheel_start)
        .circle(wheel_radius)
        .extrude(direction * wheel_width)
    )
    
    # Round the edges of the tires
    # Select the circular faces perpendicular to Y to fillet their edges
    wheel = wheel.faces(">Y" if is_right_side else "<Y").edges().fillet(wheel_chamfer)
    
    return axle.union(wheel)

# Instantiate and position wheels
# Chassis side surface is at +/- chassis_width/2
y_offset = chassis_width / 2.0

# Right Side Wheels (+Y)
wheel_right = create_wheel_assembly(is_right_side=True)

# Front Right
wh_fr = wheel_right.translate((wheel_x_pos, y_offset, wheel_z_pos))
result = result.union(wh_fr)

# Back Right
wh_br = wheel_right.translate((-wheel_x_pos, y_offset, wheel_z_pos))
result = result.union(wh_br)

# Left Side Wheels (-Y)
wheel_left = create_wheel_assembly(is_right_side=False)

# Front Left
wh_fl = wheel_left.translate((wheel_x_pos, -y_offset, wheel_z_pos))
result = result.union(wh_fl)

# Back Left
wh_bl = wheel_left.translate((-wheel_x_pos, -y_offset, wheel_z_pos))
result = result.union(wh_bl)