import cadquery as cq

# Parameters defined based on standard brick dimensions and visual inspection
cols = 4
rows = 2
pitch = 8.0  # Standard distance between stud centers
block_height = 9.6
stud_height = 1.7
stud_outer_diameter = 4.8
stud_inner_diameter = 3.2  # Inner diameter to create the hollow tube look

# Calculated overall dimensions
length = cols * pitch
width = rows * pitch

# 1. Create the rectangular base block
# Centered at origin for easier symmetry operations
result = cq.Workplane("XY").box(length, width, block_height)

# 2. Add the array of hollow studs on top
result = (
    result
    .faces(">Z")
    .workplane()
    .rarray(pitch, pitch, cols, rows)
    .circle(stud_outer_diameter / 2.0)
    .extrude(stud_height)
    .faces(">Z")
    .workplane()
    .rarray(pitch, pitch, cols, rows)
    .circle(stud_inner_diameter / 2.0)
    .cutThruAll()
)