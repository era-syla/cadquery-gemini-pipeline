import cadquery as cq

# --- Parameters ---
# Overall dimensions
plate_size = 90.0
plate_thickness = 15.0
plate_corner_radius = 8.0

# Mounting holes
hole_spacing = 70.0
hole_diameter = 5.5

# Main pocket
pocket_size = 66.0
pocket_depth = 10.0
pocket_corner_radius = 12.0

# Central Island features
island_width = 38.0  # X dimension
island_length = 22.0 # Y dimension
island_height = 8.0
island_corner_radius = 4.0

# Side Lobes (semi-circular steps)
lobe_radius = 9.0
lobe_height = 3.5

# Inner Pockets
inner_pkt_width = 10.0
inner_pkt_length = 14.0
inner_pkt_depth = 5.0
inner_pkt_spacing = 5.0
inner_pkt_fillet = 2.0

# --- Geometry Construction ---

# 1. Create Base Plate
# Center the part at origin
result = (cq.Workplane("XY")
          .box(plate_size, plate_size, plate_thickness)
          .edges("|Z").fillet(plate_corner_radius)
          )

# 2. Add Mounting Holes
result = (result.faces(">Z").workplane()
          .rarray(hole_spacing, hole_spacing, 2, 2)
          .hole(hole_diameter)
          )

# 3. Cut Main Pocket
# Calculate the floor Z height for later selections
# Box is centered at Z=0, top is at +plate_thickness/2
top_z = plate_thickness / 2.0
floor_z = top_z - pocket_depth

# Create pocket sketch with filleted corners
pocket_sketch = (cq.Workplane("XY")
                 .center(0, pocket_size/2)
                 .line(pocket_size, 0)
                 .line(0, -pocket_size)
                 .line(-pocket_size, 0)
                 .close()
                 .vertices()
                 .fillet(pocket_corner_radius))

result = (result.faces(">Z").workplane()
          .rect(pocket_size, pocket_size)
          .cutBlind(-pocket_depth)
          )

# 4. Construct Central Island
# We select the floor of the pocket to build upwards
floor_selector = cq.selectors.NearestToPointSelector((0, 0, floor_z))

# Create island with filleted corners
island_sketch = (cq.Workplane("XY")
                 .rect(island_width, island_length))

result = (result.faces(floor_selector).workplane()
          .rect(island_width, island_length)
          .extrude(island_height)
          .edges(">Z")
          .edges(cq.selectors.BoxSelector(
              (-island_width, -island_length, floor_z + island_height - 0.1),
              (island_width, island_length, floor_z + island_height + 0.1)))
          .fillet(island_corner_radius)
          )

# 5. Add Side Lobes
# These are semi-circular protrusions on the Y-faces of the island
lobe_y_offset = island_length / 2.0

result = (result.faces(floor_selector).workplane()
          .pushPoints([(0, lobe_y_offset), (0, -lobe_y_offset)])
          .circle(lobe_radius)
          .extrude(lobe_height)
          )

# 6. Cut Inner Pockets
# Select the top face of the newly created island
island_top_z = floor_z + island_height
island_top_selector = cq.selectors.NearestToPointSelector((0, 0, island_top_z))

# Calculate offset for side-by-side pockets
ip_offset_x = (inner_pkt_width + inner_pkt_spacing) / 2.0

# Cut pockets one at a time with fillets
for x_pos in [-ip_offset_x, ip_offset_x]:
    result = (result.faces(island_top_selector).workplane()
              .center(x_pos, 0)
              .rect(inner_pkt_width, inner_pkt_length)
              .cutBlind(-inner_pkt_depth)
              )

# Apply fillets to inner pocket edges
result = result.edges(cq.selectors.BoxSelector(
    (-island_width, -island_length, island_top_z - inner_pkt_depth - 0.1),
    (island_width, island_length, island_top_z - 0.1)
)).fillet(inner_pkt_fillet)

# --- Finishing Touches (Fillets) ---

# A. Fillet the pocket floor
result = result.edges(cq.selectors.BoxSelector(
    (-plate_size, -plate_size, floor_z - 0.1),
    (plate_size, plate_size, floor_z + 0.1)
)).fillet(2.0)

# B. Fillet top edge of the central island
result = result.edges(cq.selectors.BoxSelector(
    (-island_width/2 - 0.1, -island_length/2 - 0.1, island_top_z - 0.1),
    (island_width/2 + 0.1, island_length/2 + 0.1, island_top_z + 0.1)
)).fillet(1.0)

# C. Fillet top edge of the side lobes
lobe_top_z = floor_z + lobe_height
result = result.edges(cq.selectors.BoxSelector(
    (-lobe_radius - 0.1, -island_length/2 - lobe_radius - 0.1, lobe_top_z - 0.1),
    (lobe_radius + 0.1, island_length/2 + lobe_radius + 0.1, lobe_top_z + 0.1)
)).fillet(1.0)

# D. Small chamfer/fillet on the outer top rim
result = result.edges(cq.selectors.BoxSelector(
    (-plate_size, -plate_size, top_z - 0.1),
    (plate_size, plate_size, top_z + 0.1)
)).fillet(0.5)