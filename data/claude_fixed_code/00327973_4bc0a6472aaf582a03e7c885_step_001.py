import cadquery as cq

# Dimensions
height = 80.0
width = 50.0
thickness = 6.0

frame_width = 6.0        # Width of the outer frame
mid_rail_height = 6.0    # Vertical space between top and bottom panels
bottom_panel_height = 15.0
recess_depth = 2.0       # Depth of the cuts
chamfer_angle = 45.0     # Angle for the top panel beveled edges (positive for inward taper)

# 1. Create the base block
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Create the Bottom Pocket (Rectangular Cut)
# Calculate position relative to the center
# Bottom edge is at y = -height/2
bot_center_y = (-height / 2) + frame_width + (bottom_panel_height / 2)
bot_width = width - (2 * frame_width)

# Select the front face and cut the bottom pocket
result = (
    result.faces(">Z")
    .workplane()
    .center(0, bot_center_y)
    .rect(bot_width, bottom_panel_height)
    .cutBlind(-recess_depth)
)

# 3. Create the Top Pocket (Tapered/Chamfered Cut)
# Calculate vertical space available for the top panel
top_y_start = (-height / 2) + frame_width + bottom_panel_height + mid_rail_height
top_y_end = (height / 2) - frame_width
top_height = top_y_end - top_y_start
top_center_y = (top_y_start + top_y_end) / 2
top_width = width - (2 * frame_width)

# Select the front face again and cut the top pocket with a taper
# The taper creates the beveled 'picture frame' appearance shown in the image
result = (
    result.faces(">Z")
    .workplane()
    .center(0, top_center_y)
    .rect(top_width, top_height)
    .cutBlind(-recess_depth, taper=chamfer_angle)
)