import cadquery as cq

# --- Parameters ---
# Gear properties estimation based on image
num_teeth = 30
module = 2.0
pressure_angle = 20.0
thickness = 10.0

# Derived Gear Dimensions
pitch_diameter = module * num_teeth
outer_diameter = pitch_diameter + 2 * module  # ~64mm
root_diameter = pitch_diameter - 2.5 * module # ~55mm
root_radius = root_diameter / 2.0
outer_radius = outer_diameter / 2.0

# Shaft (Center Hole) properties
shaft_diameter = 12.0
shaft_radius = shaft_diameter / 2.0
# The flat is a D-profile. distance from center to flat face.
# If radius is 6, a standard D-cut might be at 4.5mm or 5mm from center.
flat_dist = 4.5 

# --- 1. Base Gear Body ---
# Create the central cylinder (root of the gear)
base_gear = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# --- 2. Teeth Generation ---
# We approximate the involute profile with a trapezoid for robust generation 
# without external libraries.
# Dimensions of the tooth cross-section:
# Width at root is slightly larger than space
tooth_root_width = (3.14159 * module) / 2.0 * 1.1 
tooth_tip_width = (3.14159 * module) / 2.0 * 0.6

# Define vertices for one tooth (centered on X axis)
# Overlap slightly with root_radius (-0.1) to ensure clean boolean union
tooth_pts = [
    (root_radius - 0.1, -tooth_root_width / 2.0),
    (outer_radius, -tooth_tip_width / 2.0),
    (outer_radius, tooth_tip_width / 2.0),
    (root_radius - 0.1, tooth_root_width / 2.0)
]

# Create all teeth using a loop approach
result = base_gear
for i in range(num_teeth):
    angle = 360.0 * i / num_teeth
    tooth = (
        cq.Workplane("XY")
        .polyline(tooth_pts)
        .close()
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(tooth)

# --- 3. Center D-Hole ---
# The hole is a circle with a chord (flat side).
# We construct the "negative" shape (the tool) to cut from the gear.
# Tool = Cylinder INTERSECT Box(that preserves the D-shape)

# Step A: Cylinder representing the full bore
bore_cyl = cq.Workplane("XY").circle(shaft_radius).extrude(thickness)

# Step B: Box representing the material to keep (the D-shape volume)
# We assume the flat is horizontal at Y = flat_dist. 
# We want to keep the part of the circle where Y < flat_dist.
# So we intersect with a large box positioned to cover Y < flat_dist.
box_height = shaft_radius * 3
box_center_y = flat_dist - (box_height / 2.0)

# Create the bounding box for intersection
d_profile_bound = (
    cq.Workplane("XY")
    .center(0, box_center_y)
    .rect(shaft_radius * 3, box_height)
    .extrude(thickness)
)

# Step C: Intersect to create the D-shaped plug
d_hole_tool = bore_cyl.intersect(d_profile_bound)

# --- 4. Final Operation ---
# Cut the D-hole from the gear body
result = result.cut(d_hole_tool)