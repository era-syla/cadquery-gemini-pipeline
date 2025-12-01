import cadquery as cq

# Dimensions
prism_length = 100.0
prism_height = 50.0
prism_top_width = 60.0

# Cut dimensions
cut_depth = 25.0
tail_length = 15.0
tail_width = 20.0  # Narrower than prism width at cut depth (creates a floor)
head_length = 25.0
head_width = 50.0  # Wider than prism width at cut depth (breaks through sides)

# 1. Create the triangular prism
# Oriented along X axis, cross-section in YZ plane
# Inverted triangle: Flat top at +Z
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0), 
        (prism_top_width / 2, prism_height), 
        (-prism_top_width / 2, prism_height)
    ])
    .close()
    .extrude(prism_length / 2, both=True)
)

# 2. Create the Arrow-shaped cut
# Defined on the top face (XY plane) and cut downwards (Z axis)
# The profile consists of a rectangular "tail" and a triangular "head"
# The differing widths create the "blind floor" vs "through hole" effect
result = (
    result
    .faces(">Z")
    .workplane()
    .polyline([
        (-tail_length, tail_width/2),
        (0, tail_width/2),
        (0, head_width/2),
        (head_length, 0),
        (0, -head_width/2),
        (0, -tail_width/2),
        (-tail_length, -tail_width/2)
    ])
    .close()
    .cutBlind(-cut_depth)
)