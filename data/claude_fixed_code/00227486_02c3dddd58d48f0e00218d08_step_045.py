import cadquery as cq

# ---------------------------------------------------------
# Dimensions and Parameters
# ---------------------------------------------------------
plate_thickness = 5.0

# Main body (central rectangular section)
main_width = 70.0
main_height = 50.0

# Side tabs (extensions on left and right)
tab_width = 12.0
tab_height = 30.0

# Central hole
hole_diameter = 18.0

# Left side vertical slot
side_slot_width = 4.0
side_slot_height = 24.0

# T-Slot configuration (for M3 nut traps)
# Positioning relative to center axis
t_slot_x_offset = 18.0  
t_stem_width = 3.2         # Width of the screw channel
t_stem_depth = 5.0         # Depth of the screw channel from edge
t_nut_width = 6.2          # Width of the nut pocket
t_nut_depth = 3.0          # Depth (length) of the nut pocket
t_nut_margin = 2.0         # Distance from edge to start of nut pocket

# ---------------------------------------------------------
# Geometry Construction
# ---------------------------------------------------------

# 1. Define the outline points
# Starting from Top-Right corner of the main body and moving clockwise.
# The shape is a central rectangle with two smaller rectangular tabs on the sides.
pts = [
    (main_width / 2, main_height / 2),              # Top-Right Main
    (main_width / 2, tab_height / 2),               # Step down
    (main_width / 2 + tab_width, tab_height / 2),   # Top-Right Tab
    (main_width / 2 + tab_width, -tab_height / 2),  # Bottom-Right Tab
    (main_width / 2, -tab_height / 2),              # Step in
    (main_width / 2, -main_height / 2),             # Bottom-Right Main
    (-main_width / 2, -main_height / 2),            # Bottom-Left Main
    (-main_width / 2, -tab_height / 2),             # Step out
    (-(main_width / 2 + tab_width), -tab_height / 2), # Bottom-Left Tab
    (-(main_width / 2 + tab_width), tab_height / 2),  # Top-Left Tab
    (-main_width / 2, tab_height / 2),              # Step in
    (-main_width / 2, main_height / 2)              # Top-Left Main
]

# Create the base extrusion
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
)

# 2. Cut the central circular hole
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 3. Cut the rectangular slot on the left tab
# The slot is centered within the left tab area
slot_x_pos = -(main_width / 2 + tab_width / 2)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(slot_x_pos, 0)
    .rect(side_slot_width, side_slot_height)
    .cutThruAll()
)

# 4. Cut the T-Slots
# Helper function to cut a T-slot at a specific x, y location
def cut_t_slot(obj, x, y, is_top_edge):
    # Determine direction to cut into the material (Y axis)
    # If on top edge, we go down (-y). If on bottom edge, we go up (+y).
    direction = -1.0 if is_top_edge else 1.0
    
    # Calculate center positions for the cutouts relative to the edge y
    stem_center_y = y + direction * (t_stem_depth / 2.0)
    nut_center_y = y + direction * (t_nut_margin + t_nut_depth / 2.0)
    
    # Cut the stem (screw channel)
    obj = (
        obj
        .faces(">Z")
        .workplane()
        .center(x, stem_center_y)
        .rect(t_stem_width, t_stem_depth)
        .cutThruAll()
    )
    # Cut the nut pocket
    obj = (
        obj
        .faces(">Z")
        .workplane()
        .center(x, nut_center_y)
        .rect(t_nut_width, t_nut_depth)
        .cutThruAll()
    )
    return obj

# Apply T-slots to Top Edge
for x in [t_slot_x_offset, -t_slot_x_offset]:
    result = cut_t_slot(result, x, main_height / 2, True)

# Apply T-slots to Bottom Edge
for x in [t_slot_x_offset, -t_slot_x_offset]:
    result = cut_t_slot(result, x, -main_height / 2, False)