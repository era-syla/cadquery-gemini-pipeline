import cadquery as cq

# Dimensions estimation based on visual proportions
length = 60.0       # Total length (X-axis)
width = 40.0        # Total width (Y-axis)
height = 15.0       # Total height (Z-axis)
wall_thickness = 2.0
post_diameter = 6.0
post_radius = post_diameter / 2.0

# Feature dimensions
# Front/Back walls have a central tab extending down (sides are shorter)
tab_width = 20.0    
side_wall_base_height = 5.0 # The height of the 'short' sections on front/back

# Side walls have a central notch cut out from the bottom
notch_width = 15.0
notch_height = 5.0

# Half dimensions for calculations
dx = length / 2.0
dy = width / 2.0

# 1. Create Corner Posts
# Four cylinders located at the corners of the bounding rectangle
posts = (
    cq.Workplane("XY")
    .rect(length, width, forConstruction=True)
    .vertices()
    .circle(post_radius)
    .extrude(height)
)

# 2. Define Front/Back Wall Profile (XZ Plane)
# These walls have a "tab" shape: full height in the middle, cut away at bottom corners.
# We draw the profile clockwise starting from top-left.
x_tab_half = tab_width / 2.0
# Points: (x, z)
front_profile_pts = [
    (-dx, height),                # Top-Left corner
    (dx, height),                 # Top-Right corner
    (dx, side_wall_base_height),  # Right side bottom (short wall)
    (x_tab_half, side_wall_base_height), # Step in for tab
    (x_tab_half, 0),              # Tab bottom right
    (-x_tab_half, 0),             # Tab bottom left
    (-x_tab_half, side_wall_base_height),# Step out from tab
    (-dx, side_wall_base_height), # Left side bottom (short wall)
]

# Create Front Wall
front_wall = (
    cq.Workplane("XZ")
    .polyline(front_profile_pts)
    .close()
    .extrude(wall_thickness, both=True)
    .translate((0, -dy, 0)) # Move to front position
)

# Create Back Wall (Same profile)
back_wall = (
    cq.Workplane("XZ")
    .polyline(front_profile_pts)
    .close()
    .extrude(wall_thickness, both=True)
    .translate((0, dy, 0)) # Move to back position
)

# 3. Define Left/Right Wall Profile (YZ Plane)
# These walls have a "notch" shape: full height at sides, cut away at bottom center.
# We draw the profile on YZ plane where local X is Global Y, local Y is Global Z.
y_notch_half = notch_width / 2.0
# Points: (y, z) -> (Global Y, Global Z)
side_profile_pts = [
    (-dy, height),                # Top-Left (Back)
    (dy, height),                 # Top-Right (Front)
    (dy, 0),                      # Bottom-Right
    (y_notch_half, 0),            # Notch start right
    (y_notch_half, notch_height), # Notch top right
    (-y_notch_half, notch_height),# Notch top left
    (-y_notch_half, 0),           # Notch start left
    (-dy, 0),                     # Bottom-Left
]

# Create Right Wall
right_wall = (
    cq.Workplane("YZ")
    .polyline(side_profile_pts)
    .close()
    .extrude(wall_thickness, both=True)
    .translate((dx, 0, 0)) # Move to right position
)

# Create Left Wall
left_wall = (
    cq.Workplane("YZ")
    .polyline(side_profile_pts)
    .close()
    .extrude(wall_thickness, both=True)
    .translate((-dx, 0, 0)) # Move to left position
)

# 4. Combine all parts into the final result
result = posts.union(front_wall).union(back_wall).union(right_wall).union(left_wall)