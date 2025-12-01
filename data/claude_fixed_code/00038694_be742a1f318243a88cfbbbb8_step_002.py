import cadquery as cq

# Parameters derived from visual estimation of the 3D model
# The object is an L-shaped corner connector with U-channels and a central pin.
profile_width = 20.0       # Outer width of the arm profile
profile_height = 20.0      # Outer height of the arm profile
arm_length = 50.0          # Length of each arm from the outer corner
wall_thickness = 4.0       # Thickness of the side walls
floor_thickness = 5.0      # Thickness of the bottom floor
pin_size = 3.0             # Width/Depth of the square pin at the corner
pin_offset_gap = 1.5       # Gap between the pin and the inner corner walls

# Derived dimensions
channel_width = profile_width - 2 * wall_thickness
channel_depth = profile_height - floor_thickness

# 1. Create the base L-shape geometry
# We position the outer corner at (0,0,0) for simpler coordinate calculation.
# Create Arm along X axis
arm_x = cq.Workplane("XY").rect(arm_length, profile_width).extrude(profile_height).translate((arm_length/2, profile_width/2, 0))
# Create Arm along Y axis
arm_y = cq.Workplane("XY").rect(profile_width, arm_length).extrude(profile_height).translate((profile_width/2, arm_length/2, 0))

# Union the two arms to create a solid L-block
base_l = arm_x.union(arm_y)

# 2. Create the Channel Cuts
# Cut slot along the X arm (Top face)
cut_x = (
    cq.Workplane("XY")
    .workplane(offset=profile_height)
    .rect(arm_length, channel_width)
    .extrude(-channel_depth)
    .translate((arm_length / 2, profile_width / 2, 0))
)

# Cut slot along the Y arm (Top face)
cut_y = (
    cq.Workplane("XY")
    .workplane(offset=profile_height)
    .rect(channel_width, arm_length)
    .extrude(-channel_depth)
    .translate((profile_width / 2, arm_length / 2, 0))
)

# Apply cuts to the base
hollowed_l = base_l.cut(cut_x).cut(cut_y)

# 3. Create the Vertical Pin at the Corner intersection
# The pin is located at the intersection of the channels.
# Visually, it is offset towards the inner corner (which is at x=profile_width, y=profile_width).
# Inner wall location: profile_width - wall_thickness
# Pin Center Calculation: (Inner Wall Pos) - (Gap) - (Pin Radius)
pin_center_pos = (profile_width - wall_thickness) - pin_offset_gap - (pin_size / 2)

pin = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .rect(pin_size, pin_size)
    .extrude(channel_depth)
    .translate((pin_center_pos, pin_center_pos, 0))
)

# 4. Final Union
result = hollowed_l.union(pin)