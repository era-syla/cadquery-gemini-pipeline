import cadquery as cq

# Geometric Parameters derived from the image analysis
# The object is a flat plate with an eccentric outer profile relative to a circular hole.
thickness = 5.0
hole_diameter = 15.0
outer_radius = 50.0

# The outer circular profile is not concentric with the hole.
# Visually, there is more material above the hole than below.
# We define the hole at the origin (0,0).
outer_arc_center_y = 15.0  # Center of the large radius relative to the hole center

# The bottom is cut flat.
# Distance from the hole center down to the flat edge.
flat_bottom_offset = 20.0

# 1. Create the base body: The outer circular profile
# We center this circle at (0, outer_arc_center_y)
base = (
    cq.Workplane("XY")
    .center(0, outer_arc_center_y)
    .circle(outer_radius)
    .extrude(thickness)
)

# 2. Cut the flat bottom
# We create a rectangular solid to subtract material below the cut line.
# The cut line is at y = -flat_bottom_offset.
# We position a large rectangle such that its top edge aligns with this line.
cut_height = outer_radius * 2
cut_width = outer_radius * 3
cut_center_y = -flat_bottom_offset - (cut_height / 2)

flat_cut_tool = (
    cq.Workplane("XY")
    .center(0, cut_center_y)
    .rect(cut_width, cut_height)
    .extrude(thickness)
)

result = base.cut(flat_cut_tool)

# 3. Create the hole
# The hole is centered at the origin (0,0).
result = (
    result.faces(">Z")
    .workplane()
    .hole(hole_diameter)
)