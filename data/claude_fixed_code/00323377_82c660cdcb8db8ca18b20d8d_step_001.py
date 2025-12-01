import cadquery as cq

# Dimensions
length = 50.0
width = 60.0
height = 40.0
wall_thickness = 15.0
floor_thickness = 15.0
wedge_width = 15.0  # How far the ramp extends into the channel at the back

# 1. Create the base U-shaped block
# Create a solid block centered in X and Y, sitting on Z=0
# This creates a box spanning x=[-30, 30], y=[-25, 25], z=[0, 40]
base = cq.Workplane("XY").box(width, length, height, centered=(True, True, False))

# Cut the central channel
channel_width = width - 2 * wall_thickness
channel_cut_depth = height - floor_thickness

# Cut from the top face downwards
u_block = (
    base.faces(">Z")
    .workplane()
    .rect(channel_width, length)
    .cutBlind(-channel_cut_depth)
)

# 2. Create the triangular wedge (ramp) feature inside the left channel wall
# X-coordinates (Global)
x_inner_left = -width/2 + wall_thickness
x_wedge_extent = x_inner_left + wedge_width

# Y-coordinates (Global)
y_back = length / 2
y_front = -length / 2

# Z-coordinates (Global)
z_floor = floor_thickness
z_top = height

# Setup Planes
offset_to_back = -y_back

# Points for the triangle on the back face (local coords X, Z)
p1 = (x_inner_left, z_floor)           # Bottom-inner corner
p2 = (x_inner_left, z_top)             # Top-inner corner
p3 = (x_wedge_extent, z_floor)         # Point sticking into channel on the floor

# Distance to loft to the front
distance_to_front = length

wedge = (
    cq.Workplane("XZ")
    .workplane(offset=offset_to_back)  # Move to Back Face (Y=+25)
    .moveTo(p1[0], p1[1])
    .lineTo(p2[0], p2[1])
    .lineTo(p3[0], p3[1])
    .close()
    .workplane(offset=distance_to_front) # Move to Front Face (Y=-25)
    .moveTo(p1[0], p1[1])
    .lineTo(p1[0] + 0.001, p1[1])
    .lineTo(p1[0], p1[1] + 0.001)
    .close()
    .loft()
)

# 3. Combine the U-block and the wedge
result = u_block.union(wedge)