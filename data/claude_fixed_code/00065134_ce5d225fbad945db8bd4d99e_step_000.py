import cadquery as cq

# Parameters for the enclosure
width = 200.0
height = 250.0
depth = 120.0
wall_thickness = 3.0
fillet_radius = 6.0

# 1. Main Box Body
# Create the base block centered on origin
base = (
    cq.Workplane("XY")
    .box(width, height, depth)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Create the internal cavity by shelling the front face (+Z)
# The box goes from Z = -depth/2 to +depth/2
box_shell = base.faces("+Z").shell(-wall_thickness)

# 2. Front Rim / Flange
# Create a thickened rim around the opening for rigidity and sealing
rim_width = 8.0
rim_height = 8.0
rim = (
    cq.Workplane("XY")
    .workplane(offset=depth/2) # Start at the front face
    .rect(width, height)
    .extrude(rim_height)
)

rim_cutout = (
    cq.Workplane("XY")
    .workplane(offset=depth/2)
    .rect(width - 2*rim_width, height - 2*rim_width)
    .extrude(rim_height)
)

rim = rim.cut(rim_cutout).edges("|Z").fillet(fillet_radius)

# 3. Internal Mounting Rail
# Horizontal strap inside the box
rail_height = 25.0
rail_thickness = 2.0
rail_z_pos = depth/2 - 25.0 # Set back from the opening

rail = (
    cq.Workplane("XY")
    .workplane(offset=rail_z_pos)
    .rect(width - wall_thickness + 1.0, rail_height) # Slightly wider to penetrate walls
    .extrude(rail_thickness)
)

# 4. Central Latch Mechanism
# Block located on the center of the rail
latch_w, latch_h = 25.0, 35.0
latch = (
    cq.Workplane("XY")
    .workplane(offset=rail_z_pos + rail_thickness)
    .rect(latch_w, latch_h)
    .extrude(15.0)
)

# Add a keyhole detail to the latch
latch = (
    latch.faces(">Z").workplane()
    .rect(5, 10)
    .cutBlind(-10)
)

# 5. Hinges (Right Side)
# Located on the +X face
hinge_centers_y = [height/4, -height/4]
hinge_block_depth = 12.0
hinge_knuckle_rad = 4.0

hinges = None

for y in hinge_centers_y:
    # Base block attached to the side wall
    # Using local coordinates relative to the side face
    blk = (
        cq.Workplane("YZ")
        .workplane(offset=width/2) # Move to right face
        .center(depth/2 - 15, y)   # Position: near front edge, at specific height
        .rect(15, 25)
        .extrude(10) # Stick out from the side
    )
    
    # Cylindrical Knuckle
    knuckle = (
        cq.Workplane("XY")
        .workplane(offset=depth/2 - 15 - 12.5) # Align Z with block bottom
        .center(width/2 + 10, y) # Position outside the block
        .circle(hinge_knuckle_rad)
        .extrude(25) # Vertical cylinder
    )
    
    if hinges is None:
        hinges = blk.union(knuckle)
    else:
        hinges = hinges.union(blk).union(knuckle)

# 6. Internal Mounting Bosses
# Cylinders in the back corners for mounting a backplate
boss_dx = width/2 - 20
boss_dy = height/2 - 20
boss_pts = [
    (boss_dx, boss_dy), (boss_dx, -boss_dy),
    (-boss_dx, boss_dy), (-boss_dx, -boss_dy)
]

# Create bosses
bosses = (
    cq.Workplane("XY")
    .workplane(offset=-depth/2 + wall_thickness) # Inside back face
    .pushPoints(boss_pts)
    .circle(6.0)
    .extrude(10.0)
)

# Create holes for bosses
boss_holes = (
    cq.Workplane("XY")
    .workplane(offset=-depth/2 + wall_thickness)
    .pushPoints(boss_pts)
    .circle(3.0)
    .extrude(10.0)
)

bosses = bosses.cut(boss_holes)

# 7. Combine all parts into final result
result = (
    box_shell
    .union(rim)
    .union(rail)
    .union(latch)
    .union(hinges)
    .union(bosses)
)