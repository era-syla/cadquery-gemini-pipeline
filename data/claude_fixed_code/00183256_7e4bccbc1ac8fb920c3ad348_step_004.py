import cadquery as cq
import math

# --- Parameters ---
tube_radius = 2.0
# Center of the spiral part in 3D space
spiral_center_y = 0
spiral_center_z = 40

# --- 1. Path Generation ---
# We will generate a list of 3D points to define the path of the tube
path_points = []

# A. Nozzle Connection (Straight section)
# Starting from the nozzle base (x=15) moving towards the spiral center
path_points.append((15, 0, 40))
path_points.append((10, 0, 40))

# B. Transition to Spiral
# Curve from the straight X-axis segment into the YZ-plane spiral
# Using intermediate points to guide the spline smoothly
path_points.append((4, 0, 41))
path_points.append((1, 0, 44))

# C. Spiral Section
# Parametric spiral generation in the YZ plane (x=0)
# r = a + b * theta
turns = 2.5
r_start = 8.0
r_end = 32.0
n_spiral_points = 60

# Start at top (pi/2) to match the incoming upward curve
start_angle = math.pi / 2
end_angle = start_angle + (turns * 2 * math.pi)

for i in range(n_spiral_points + 1):
    t = i / n_spiral_points
    theta = start_angle + t * (end_angle - start_angle)
    r = r_start + (r_end - r_start) * t
    
    # Calculate coordinates in YZ plane
    # y corresponds to cos, z corresponds to sin
    y = spiral_center_y + r * math.cos(theta)
    z = spiral_center_z + r * math.sin(theta)
    x = 0 # Spiral lies flat on x=0 plane
    
    path_points.append((x, y, z))

# D. Tail Section
# From the bottom/exit of the spiral, snake along the ground to the wedge
last_p = path_points[-1] # This should be at low Z (approx z=8)

# Define waypoints for an S-curve on the floor
tail_pts = [
    (-10, last_p[1] - 15, 10),      # Curve out and down
    (-30, last_p[1] - 25, 6),       # Low point on 'floor'
    (-50, last_p[1] - 10, 6),       # S-bend
    (-75, last_p[1] + 5, 6)         # End point for wedge connection
]
path_points.extend(tail_pts)

# --- 2. Create Tube ---
# Create the spline wire from the points
path = cq.Workplane("XY").spline(path_points)

# Sweep a circle along the path
# The path starts at x=15 going -x, so the profile plane is YZ
tube = (
    cq.Workplane("YZ")
    .center(15, 0)
    .circle(tube_radius)
    .sweep(path)
)

# --- 3. Create Nozzle (Start Component) ---
# A lofted shape from the tube circle to a flattened rectangle
nozzle = (
    cq.Workplane("YZ", origin=(15, 0, 40))
    .circle(tube_radius)
    .workplane(offset=12)
    .rect(2, 8)
    .loft()
)

# --- 4. Create Wedge (End Component) ---
# A tapered block at the end of the tail
end_pos = tail_pts[-1]
wedge_len = 20
wedge_width = 12
wedge_height = 12

wedge = (
    cq.Workplane("XY", origin=end_pos)
    .transformed(offset=(0, 0, -tube_radius), rotate=(0, 0, 195))
    .box(wedge_len, wedge_width, wedge_height, centered=(False, True, False))
    .edges("|Y and >Z") 
    .chamfer(wedge_height - 2)
)

# --- 5. Assembly ---
result = tube.union(nozzle).union(wedge)