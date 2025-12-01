import cadquery as cq

# Parametric dimensions
disk_radius = 50.0
disk_thickness = 2.0
hole_radius = 1.0
tab_width = 5.0
tab_protrusion = 8.0  # Length the tab sticks out from the edge
tab_overlap = 3.0     # Length the tab goes into the disk for connection

# Create the main circular disk with a center hole
# Defining two circles in the same sketch creates a hole when extruded
main_body = (
    cq.Workplane("XY")
    .circle(disk_radius)
    .circle(hole_radius)
    .extrude(disk_thickness)
)

# Calculate dimensions for the tab geometry
tab_total_length = tab_protrusion + tab_overlap
# Determine the center X coordinate for the tab box
# Start X = disk_radius - tab_overlap
# End X = disk_radius + tab_protrusion
# Center X = (Start X + End X) / 2
tab_center_x = disk_radius + (tab_protrusion - tab_overlap) / 2.0

# Create the rectangular tab
# Using a separate solid and unioning allows for parallel sides on the tab
tab = (
    cq.Workplane("XY")
    .center(tab_center_x, 0)
    .box(tab_total_length, tab_width, disk_thickness)
)

# Combine the disk and the tab into the final result
result = main_body.union(tab)