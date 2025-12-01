import cadquery as cq

# Parameters based on visual analysis of the L-shaped bracket
arm_length = 50.0      # Length of the outer edge of each arm
arm_thickness = 10.0   # Width of the arm profile
height = 15.0          # Height of the extrusion

# Create the L-shape profile on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(arm_length, 0)
    .lineTo(arm_length, arm_thickness)
    .lineTo(arm_thickness, arm_thickness)
    .lineTo(arm_thickness, arm_length)
    .lineTo(0, arm_length)
    .close()
    .extrude(height)
)