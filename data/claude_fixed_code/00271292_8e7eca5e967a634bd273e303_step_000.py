import cadquery as cq

# --- Parameter Definitions ---
# Base Plate dimensions
base_width = 46.0
base_depth = 32.0
base_thickness = 3.0
base_corner_fillet = 4.0

# Rear Tab dimensions
tab_radius = 8.0
# Tab is centered on the back edge (Y axis)
tab_center_y = base_depth / 2.0
tab_hole_diameter = 5.0

# Central Rectangular Boss dimensions
rect_boss_width = 22.0
rect_boss_depth = 14.0
rect_boss_height = 10.0
rect_boss_wall_thickness = 2.0

# Cylindrical Bosses dimensions
cyl_boss_spacing = 16.5  # Distance from center to cylinder center
cyl_boss_od = 9.0
cyl_boss_id = 5.0

# --- Geometry Construction ---

# 1. Base Plate construction using a Sketch
# Union of a rectangle and a circle for the back tab
base_sketch = (
    cq.Sketch()
    .rect(base_width, base_depth)
    .push([(0, tab_center_y)])
    .circle(tab_radius)
    .clean()  # Fuses the shapes
)

# Extrude base and fillet corners
# We filter edges to fillet only the main corners, avoiding the tab connection
base = cq.Workplane("XY").placeSketch(base_sketch).extrude(base_thickness)
base = base.edges("|Z").filter(lambda e: abs(e.Center().x) > 10).fillet(base_corner_fillet)

# 2. Create the features on top of the base
# Define a workplane on the top face of the base
top_plane = base.faces(">Z").workplane()

# Generate Central Rectangular Boss (Solid)
center_boss = (
    top_plane
    .rect(rect_boss_width, rect_boss_depth)
    .extrude(rect_boss_height)
)

# Generate Side Cylindrical Bosses (Solid)
side_bosses = (
    top_plane
    .pushPoints([(-cyl_boss_spacing, 0), (cyl_boss_spacing, 0)])
    .circle(cyl_boss_od / 2.0)
    .extrude(rect_boss_height)
)

# Combine all solid parts
result = base.union(center_boss).union(side_bosses)

# 3. Cut Holes
# Select the top-most faces (top of bosses) to start the cuts
# Cut the rectangular pocket
result = (
    result.faces(">Z").workplane()
    .rect(rect_boss_width - 2*rect_boss_wall_thickness, 
          rect_boss_depth - 2*rect_boss_wall_thickness)
    .cutBlind(rect_boss_height - base_thickness)
)

# Cut the holes in the cylindrical bosses
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-cyl_boss_spacing, 0), (cyl_boss_spacing, 0)])
    .circle(cyl_boss_id / 2.0)
    .cutBlind(rect_boss_height - base_thickness)
)

# Cut the hole in the back tab
# We cut from the bottom face for clarity
result = (
    result.faces("<Z").workplane()
    .center(0, tab_center_y)
    .circle(tab_hole_diameter / 2.0)
    .cutThruAll()
)