import cadquery as cq

# --- Dimensions & Parameters ---
length = 120.0          # Total length of the arm
width_wide = 45.0       # Width at the forked end (Left)
width_narrow = 18.0     # Width at the mounting end (Right)
height = 12.0           # Overall height of the solid
wall_thickness = 2.0    # Thickness of outer walls
floor_thickness = 3.0   # Thickness of the bottom floor in pocketed areas
boss_height = 1.5       # Height of bosses above the top surface
boss_diam = 7.0         # Diameter of mounting bosses
hole_diam = 3.2         # Diameter of screw holes
cbore_diam = 6.5        # Counterbore diameter
cbore_depth = 2.5       # Counterbore depth
cutout_radius = 12.0    # Radius of the 'Y' fork cutout

# Derived coordinates (Center the part on origin)
x_min = -length / 2.0
x_max = length / 2.0
y_wide = width_wide / 2.0
y_narrow = width_narrow / 2.0

# --- 1. Base Geometry ---
# Create the main tapered trapezoidal solid
base_sketch = (
    cq.Workplane("XY")
    .moveTo(x_min, y_wide)
    .lineTo(x_min, -y_wide)
    .lineTo(x_max, -y_narrow)
    .lineTo(x_max, y_narrow)
    .close()
)
result = base_sketch.extrude(height)

# --- 2. Left End Fork (Y-Shape) ---
# Cut a circular shape from the wider end to create the fork
cutout = (
    cq.Workplane("XY")
    .moveTo(x_min, 0)
    .circle(cutout_radius)
    .extrude(height * 2)
    .translate((0, 0, -height))
)
result = result.cut(cutout)

# --- 3. Internal Pocketing & Ribs ---
# Strategy: Create a solid representing the "air" to be removed (inner pocket),
# then subtract rib shapes from this "air" solid, and finally cut the 
# resulting shape from the main body.

# Define the boundaries of the inner pocket area
pocket_start_x = x_min + 12.0   # Start after the boss area
pocket_end_x = x_max - 12.0     # End before the right solid block

# Calculate Y width at specific X points to follow the taper
# Slope calculation: dy/dx
slope = (y_wide - y_narrow) / length
def get_y(x):
    # Linear interpolation of half-width
    dist_from_left = x - x_min
    return y_wide - (dist_from_left * slope)

# Inner Y values accounting for wall thickness
y_p_start = get_y(pocket_start_x) - wall_thickness
y_p_end = get_y(pocket_end_x) - wall_thickness

# Create the "Air Block" (Volume to remove)
air_block = (
    cq.Workplane("XY")
    .moveTo(pocket_start_x, y_p_start)
    .lineTo(pocket_start_x, -y_p_start)
    .lineTo(pocket_end_x, -y_p_end)
    .lineTo(pocket_end_x, y_p_end)
    .close()
    .extrude(height - floor_thickness)
    .translate((0, 0, floor_thickness))
)

# Create Ribs (Solids to preserve inside the air block)
rib_thickness = 2.0
split_point_x = 0.0 # Point where diagonals meet central rib

# Central Rib (Spine)
central_rib = (
    cq.Workplane("XY")
    .rect(length, rib_thickness)
    .extrude(height)
    .translate((20, 0, 0))
)

# Diagonal Ribs (V-shape)
# Diagonal 1
diag_rib_1 = (
    cq.Workplane("XY")
    .rect(50, rib_thickness)
    .extrude(height)
    .rotate((0,0,0), (0,0,1), 25)
    .translate((-15, 8, 0))
)
# Diagonal 2
diag_rib_2 = (
    cq.Workplane("XY")
    .rect(50, rib_thickness)
    .extrude(height)
    .rotate((0,0,0), (0,0,1), -25)
    .translate((-15, -8, 0))
)

all_ribs = central_rib.union(diag_rib_1).union(diag_rib_2)

# Subtract ribs from the air block to create the final cutting tool
pocket_tool = air_block.cut(all_ribs)

# Cut the pocket from the main body
result = result.cut(pocket_tool)

# --- 4. Mounting Bosses & Holes (Left End) ---
# Four bosses in total, 2 on each arm
# Coordinates relative to the angled arm
boss_locations = [
    (x_min + 6, y_wide - 5),   # Top-Left Near
    (x_min + 16, y_wide - 7),  # Top-Left Far
    (x_min + 6, -y_wide + 5),  # Bottom-Left Near
    (x_min + 16, -y_wide + 7)  # Bottom-Left Far
]

for bx, by in boss_locations:
    # Create Boss (Raised cylinder)
    boss = (
        cq.Workplane("XY")
        .moveTo(bx, by)
        .circle(boss_diam / 2.0)
        .extrude(boss_height)
        .translate((0, 0, height))
    )
    result = result.union(boss)
    
    # Cut Hole
    result = (
        result.faces(">Z")
        .workplane()
        .moveTo(bx, by)
        .circle(hole_diam / 2.0)
        .cutThruAll()
    )

# --- 5. Mounting Holes (Right End) ---
# Two counterbored holes
hole_right_x = x_max - 6.0
hole_right_y_offset = 4.5

for y_off in [hole_right_y_offset, -hole_right_y_offset]:
    result = (
        result.faces(">Z")
        .workplane()
        .moveTo(hole_right_x, y_off)
        .cboreHole(hole_diam, cbore_diam, cbore_depth)
    )

# --- 6. Finishing Touches ---
# Chamfer the bottom of the right tip (angled undercut)
result = result.edges(">X and <Z").chamfer(3.0)

# Chamfer the top edge of the right tip
result = result.edges(">X and >Z").chamfer(1.0)