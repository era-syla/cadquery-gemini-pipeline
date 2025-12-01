import cadquery as cq

# Geometric Parameters inferred from the image
# The object consists of 4 overlapping cylindrical clips arranged in a line.
num_clips = 4
radius_outer = 10.0
radius_inner = 8.0      # Creates a 2mm wall thickness
height = 60.0
spacing = 18.0          # Spacing < 2*radius_outer (20) creates the overlap/bridge
slot_width = 11.0       # Width of the rectangular cutout on the front
fillet_radius = 2.0     # Smoothing the sharp intersection valleys on the back

# Calculate the center points for each clip unit
# We align them along the X-axis
centers = [(i * spacing, 0) for i in range(num_clips)]

# 1. Generate the Base Solid
# Create a linear array of circles and extrude them.
# Since the circles overlap (spacing 18 vs diameter 20), they automatically fuse into a single solid.
result = (
    cq.Workplane("XY")
    .pushPoints(centers)
    .circle(radius_outer)
    .extrude(height)
)

# 2. Fillet the Back Intersections
# The union of overlapping cylinders creates sharp re-entrant corners (cusps) on the back surface.
# We fillet these vertical edges to match the smooth wavy appearance in the image.
# We select edges parallel to Z (|Z) on the back side.
result = (
    result
    .edges("|Z")
    .fillet(fillet_radius)
)

# 3. Create Internal Cavities
# Cut cylindrical holes for each unit.
# With spacing=18 and radius_inner=8 (diameter 16), the holes do not intersect (18 > 16),
# creating separate compartments with a thin dividing wall, which is typical for such holders.
result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints(centers)
    .circle(radius_inner)
    .cutThruAll()
)

# 4. Cut Front Slots
# Create the rectangular opening for each clip.
# The cut needs to start from the front face and go deep enough to connect with the inner cavity.
# We position the cutting rectangles at the front tangent of the cylinders (y = -radius_outer).
# A height of 2*radius_outer ensures the rectangle extends from y=-20 to y=0 (the center),
# effectively removing the front half of the shell within the slot width.
slot_centers = [(x, -radius_outer) for x, y in centers]

result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints(slot_centers)
    .rect(slot_width, radius_outer * 2.0)
    .cutThruAll()
)