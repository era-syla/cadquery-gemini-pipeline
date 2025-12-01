import cadquery as cq

# Object Dimensions based on visual analysis
# The object consists of a rectangular handle section and a flared, rounded head.
thickness = 8.0          # Thickness of the plate
handle_len = 60.0        # Length of the straight rectangular section
handle_width = 25.0      # Width of the handle section
flare_len = 40.0         # Length of the tapered section
head_width = 50.0        # Maximum width at the start of the curved tip
tip_protrusion = 10.0    # Distance the curved tip extends beyond the flare end

# Coordinates calculations
# Origin (0,0) is placed at the center of the left (handle) end face logic, 
# but drawing starts from corners for easier lineTo commands.
# We align the centerline with the X-axis.

x_start = 0
x_flare_start = handle_len
x_flare_end = handle_len + flare_len
x_tip = x_flare_end + tip_protrusion

y_handle = handle_width / 2.0
y_head = head_width / 2.0

# Generate the geometry
# 1. Start at the bottom-left corner of the profile
# 2. Draw the rectangular back end
# 3. Draw the straight handle side
# 4. Draw the angled flare side
# 5. Draw the convex arc for the tip
# 6. Mirror the path back to start
result = (
    cq.Workplane("XY")
    .moveTo(x_start, -y_handle)
    .lineTo(x_start, y_handle)                  # Left edge
    .lineTo(x_flare_start, y_handle)            # Top handle edge
    .lineTo(x_flare_end, y_head)                # Top flared edge
    .threePointArc(                             # Rounded tip
        (x_tip, 0), 
        (x_flare_end, -y_head)
    )
    .lineTo(x_flare_start, -y_handle)           # Bottom flared edge
    .close()
    .extrude(thickness)
)