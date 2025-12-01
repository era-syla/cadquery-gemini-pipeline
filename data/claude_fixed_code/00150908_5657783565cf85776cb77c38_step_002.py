import cadquery as cq

# --- Dimensions based on image analysis ---
# Base Wall Plate dimensions
plate_height = 30.0  # Vertical dimension (Z)
plate_width = 50.0   # Horizontal dimension along wall (Y)
plate_thick = 10.0   # Thickness coming off the wall (X)

# Arm dimensions
arm_width = 15.0     # Width of the rectangular bars
arm_thick = 10.0     # Height/Thickness of the bars
arm1_len = 140.0     # Length of the first arm segment
arm2_len = 180.0     # Length of the second arm segment

# Joint and Pin dimensions
joint_radius = arm_width / 2.0
pin_dia = 6.0        # Diameter of the vertical pin at the end
pin_height = 15.0    # Height of the pin
elbow_pin_head_h = 2.0 # Height of the small decorative pin head at the elbow

# --- Geometry Construction ---

# 1. Base Plate
# Oriented on the YZ plane. We offset it so the front face is at X=0.
base = (
    cq.Workplane("YZ")
    .box(plate_width, plate_height, plate_thick)
    .translate((-plate_thick / 2.0, 0, 0))
)

# 2. Arm 1 (Proximal Arm)
# Extends along the X-axis from the center of the base plate.
# We position a box such that it starts at X=0 and extends to X=arm1_len.
arm1 = (
    cq.Workplane("XY")
    .box(arm1_len, arm_width, arm_thick)
    .translate((arm1_len / 2.0, 0, 0))
)

# 3. Elbow Joint (Connection between arms)
# Modeled as a cylinder to create rounded corners at the joint.
# Positioned at the end of Arm 1.
elbow_pos = (arm1_len, 0)
elbow = (
    cq.Workplane("XY")
    .center(elbow_pos[0], elbow_pos[1])
    .circle(joint_radius)
    .extrude(arm_thick)
    .translate((0, 0, -arm_thick / 2.0))
)

# Elbow Pin Head (Small detail visible in the image on top of the joint)
elbow_pin = (
    cq.Workplane("XY")
    .center(elbow_pos[0], elbow_pos[1])
    .circle(pin_dia / 2.0 + 1.5)
    .extrude(elbow_pin_head_h)
    .translate((0, 0, arm_thick / 2.0))
)

# 4. Arm 2 (Distal Arm)
# Extends along the Y-axis (creating an L-shape) from the elbow.
# Starts at the elbow Y=0 and goes to Y=arm2_len.
arm2 = (
    cq.Workplane("XY")
    .box(arm_width, arm2_len, arm_thick)
    .translate((arm1_len, arm2_len / 2.0, 0))
)

# 5. Distal Tip
# Rounded end of the second arm.
tip_pos = (arm1_len, arm2_len)
tip = (
    cq.Workplane("XY")
    .center(tip_pos[0], tip_pos[1])
    .circle(joint_radius)
    .extrude(arm_thick)
    .translate((0, 0, -arm_thick / 2.0))
)

# 6. Distal Pin
# The vertical pin sticking up from the end of the arm.
distal_pin = (
    cq.Workplane("XY")
    .center(tip_pos[0], tip_pos[1])
    .circle(pin_dia / 2.0)
    .extrude(pin_height)
    .translate((0, 0, arm_thick / 2.0))
)

# --- Final Assembly ---
# Union all components into a single solid object
result = (
    base
    .union(arm1)
    .union(elbow)
    .union(elbow_pin)
    .union(arm2)
    .union(tip)
    .union(distal_pin)
)