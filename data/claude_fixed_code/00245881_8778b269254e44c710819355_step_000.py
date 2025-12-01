import cadquery as cq

# Object Dimensions derived from image analysis
width = 50.0          # Overall width of the base
depth = 40.0          # Overall depth of the base
base_height = 10.0    # Thickness of the base plate
tower_height = 30.0   # Total height of the side towers (from bottom)
tower_width = 15.0    # Width of the tower blocks
tower_depth = 15.0    # Depth of the tower blocks
hole_diameter = 6.0   # Diameter for all holes

# 1. Create the Base Plate
# Centered on XY plane, extending from Z=0 to Z=base_height
result = cq.Workplane("XY").box(width, depth, base_height, centered=(True, True, False))

# 2. Add the Rear Towers
# Calculate center positions for the towers relative to global origin
# Y: Aligned with the back edge. Center is at (depth/2) - (tower_depth/2)
# X: Aligned with side edges. Center is at +/-(width/2 - tower_width/2)
tower_y_center = (depth / 2.0) - (tower_depth / 2.0)
tower_x_offset = (width / 2.0) - (tower_width / 2.0)

tower_centers = [
    (-tower_x_offset, tower_y_center),
    (tower_x_offset, tower_y_center)
]

# Select top face of base, place rectangles, and extrude upwards
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(tower_centers)
    .rect(tower_width, tower_depth)
    .extrude(tower_height - base_height)
)

# 3. Create Side Holes
# These go horizontally (X-axis) through the towers.
# We use the YZ plane to define the circle profile and cut through the object.
# Position: Centered in tower depth (Y) and vertically in the tower extension (Z).
side_hole_z = base_height + (tower_height - base_height) / 2.0
side_hole_y = tower_y_center

result = (
    result
    .faces(">X")
    .workplane()
    .center(side_hole_y, side_hole_z)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

result = (
    result
    .faces("<X")
    .workplane()
    .center(side_hole_y, side_hole_z)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 4. Create Front Hole
# Vertical hole centered on the front shelf section.
# Shelf Y range is from front edge (-depth/2) to the start of the towers.
shelf_front_y = -depth / 2.0
shelf_back_y = (depth / 2.0) - tower_depth
front_hole_y = (shelf_front_y + shelf_back_y) / 2.0

result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, front_hole_y)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)