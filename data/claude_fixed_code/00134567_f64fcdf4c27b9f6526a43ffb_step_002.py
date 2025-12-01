import cadquery as cq

# -- Parameters --
# Geometry estimation derived from the image analysis
num_teeth = 40
gear_od = 60.0          # Outer Diameter estimate (mm)
thickness = 12.0        # Gear thickness
pocket_depth = 4.0      # Depth of the top recess
hole_diameter = 8.0     # Central shaft hole diameter

# Derived Gear Parameters (Standard Spur Gear Logic)
# Module m ~ OD / (N + 2)
module = gear_od / (num_teeth + 2)
pitch_diameter = module * num_teeth
root_diameter = pitch_diameter - (2.5 * module) # Standard root clearance
tooth_height = (gear_od - root_diameter) / 2.0

# Tooth Profile Dimensions (Trapezoidal approximation)
circular_pitch = (3.14159 * pitch_diameter) / num_teeth
tooth_base_width = circular_pitch * 0.60
tooth_tip_width = circular_pitch * 0.35

# Pocket (Recess) Dimensions
# The shape is a "lozenge" formed by a hull of circles
pocket_length = gear_od * 0.70       # Tip-to-tip length
pocket_width = gear_od * 0.25        # Width at the center
pocket_tip_radius = 2.0              # Radius at the pointed ends
pocket_center_radius = pocket_width / 2.0
# Distance from center to the center of the tip circle
tip_offset = (pocket_length / 2.0) - pocket_tip_radius

# -- Construction --

# 1. Base Gear Body
# Create the solid inner root cylinder
base_cyl = cq.Workplane("XY").circle(root_diameter / 2.0).extrude(thickness)

# 2. Gear Teeth
# Define a single tooth profile.
# In a polarArray with rotate=True, the local X axis points Radially outward.
# Height is along X, Width is along Y.
tooth_profile = [
    (0, -tooth_base_width / 2.0),             # Start at root
    (tooth_height, -tooth_tip_width / 2.0),   # Go to tip
    (tooth_height, tooth_tip_width / 2.0),    # Across tip
    (0, tooth_base_width / 2.0)               # Back to root
]

# Generate all teeth and extrude them
teeth = (
    cq.Workplane("XY")
    .polarArray(radius=root_diameter/2.0, startAngle=0, angle=360, count=num_teeth)
    .polyline(tooth_profile)
    .close()
    .extrude(thickness)
)

# Combine root cylinder and teeth
result = base_cyl.union(teeth)

# 3. Recessed Pocket
# Create the lozenge shape on the top face using a convex hull of 3 circles
pocket_shape = (
    cq.Workplane("XY")
    .circle(pocket_center_radius)
    .circle(pocket_tip_radius).translate((-tip_offset, 0, 0))
    .circle(pocket_tip_radius).translate((tip_offset, 0, 0))
    .hull()
    .extrude(pocket_depth)
    .translate((0, 0, thickness - pocket_depth))
)

result = result.cut(pocket_shape)

# 4. Center Hole
# Cut the through-hole for the shaft
result = (
    result.faces(">Z").workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)