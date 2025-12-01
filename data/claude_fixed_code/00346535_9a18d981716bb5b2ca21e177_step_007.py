import cadquery as cq

# Parametric dimensions of the table
length = 120.0       # Length of the table top
width = 60.0         # Width of the table top
height = 50.0        # Total height of the table
top_thickness = 5.0  # Thickness of the table top
leg_width = 5.0      # Width/Depth of the square legs

# Calculate the height of the legs
leg_height = height - top_thickness

# Calculate the x and y offsets for the leg centers so they are flush with the corners
# Center position = (Total Length / 2) - (Leg Width / 2)
x_dist = (length / 2.0) - (leg_width / 2.0)
y_dist = (width / 2.0) - (leg_width / 2.0)

# Define the centers of the four legs
leg_centers = [
    (x_dist, y_dist),
    (x_dist, -y_dist),
    (-x_dist, y_dist),
    (-x_dist, -y_dist)
]

# Create the legs
# Start on XY plane, position points, draw rectangles, and extrude up
legs = (
    cq.Workplane("XY")
    .pushPoints(leg_centers)
    .rect(leg_width, leg_width)
    .extrude(leg_height)
)

# Create the table top
# Create a workplane at the top of the legs, then create the box
top = (
    cq.Workplane("XY")
    .workplane(offset=leg_height)
    .center(0, 0)
    .box(length, width, top_thickness)
)

# Combine legs and top into the final model
result = legs.union(top)