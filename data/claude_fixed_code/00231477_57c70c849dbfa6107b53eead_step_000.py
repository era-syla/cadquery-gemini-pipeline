import cadquery as cq

# --- Dimensions & Parameters ---
# Main body dimensions
main_width = 46.0      # X dimension
main_length = 40.0     # Y dimension
main_height = 10.0     # Z dimension
wall_thickness = 3.0
floor_thickness = 2.0
corner_radius = 4.0

# Mounting Tabs (Ears)
tab_projection = 9.0   # Distance from main body to tab center
tab_radius = 5.0
tab_hole_dia = 4.0
tab_thickness = 3.0    # Flush with bottom

# Central Island
island_width = 22.0
island_length = 14.0
island_height = 7.0    # From floor (Total height from Z=0 is floor + island_h)
island_radius = 3.0
island_rim_height = 0.5
island_rim_thick = 0.6

# Island Internal Pockets
pocket_size_x = 6.0
pocket_size_y = 8.0
pocket_gap = 2.0

# Corner Holes
corner_hole_dia = 2.2

# --- Construction ---

# 1. Base Main Body (Rectangular Block with rounded corners)
main_body = (
    cq.Workplane("XY")
    .rect(main_width, main_length)
    .extrude(main_height)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Create the Main Cavity (Pocket)
# Calculate inner dimensions
inner_w = main_width - 2 * wall_thickness
inner_l = main_length - 2 * wall_thickness
inner_r = corner_radius - wall_thickness
if inner_r < 0.1: inner_r = 0.1 # Safety clamp

pocket_cut = (
    main_body.faces(">Z")
    .workplane()
    .rect(inner_w, inner_l)
    .cutBlind(-(main_height - floor_thickness))
)

result = pocket_cut

# 3. Mounting Tabs
# Function to generate a tab on left or right side
def create_tab(direction):
    # direction: 1 for right (+X), -1 for left (-X)
    center_x = direction * (main_width / 2 + tab_projection)
    
    # Create the circular tip
    tip = (
        cq.Workplane("XY")
        .center(center_x, 0)
        .circle(tab_radius)
        .extrude(tab_thickness)
    )
    
    # Create a base rectangle that intersects with the main body wall
    # to ensure a solid connection.
    # Overlap slightly into the body
    overlap = 2.0
    rect_x = direction * (main_width / 2 - overlap / 2)
    # Width at the root is slightly wider than diameter to allow for smooth transition
    root_width = tab_radius * 2 + 4.0 
    
    base = (
        cq.Workplane("XY")
        .center(rect_x, 0)
        .rect(overlap + 2, root_width)
        .extrude(tab_thickness)
    )
    
    # Union the circle and the base rectangle to form the tab shape
    tab_geo = tip.union(base)
    
    # Cut the mounting hole
    tab_geo = (
        tab_geo.faces(">Z")
        .workplane()
        .center(center_x, 0)
        .circle(tab_hole_dia / 2)
        .cutThruAll()
    )
    return tab_geo

# Generate and union tabs
result = result.union(create_tab(1)).union(create_tab(-1))

# 4. Corner Holes in the Main Rim
# Locations relative to center
dx = main_width / 2 - corner_radius
dy = main_length / 2 - corner_radius
hole_locs = [(dx, dy), (dx, -dy), (-dx, dy), (-dx, -dy)]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locs)
    .circle(corner_hole_dia / 2)
    .cutThruAll()
)

# 5. Central Island Structure
# Create workplane on the floor of the pocket
floor_plane = cq.Workplane("XY").workplane(offset=floor_thickness)

island = (
    floor_plane
    .rect(island_width, island_length)
    .extrude(island_height)
    .edges("|Z")
    .fillet(island_radius)
)

# 6. Island Details: Inner Pockets
# Two rectangular pockets inside the island
hole_offset = pocket_size_x / 2 + pocket_gap / 2
island_hole_centers = [(-hole_offset, 0), (hole_offset, 0)]

island = (
    island.faces(">Z")
    .workplane()
    .pushPoints(island_hole_centers)
    .rect(pocket_size_x, pocket_size_y)
    .cutBlind(-island_height)
)

# 7. Island Details: Top Rim/Lip
# Add a thin raised profile on top of the island
rim_base = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness + island_height)
    .rect(island_width, island_length)
    .extrude(island_rim_height)
    .edges("|Z")
    .fillet(island_radius)
)

# Cut the interior of the rim
rim_cut_w = island_width - 2 * island_rim_thick
rim_cut_l = island_length - 2 * island_rim_thick
rim_cut_r = max(island_radius - island_rim_thick, 0.1)

rim_final = (
    rim_base.faces(">Z")
    .workplane()
    .rect(rim_cut_w, rim_cut_l)
    .cutBlind(-island_rim_height)
)

# 8. Island Details: Base Boss (Keying feature)
# Semi-circular protrusion at the base of the island (front side)
boss_radius = 3.5
boss_height = 2.5
boss = (
    floor_plane
    .center(0, -island_length/2)
    .circle(boss_radius)
    .extrude(boss_height)
)

# Union all internal features to the main result
result = result.union(island).union(rim_final).union(boss)

# 9. Final Fillets (Optional cleanup)
# Add a small fillet to the floor of the pocket for a molded look
# Selecting edges at the Z height of the floor
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0, main_length/2 - wall_thickness, floor_thickness))).fillet(0.5)
except:
    pass # Skip if selection is complex

# Export or Display
# show_object(result)