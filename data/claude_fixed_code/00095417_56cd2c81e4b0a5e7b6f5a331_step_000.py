import cadquery as cq

# --- Parameter Definitions ---
thickness = 3.0

# --- Part 1: Main Chassis Plate (Left Object) ---
# Coordinates approximated from visual inspection to recreate the profile
# Origin (0,0) is placed at the bottom-left corner

# Define profile points (Counter-Clockwise)
plate_pts = [
    (0, 12),        # Start of left vertical edge
    (25, 42),       # Top of left angled chamfer/slope
    (70, 50),       # Start of top edge transition
    (82, 68),       # Top-left of the "hump"
    (102, 68),      # Top-right of the "hump"
    (115, 52),      # Bottom-right of hump (shoulder)
    (115, 35),      # Vertical drop to step
    (128, 35),      # Horizontal step out
    (128, 20),      # Vertical drop of the "tail"
    (110, 0),       # Angled cut to bottom
    (0, 0)          # Bottom left corner
]

# Create the base solid for the plate
plate = (
    cq.Workplane("XY")
    .polyline(plate_pts)
    .close()
    .extrude(thickness)
)

# Apply fillets to smooth out the profile similar to the image
# Using simple edge selection without filterBy or select
plate = plate.edges("|Z").fillet(2.0)

# Add Holes and Cutouts to the Plate
plate = (
    plate.faces(">Z").workplane()
    # Large central hole (approx 14mm dia)
    .pushPoints([(78, 45)])
    .hole(14.0)
)

# Horizontal slots
for x_pos in [42, 58]:
    plate = (
        plate.faces(">Z").workplane()
        .center(x_pos, 28)
        .rect(10, 3)
        .cutThruAll()
    )

# Small mounting holes
plate = (
    plate.faces(">Z").workplane()
    .pushPoints([
        (15, 8),   # Bottom left
        (90, 8),   # Bottom right
        (92, 58),  # On the hump
        (122, 28)  # On the right tail
    ])
    .hole(3.2)
)

# --- Part 2: Servo Arm / Lever (Right Object) ---
# Create the second object and position it to the right

arm_origin_x = 190
arm_origin_y = 45

# Create the main arm shape using hull of two circles (lofted 2D shape)
arm_base = (
    cq.Workplane("XY")
    .moveTo(arm_origin_x, arm_origin_y)
    .circle(12)  # Pivot end radius
    .moveTo(arm_origin_x - 45, arm_origin_y - 25)
    .circle(9)   # Tip end radius
    .hull()
    .extrude(thickness)
)

# Add the small hook/latch feature near the pivot
hook = (
    cq.Workplane("XY")
    .center(arm_origin_x + 9, arm_origin_y - 6)
    .rect(8, 12)
    .extrude(thickness)
)
arm = arm_base.union(hook)

# Add Holes to Arm
# Main Pivot hole
arm = (
    arm.faces(">Z").workplane()
    .pushPoints([(arm_origin_x, arm_origin_y)])
    .hole(6.0)
)

# Tip holes
tip_x = arm_origin_x - 45
tip_y = arm_origin_y - 25

# Center hole
arm = (
    arm.faces(">Z").workplane()
    .pushPoints([(tip_x, tip_y)])
    .hole(4.0)
)

# Ring of 6 holes
import math
for i in range(6):
    angle = i * 60 * math.pi / 180
    hole_x = tip_x + 6.0 * math.cos(angle)
    hole_y = tip_y + 6.0 * math.sin(angle)
    arm = (
        arm.faces(">Z").workplane()
        .pushPoints([(hole_x, hole_y)])
        .hole(2.0)
    )

# --- Final Result ---
# Combine both objects into a single result
result = plate.union(arm)