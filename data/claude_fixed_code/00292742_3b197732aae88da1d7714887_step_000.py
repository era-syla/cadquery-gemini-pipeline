import cadquery as cq
import math

# Parametric definitions
length = 1200.0       # Total length of the truss
height = 60.0         # Height of the truss (centerline to centerline)
member_size = 5.0     # Width/Thickness of the square tubing
num_bays = 24         # Number of truss segments

# derived parameters
bay_length = length / num_bays

# 1. Create Top and Bottom Chords
# We use square tubes.
# Bottom Chord aligned along X-axis, Y=0
bottom_chord = (
    cq.Workplane("XY")
    .box(length, member_size, member_size)
    .translate((length / 2, 0, 0))
)

# Top Chord aligned along X-axis, Y=height
top_chord = (
    cq.Workplane("XY")
    .box(length, member_size, member_size)
    .translate((length / 2, height, 0))
)

# Start combining into a single result
result = bottom_chord.union(top_chord)

# 2. Create Verticals and Diagonals loop
for i in range(num_bays + 1):
    x_loc = i * bay_length
    
    # Vertical Member
    # Extends from bottom chord to top chord
    vert = (
        cq.Workplane("XY")
        .box(member_size, height, member_size)
        .translate((x_loc, height / 2, 0))
    )
    result = result.union(vert)
    
    # Diagonal Member
    # Connects top of current vertical to bottom of next vertical (N-truss pattern)
    if i < num_bays:
        # Calculate geometry
        delta_x = bay_length
        delta_y = height
        diag_len = math.hypot(delta_x, delta_y)
        angle = -math.degrees(math.atan2(delta_y, delta_x))
        
        # Midpoint for positioning
        mid_x = x_loc + bay_length / 2
        mid_y = height / 2
        
        diag = (
            cq.Workplane("XY")
            .box(diag_len, member_size, member_size)
            .translate((diag_len / 2, 0, 0))
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .translate((x_loc, height, 0))
        )
        result = result.union(diag)

# The variable 'result' now contains the final truss geometry