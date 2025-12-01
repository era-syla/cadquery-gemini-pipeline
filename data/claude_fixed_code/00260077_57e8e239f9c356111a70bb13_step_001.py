import cadquery as cq

# --- Parameters ---
length = 150.0          # Total length of the part
width = 50.0            # Width of the part (diameter of the curved section)
plate_thickness = 2.0   # Thickness of the top plate
wall_height = 12.0      # Height of the rim/wall
wall_thickness = 2.0    # Thickness of the rim/wall
flange_width = 2.0      # Width of the lip (offset from plate edge to wall)

# Snap tab parameters
tab_length = 6.0        # Width of the tab along the wall
tab_depth = 1.5         # How far the tab protrudes inwards
tab_height = 3.0        # Vertical height of the tab
tab_z_offset = 3.0      # Distance from the open edge of the wall to the tab

# --- Derived Geometry ---
radius = width / 2.0
straight_len = length - radius

# Calculate dimensions for the inner wall surface (where tabs attach)
total_wall_offset = flange_width + wall_thickness
inner_radius = radius - total_wall_offset
inner_straight_len = straight_len - total_wall_offset

# --- Helper Function ---
def stadium_profile(workplane, l_straight, r):
    """
    Draws a stadium (oblong) profile.
    Origin is at the center of the semi-circle.
    The shape extends along the +X axis.
    """
    return (workplane
        .moveTo(0, -r)
        .lineTo(l_straight, -r)
        .lineTo(l_straight, r)
        .lineTo(0, r)
        .threePointArc((-r, 0), (0, -r))
        .close()
    )

# --- Modeling ---

# 1. Create the Main Plate
# Origin (0,0,0) is at the center of the curved end on the bottom face of the plate
result = cq.Workplane("XY")
result = stadium_profile(result, straight_len, radius).extrude(plate_thickness)

# 2. Create the Perimeter Wall
# Extrude downwards from the bottom face (Z=0)
# We define the wall by an outer loop and an inner loop
outer_wall_r = radius - flange_width
outer_wall_l = straight_len - flange_width

inner_wall_r = inner_radius
inner_wall_l = inner_straight_len

wall = (
    result.faces("<Z").workplane()
    .transformed(offset=(0, 0, 0))
)
wall = stadium_profile(wall, outer_wall_l, outer_wall_r)
wall = stadium_profile(wall, inner_wall_l, inner_wall_r)
wall = wall.extrude(-wall_height)
result = result.union(wall)

# 3. Create Snap Tabs
# Create a generic tab object centered at origin
# Dimensions: X=depth, Y=length, Z=height
base_tab = cq.Workplane("XY").box(tab_depth, tab_length, tab_height)

# Add a chamfer to the bottom-front edge for snapping action
# >X is the protruding face, <Z is the bottom face
base_tab = base_tab.edges(">X and <Z").chamfer(tab_depth * 0.6)

# Calculate global Z position for the tabs
# The wall extends from Z=0 to Z=-wall_height. 
# Tabs are positioned near the bottom edge.
global_z = -(wall_height - tab_z_offset - tab_height/2.0)

tabs = []

# A. Tabs along the straight sides
num_side_tabs = 5
x_step = inner_straight_len / (num_side_tabs + 1)

for i in range(num_side_tabs):
    x_pos = (i + 1) * x_step
    
    # Top wall (Y positive), facing -Y
    # Rotate -90 Z so +X (depth) points -Y
    t_top = (base_tab
             .rotate((0,0,0), (0,0,1), -90)
             .translate((x_pos, inner_radius - tab_depth/2, global_z)))
    tabs.append(t_top)
    
    # Bottom wall (Y negative), facing +Y
    # Rotate 90 Z so +X (depth) points +Y
    t_bot = (base_tab
             .rotate((0,0,0), (0,0,1), 90)
             .translate((x_pos, -inner_radius + tab_depth/2, global_z)))
    tabs.append(t_bot)

# B. Tabs on the flat end (Right side)
# Wall at X = inner_straight_len, facing -X
# Rotate 180 Z so +X points -X
y_spacing = inner_radius * 0.8
for y in [-y_spacing/2, y_spacing/2]:
    t_end = (base_tab
             .rotate((0,0,0), (0,0,1), 180)
             .translate((inner_straight_len - tab_depth/2, y, global_z)))
    tabs.append(t_end)

# C. Tab on the curved end (Left side)
# Wall at X = -inner_radius, facing +X
# No rotation needed (+X points +X)
t_curve = (base_tab
           .translate((-inner_radius + tab_depth/2, 0, global_z)))
tabs.append(t_curve)

# Combine all tabs into the main model
for t in tabs:
    result = result.union(t)