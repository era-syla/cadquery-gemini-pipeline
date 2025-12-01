import cadquery as cq

# Parameters for dimensions
box_length = 40.0
box_width = 25.0
box_height = 20.0

cyl_radius = 8.0
cyl_length = 20.0
gap = 5.0

# Create the rectangular box centered at the origin
box = cq.Workplane("XY").box(box_length, box_width, box_height)

# Calculate the center position for the cylinder
# It is positioned to the right of the box along the X-axis
cyl_center_x = (box_length / 2.0) + gap + (cyl_length / 2.0)

# Create the cylinder
# Initial cylinder is aligned with Z-axis, rotate 90 degrees around Y-axis to align with X-axis
cyl = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(cyl_radius)
    .extrude(cyl_length)
    .translate((cyl_center_x, 0, 0))
)

# Combine the two shapes into the final result
result = box.union(cyl)