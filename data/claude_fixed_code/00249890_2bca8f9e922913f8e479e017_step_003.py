import cadquery as cq

# --- Dimensions & Parameters ---
width = 80.0
depth = 80.0
base_height = 40.0
lid_height = 15.0
fillet_radius = 6.0
wall_thickness = 3.0
chamfer_size = 0.5  # For the seam between base and lid

# Lug parameters
lug_width = 16.0
lug_extension = 12.0
lug_hole_diam = 6.0
lug_cbore_diam = 11.0
lug_cbore_depth = 5.0

# --- Helper Functions ---

def rounded_rect_block(w, d, h, r):
    return (cq.Workplane("XY")
            .box(w, d, h)
            .edges("|Z")
            .fillet(r))

# --- Base Construction ---
# Create the main block
base_solid = rounded_rect_block(width, depth, base_height, fillet_radius)

# Shell the base (open top)
base = base_solid.faces(">Z").shell(-wall_thickness)

# Add chamfer to the top edge to create a visible seam line
base = base.faces(">Z").edges().chamfer(chamfer_size)

# Create Mounting Lugs
def create_lug():
    # Defines a lug pointing along +X
    # Center of lug cylinder
    cx = width/2.0 + lug_extension
    
    # 2D Profile
    lug_profile = (cq.Workplane("XY")
                   .center(cx, 0)
                   .circle(lug_width/2.0)
                   .center(-lug_extension/2.0 - 1, 0)
                   .rect(lug_extension + 2, lug_width)
                  )
    
    # Extrude
    lug = lug_profile.extrude(lug_width)
    
    # Add hole and counterbore
    lug = (lug.faces(">Z").workplane()
           .center(cx, 0)
           .cboreHole(lug_hole_diam, lug_cbore_diam, lug_cbore_depth)
          )
    
    # Fillet vertical edges of the lug
    lug = lug.edges("|Z").fillet(2.0)
    
    return lug

# Lug 1: X+
l1 = create_lug().translate((0, 0, -lug_width/2))
# Lug 2: Y-
l2 = create_lug().rotate((0,0,0), (0,0,1), -90).translate((0, 0, -lug_width/2))

# Add Lugs to Base
base = base.union(l1).union(l2)

# Add Corner Feet
feet = (cq.Workplane("XY")
        .rect(width - fillet_radius*2, depth - fillet_radius*2, forConstruction=True)
        .vertices()
        .circle(5)
        .extrude(4)
        .translate((0, 0, -base_height/2.0 - 2))
       )
base = base.union(feet)


# --- Lid Construction ---
lid_start_z = base_height/2.0
lid_solid = rounded_rect_block(width, depth, lid_height, fillet_radius)
lid_solid = lid_solid.translate((0, 0, lid_start_z + lid_height/2.0))

# Shell the lid (open bottom)
lid = lid_solid.faces("<Z").shell(-wall_thickness)

# Chamfer bottom edge for seam
lid = lid.faces("<Z").edges().chamfer(chamfer_size)

# -- Lid Top Details --
top_z = lid_start_z + lid_height

# Grooves on top
groove_depth = 1.0
lid = (lid.faces(">Z").workplane()
       .center(0, depth/6.0).rect(width+10, 2).cutBlind(-groove_depth)
       .center(0, -depth/3.0).rect(width+10, 2).cutBlind(-groove_depth)
      )

# Hinge Bar on Left Edge (-X)
bar_offset_x = -width/2.0 + 4
bar_height = 5
num_supports = 4

# Supports
hinge_supports = (cq.Workplane("XY")
                  .rarray(1, depth/4.0, 1, num_supports)
                  .rect(4, 4)
                  .extrude(bar_height)
                  .translate((bar_offset_x, 0, top_z))
                 )

# The Bar
hinge_rod = (cq.Workplane("YZ")
             .circle(1.5)
             .extrude(depth)
             .translate((bar_offset_x, -depth/2.0, top_z + bar_height - 1.5))
            )

# Front Clips (-Y edge)
clips_front = (cq.Workplane("XY")
               .rarray(width/5.0, 1, 4, 1)
               .rect(4, 4)
               .extrude(5)
               .translate((0, -depth/2.0 + 3, top_z))
              )

# Right edge clips (+X)
clips_right = (cq.Workplane("XY")
               .rarray(1, depth/5.0, 1, 4)
               .rect(4, 4)
               .extrude(5)
               .translate((width/2.0 - 3, 0, top_z))
              )

# Back edge clips (+Y)
clips_back = (cq.Workplane("XY")
               .rarray(width/5.0, 1, 4, 1)
               .rect(4, 4)
               .extrude(5)
               .translate((0, depth/2.0 - 3, top_z))
              )

lid = lid.union(hinge_supports).union(hinge_rod).union(clips_front).union(clips_right).union(clips_back)

# --- Final Assembly ---
result = base.union(lid)