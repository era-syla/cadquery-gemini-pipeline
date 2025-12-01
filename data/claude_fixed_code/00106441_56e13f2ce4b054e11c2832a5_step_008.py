import cadquery as cq

# Dimensions based on visual analysis
length = 100.0         # Total length of the bar
height = 12.0          # Total height
width_straight = 20.0  # Width of the rectangular portion
arc_bulge = 5.0        # How much the curved side extends out
step_width = 2.5       # Width of the rebate/groove on the top-left
step_depth = 3.0       # Depth of the rebate from the top
block_length = 15.0    # Length of the raised tab at the near end
block_stickout = 3.0   # Height the tab extends above the main top surface

# Calculated dimensions
total_width = width_straight + arc_bulge
shelf_height = height - step_depth

# 1. Create the main extruded body
# We draw the profile on the YZ plane (Side view) and extrude along X (Length)
# Origin (0,0) is at the bottom-left corner of the cross-section
main_body = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(width_straight, 0)  # Bottom straight edge
    # Create the curved right side (convex airfoil/teardrop shape)
    # Arc from current point to top-right corner, passing through the bulge point
    .threePointArc((total_width, height / 2.0), (width_straight, height))
    .lineTo(step_width, height)           # Top edge inwards
    .lineTo(step_width, shelf_height)     # Vertical step down (rebate wall)
    .lineTo(0, shelf_height)              # Horizontal step out (rebate floor)
    .close()                              # Line back to (0,0) completes the left wall
    .extrude(length)
)

# 2. Create the raised block/tab feature at the near end
# This block sits in the rebate created above and extends upwards
# Total height of block = depth of step to fill + extra stickout
block_total_height = step_depth + block_stickout

block = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, shelf_height))  # Start drawing at the level of the rebate shelf
    # Create a box aligned with the origin (which corresponds to the rebate corner)
    # Dimensions: Length (X), Width (Y), Height (Z)
    .box(block_length, step_width, block_total_height, centered=False)
)

# 3. Combine the main body and the block into a single object
result = main_body.union(block)