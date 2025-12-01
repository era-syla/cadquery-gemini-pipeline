import cadquery as cq

# --- Dimensions ---
ring_od = 15.0
ring_id = 9.0
ring_thickness = 2.0

neck_radius = 2.5
neck_height = 2.0

block_width = 16.0
block_depth = 8.0
block_height = 6.0
block_fillet = 1.5

stem_radius = 3.5
stem_height = 10.0

ball_radius = 6.5

# Tapered Upper Section
taper_bottom_radius = 3.5
taper_top_radius = 5.5
taper_height = 20.0

# Top Cap
cap_radius = 14.0
cap_height = 5.0
cap_fillet_top = 2.0
cap_fillet_bot = 1.0

# Rib features
rib_thickness = 2.0
rib_offset = 1.0  # Extra protrusion from the main bodies

# --- Z-Level Calculations ---
z_0 = 0
z_ring_top = z_0 + ring_thickness
z_neck_top = z_ring_top + neck_height
z_block_top = z_neck_top + block_height
z_stem_top = z_block_top + stem_height
z_ball_center = z_stem_top + 2.0  # Ball center slightly above stem end
z_taper_start = z_ball_center + 3.0  # Start taper inside the ball
z_taper_end = z_taper_start + taper_height
z_cap_bot = z_taper_end
z_cap_top = z_cap_bot + cap_height

# --- Construction ---

# 1. Base Ring
result = (
    cq.Workplane("XY")
    .circle(ring_od / 2.0)
    .circle(ring_id / 2.0)
    .extrude(ring_thickness)
)

# 2. Neck Connector
neck = (
    cq.Workplane("XY")
    .workplane(offset=z_ring_top)
    .circle(neck_radius)
    .extrude(neck_height)
)
result = result.union(neck)

# 3. Rectangular Block
block = (
    cq.Workplane("XY")
    .workplane(offset=z_neck_top)
    .box(block_width, block_depth, block_height, centered=(True, True, False))
)
block = block.edges("|Z").fillet(block_fillet)
result = result.union(block)

# 4. Lower Cylindrical Stem
stem = (
    cq.Workplane("XY")
    .workplane(offset=z_block_top)
    .circle(stem_radius)
    .extrude(stem_height)
)
result = result.union(stem)

# 5. Central Ball Joint
ball = (
    cq.Workplane("XY")
    .workplane(offset=z_ball_center)
    .sphere(ball_radius)
)
result = result.union(ball)

# 6. Upper Tapered Stem (Loft)
taper = (
    cq.Workplane("XY")
    .workplane(offset=z_taper_start)
    .circle(taper_bottom_radius)
    .workplane(offset=taper_height)
    .circle(taper_top_radius)
    .loft()
)
result = result.union(taper)

# 7. Top Cap
cap = (
    cq.Workplane("XY")
    .workplane(offset=z_cap_bot)
    .circle(cap_radius)
    .extrude(cap_height)
)
cap = cap.faces(">Z").edges().fillet(cap_fillet_top)
cap = cap.faces("<Z").edges().fillet(cap_fillet_bot)

# Add the split line groove on the top cap
split_cut = (
    cq.Workplane("XY")
    .workplane(offset=z_cap_top)
    .rect(cap_radius * 2.2, 0.8)
    .extrude(-1.0)
)
cap = cap.cut(split_cut)
result = result.union(cap)

# 8. Vertical Ribs
# Create a profile on the XZ plane that outlines the shape and extrude it
# Points define the right half of the profile
rib_pts = [
    (0, z_block_top),
    (stem_radius + rib_offset, z_block_top),
    (stem_radius + rib_offset, z_ball_center - ball_radius + 1.5),
    (ball_radius + rib_offset, z_ball_center),
    (taper_bottom_radius + rib_offset, z_ball_center + ball_radius - 1.5),
    (taper_top_radius + rib_offset, z_cap_bot),
    (0, z_cap_bot)
]

# Mirror points to form a closed shape
rib_pts_left = [(-x, z) for x, z in rib_pts[::-1]]
full_rib_profile = rib_pts + rib_pts_left

rib = (
    cq.Workplane("XZ")
    .polyline(full_rib_profile)
    .close()
    .extrude(rib_thickness / 2.0, both=True)
)

result = result.union(rib)