import cadquery as cq

# --- Dimensions & Parameters ---
base_width = 44.0          # Width/Length of the square base
base_height = 10.0         # Thickness of the base (including feet)
chamfer_size = 7.0         # Size of the corner chamfers
leg_arch_width = 24.0      # Width of the cutout between legs
leg_arch_height = 5.0      # Height/Depth of the cutout from bottom

post_height = 24.0         # Height of the vertical posts
post_dim_narrow = 6.0      # Narrow dimension of post
post_dim_long = 12.0       # Long dimension of post
post_offset = 11.0         # Distance from center to post center
post_fillet_top = 0.5      # Chamfer size at post top

hole_offset = 16.0         # Distance from center to corner hole center
hole_diameter = 3.4        # Diameter of corner holes
center_hole_dia = 2.0      # Diameter of small center hole

slot_width = 10.0          # Length of side slots
slot_height = 2.5          # Height of side slots
slot_depth = 3.0           # Depth of side slots

# --- 1. Create Base Block ---
# Create a square block and chamfer the corners to create the octagonal-like profile
result = (cq.Workplane("XY")
          .rect(base_width, base_width)
          .extrude(base_height)
          .edges("|Z")
          .chamfer(chamfer_size)
         )

# --- 2. Create Legs (Bottom Cutouts) ---
# Create a cross-shaped cutter to remove material from the bottom, creating the 4 corner legs
# This cuts a channel along X and Y axes from the bottom face.
cutter_x = (cq.Workplane("XY")
            .rect(base_width * 1.5, leg_arch_width)
            .extrude(leg_arch_height))

cutter_y = (cq.Workplane("XY")
            .rect(leg_arch_width, base_width * 1.5)
            .extrude(leg_arch_height))

# Combine cutters and subtract from base
cutters = cutter_x.union(cutter_y)
result = result.cut(cutters)

# --- 3. Create Top Posts ---
# Define positions for the 4 posts
post_locations = [
    (post_offset, post_offset),
    (post_offset, -post_offset),
    (-post_offset, post_offset),
    (-post_offset, -post_offset)
]

# Draw and extrude posts from the top face
# Orientation: Long dimension along Y axis based on visual analysis
posts = (result.faces(">Z").workplane()
         .pushPoints(post_locations)
         .rect(post_dim_narrow, post_dim_long)
         .extrude(post_height)
         )

# Fillet the vertical edges of the posts to create the stadium/lozenge shape
# We select edges within the Z-range of the posts to avoid affecting the base
z_min_posts = base_height + 0.1
z_max_posts = base_height + post_height - 0.1
posts = posts.edges(cq.selectors.BoxSelector(
    (-100, -100, z_min_posts), (100, 100, z_max_posts)
)).fillet(post_dim_narrow / 2.0 - 0.01)

# Add a fillet at the base of the posts (connection to the plate)
# Select edges approximately at Z = base_height
posts = posts.edges(cq.selectors.BoxSelector(
    (-50, -50, base_height - 0.1), (50, 50, base_height + 0.1)
)).fillet(1.5)

# Chamfer the top edges of the posts
posts = posts.faces(">Z").edges().chamfer(post_fillet_top)

result = posts

# --- 4. Create Holes ---
# Corner holes
hole_locations = [
    (hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (-hole_offset, -hole_offset)
]

# Select the main top face of the base (not the post tops)
# This face is located at Z = base_height
result = (result.faces(cq.selectors.NearestToPointSelector((0, 0, base_height)))
          .workplane()
          .pushPoints(hole_locations)
          .circle(hole_diameter / 2.0)
          .cutThruAll()
          )

# Optional Center hole
result = (result.faces(cq.selectors.NearestToPointSelector((0, 0, base_height)))
          .workplane()
          .circle(center_hole_dia / 2.0)
          .cutThruAll()
          )

# --- 5. Create Side Slots ---
# Add slots to the four main vertical faces
for direction in [">X", "<X", ">Y", "<Y"]:
    try:
        result = (result.faces(direction).workplane(centerOption="CenterOfBoundBox")
                  .center(0, 0)
                  .rect(slot_width, slot_height)
                  .cutBlind(-slot_depth)
                 )
    except:
        # Failsafe in case geometry selection is ambiguous
        pass

# Final result is stored in 'result' variable