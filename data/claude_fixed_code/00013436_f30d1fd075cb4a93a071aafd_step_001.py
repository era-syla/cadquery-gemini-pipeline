import cadquery as cq

# ==========================================
# 1. Parameter Definitions
# ==========================================
# Main body dimensions
outer_radius = 20.0
cylinder_height = 25.0
dome_radius = outer_radius  # Hemisphere matches cylinder
wall_thickness = 4.0
total_height = cylinder_height + dome_radius

# Cutout dimensions (The "Arch" legs)
num_legs = 3
cut_width = 16.0
cut_height = 32.0   # Height of the cutout from the base
# Arch geometry
arch_radius = cut_width / 2.0
rect_height = cut_height - arch_radius

# Top hole dimensions
hole_diameter = 8.0

# ==========================================
# 2. Geometry Construction
# ==========================================

# --- A. Create the Main Body (Outer Shell) ---
# 1. Cylinder base
outer_cyl = cq.Workplane("XY").circle(outer_radius).extrude(cylinder_height)

# 2. Dome top (Hemisphere)
# Centered at the top of the cylinder to blend perfectly
outer_dome = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height)
    .sphere(outer_radius)
)

# Union cylinder and dome
outer_solid = outer_cyl.union(outer_dome)

# --- B. Create the Inner Body (for Hollowing) ---
inner_radius = outer_radius - wall_thickness

# 1. Inner Cylinder
inner_cyl = cq.Workplane("XY").circle(inner_radius).extrude(cylinder_height)

# 2. Inner Dome
inner_dome = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height)
    .sphere(inner_radius)
)

# Union inner parts
inner_solid = inner_cyl.union(inner_dome)

# Create the hollow shell
main_shell = outer_solid.cut(inner_solid)

# --- C. Create the Side Cutouts ---
# We create a single cutter tool and pattern it rotationally

# Define the 2D profile of the arch on the XZ plane
# Positioned outside the object, facing inwards
cutter_profile = (
    cq.Workplane("XZ")
    .workplane(offset=outer_radius + 5)
    .center(0, 0)
    .moveTo(-cut_width / 2, 0)
    .lineTo(-cut_width / 2, rect_height)
    .threePointArc((0, cut_height), (cut_width / 2, rect_height))
    .lineTo(cut_width / 2, 0)
    .close()
)

# Extrude the cutter inwards to create a solid tool
# Extrude deep enough to pass through the wall but safely past the center
# to avoid clipping the opposite side legs (geometry dependent).
# Here, going slightly past center is safe due to the 120-degree leg spacing.
single_cutter = cutter_profile.extrude(-(outer_radius + 15))

# Create the pattern of 3 cutters
cutters = single_cutter
for i in [1, 2]:
    angle = i * (360.0 / num_legs)
    rotated_cutter = single_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    cutters = cutters.union(rotated_cutter)

# Apply the cuts to the main shell
result_solid = main_shell.cut(cutters)

# --- D. Create the Top Hole ---
# Define a cylinder tool to cut the top hole
hole_tool = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 5)
    .circle(hole_diameter / 2.0)
    .extrude(-20) # Cut downwards into the dome
)

result_solid = result_solid.cut(hole_tool)

# --- E. Final Result ---
result = result_solid