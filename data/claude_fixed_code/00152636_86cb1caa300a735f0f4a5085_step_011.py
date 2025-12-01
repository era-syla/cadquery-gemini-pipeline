import cadquery as cq

# --- Parameters ---
# Main body dimensions
post_width = 12.0
post_depth = 12.0
post_height = 40.0

# Housing (Left Arm) dimensions
housing_length = 25.0
housing_radius = 6.0         # Matches half of post_width
housing_rect_height = 5.0    # Height of the rectangular part above the center axis
housing_hole_radius = 3.5

# Pin (Right Arm) dimensions
pin_length = 20.0
pin_radius = 4.0
pin_chamfer = 1.0

# Slot dimensions (Vertical Post)
slot_width = 4.0
slot_depth = 15.0

# --- Geometry Construction ---

# 1. Central Vertical Post
# Oriented along Z axis. Centered on XY plane.
# Base starts at Z = -housing_radius to align with the bottom of the housing arm.
post = (
    cq.Workplane("XY")
    .workplane(offset=-housing_radius)
    .rect(post_width, post_depth)
    .extrude(post_height)
)

# 2. Left Housing Arm
# Oriented along -X axis.
# Profile created on YZ plane and extruded.
# Profile combines a semi-circle at the bottom and a rectangle on top.
housing_sketch = (
    cq.Sketch()
    .segment((housing_radius, 0), (housing_radius, housing_rect_height))
    .segment((housing_radius, housing_rect_height), (-housing_radius, housing_rect_height))
    .segment((-housing_radius, housing_rect_height), (-housing_radius, 0))
    .arc((-housing_radius, 0), (0, -housing_radius), (housing_radius, 0))
    .assemble()
)

housing = (
    cq.Workplane("YZ")
    .workplane(offset=-post_width/2)
    .placeSketch(housing_sketch)
    .extrude(-housing_length)
)

# 3. Right Pin
# Oriented along +X axis.
# Cylindrical pin extending from the right face of the post.
pin = (
    cq.Workplane("YZ")
    .workplane(offset=post_width/2)
    .circle(pin_radius)
    .extrude(pin_length)
)

# Union the main parts
result = post.union(housing).union(pin)

# --- Cuts and Features ---

# 4. Hole in Housing
# Through-hole along the housing axis (-X).
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=-post_width/2)
    .circle(housing_hole_radius)
    .extrude(-housing_length * 1.5) # Cut through to the end
)

# 5. Slot in Vertical Post
# Cut from the top face downwards.
# The slot separates the post into front and back prongs (cutting along X axis).
result = result.faces(">Z").workplane().rect(post_width * 2, slot_width).cutBlind(-slot_depth)

# --- Fillets and Chamfers ---

# 6. Chamfer Pin Tip
result = result.edges(">X").chamfer(pin_chamfer)

# 7. Fillet Housing Tip
# Rounds off the top front edge of the housing arm.
# Select the edge at the minimum X face and maximum Z.
result = result.edges("<X").edges(">Z").fillet(3.0)

# 8. Fillet Pin Base
# Smooth transition between pin and post.
result = result.edges(cq.NearestToPointSelector((post_width/2, 0, 0))).fillet(1.5)

# 9. Top Post Details
# Chamfer the inner edges of the slot for easy insertion.
# Fillet the outer edges for a smooth finish.
top_edges = result.faces(">Z").edges()
inner_edges = top_edges.vals()
outer_edges = top_edges.vals()

inner_edge_list = [e for e in inner_edges if abs(e.Center().y) < slot_width/2 + 0.1]
outer_edge_list = [e for e in outer_edges if abs(e.Center().y) > slot_width/2 + 0.1]

if inner_edge_list:
    result = result.edges(cq.selectors.BoxSelector(inner_edge_list)).chamfer(0.8)
if outer_edge_list:
    result = result.edges(cq.selectors.BoxSelector(outer_edge_list)).fillet(1.5)

# Return the result