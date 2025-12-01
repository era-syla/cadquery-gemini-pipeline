import cadquery as cq

# Overall dimensions of the enclosure
length = 90.0
width = 45.0
height = 30.0
wall_thickness = 3.0

# Internal feature dimensions
rib_thickness = 3.0
rib_height = 14.0
boss_size = 8.0

# 1. Create the main box and shell it to create the open enclosure
# We create a solid box and shell the top face (+Z) inwards
result = cq.Workplane("XY").box(length, width, height).faces("+Z").shell(-wall_thickness)

# Calculate Z level of the internal floor for placing internal components
floor_z = -height/2 + wall_thickness

# 2. Add Internal Ribs
# These are transverse walls connecting the long sides, shorter than the main walls
# Internal width
internal_w = width - 2 * wall_thickness

# Rib 1 (closer to front)
rib1 = (cq.Workplane("XY")
        .box(rib_thickness, internal_w, rib_height)
        .translate((-15, 0, floor_z + rib_height/2)))

# Rib 2 (closer to back)
rib2 = (cq.Workplane("XY")
        .box(rib_thickness, internal_w, rib_height)
        .translate((20, 0, floor_z + rib_height/2)))

# Union the ribs to the main body
result = result.union(rib1).union(rib2)

# 3. Add Boss (Square block on floor)
# Located near the front wall
boss = (cq.Workplane("XY")
        .box(boss_size, boss_size, boss_size)
        .translate((-32, 0, floor_z + boss_size/2)))

result = result.union(boss)

# 4. Create Front Cutout (Stepped Notch)
# Located on the -X face
# Dimensions for the stepped profile
wide_cut_w = 22.0
wide_cut_d = 8.0
narrow_cut_w = 12.0
narrow_cut_d = 5.0

# Define the points for the stepped profile relative to face center
# Local coordinates: Top edge is at y = height/2
y_top = height / 2
y_step = y_top - wide_cut_d
y_bottom = y_step - narrow_cut_d
x_outer = wide_cut_w / 2
x_inner = narrow_cut_w / 2

notch_profile = [
    (-x_outer, y_top),
    (-x_outer, y_step),
    (-x_inner, y_step),
    (-x_inner, y_bottom),
    (x_inner, y_bottom),
    (x_inner, y_step),
    (x_outer, y_step),
    (x_outer, y_top)
]

# Apply the cut to the front face (<X)
result = (result.faces("<X").workplane()
          .polyline(notch_profile).close()
          .cutThruAll())

# 5. Create Back Cutout (Deep Rectangular Slot)
# Located on the +X face
back_cut_w = 20.0
back_cut_d = 16.0

# Calculate center for the rectangle relative to face center
# Align with top edge (y = height/2)
cut_center_y = (height / 2) - (back_cut_d / 2)

# Apply the cut to the back face (>X)
result = (result.faces(">X").workplane()
          .center(0, cut_center_y)
          .rect(back_cut_w, back_cut_d)
          .cutThruAll())