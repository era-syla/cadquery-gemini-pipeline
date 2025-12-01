import cadquery as cq

# Dimensions
pipe_radius = 5.0
bend_radius = 25.0
straight_length = 60.0

# Create the model
# 1. Create a wire path for the hook shape
# Start at origin, go up straight_length, then arc 180 degrees
path = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, straight_length)
    .radiusArc((0, straight_length + bend_radius * 2), bend_radius)
)

# 2. Sweep a circle along the path to create the pipe
result = (
    cq.Workplane("XY")
    .circle(pipe_radius)
    .sweep(path)
)