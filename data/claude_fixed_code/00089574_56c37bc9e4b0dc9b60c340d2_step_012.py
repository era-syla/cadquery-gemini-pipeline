import cadquery as cq

# --- Parameter Definitions ---
# Estimated dimensions based on visual proportions
height = 90.0
width = 50.0
depth = 30.0
wall_thickness = 4.0
plate_thickness = 4.0

# The depth of the 'seat' (rabbet) cut into the side walls for the top/bottom plates
rabbet_depth = 2.0 

# Calculated width of the top/bottom plates to fit into the rabbets
# The plates sit between the walls, but the walls are notched.
# Internal Span = Width - 2*Wall_Thick
# Plate Width = Internal Span + 2*Rabbet_Depth
internal_plate_width = width - 2 * (wall_thickness - rabbet_depth)

# --- Geometry Construction Functions ---

def create_side_wall():
    """
    Creates one side wall with internal rabbets for plates and an external cosmetic groove.
    The wall is created at the origin, intended to be moved later.
    We assume this is the RIGHT wall (Outer face at +X relative to its center).
    """
    # Start with the main block
    wall = cq.Workplane("XY").box(wall_thickness, depth, height)
    
    # Define parameters for the rabbets (notches) on the inside face
    # For the right wall, the inner face is at x = -wall_thickness/2
    rabbet_x = -wall_thickness/2 + rabbet_depth/2
    
    # Top Rabbet (Top Inner Corner)
    top_rabbet_z = height/2 - plate_thickness/2
    top_cut = cq.Workplane("XY").box(rabbet_depth, depth, plate_thickness).val()\
                .translate((rabbet_x, 0, top_rabbet_z))
    
    # Bottom Rabbet (Bottom Inner Corner)
    bot_rabbet_z = -height/2 + plate_thickness/2
    bot_cut = cq.Workplane("XY").box(rabbet_depth, depth, plate_thickness).val()\
                .translate((rabbet_x, 0, bot_rabbet_z))
    
    # Cosmetic Groove on the outer face
    # The image shows a horizontal line on the side face, aligned with the internal plate level.
    groove_size = 0.5
    groove_z_top = height/2 - plate_thickness
    groove_z_bot = -height/2 + plate_thickness
    # Outer face is at x = wall_thickness/2
    groove_x = wall_thickness/2 - groove_size/2
    
    groove_top = cq.Workplane("XY").box(groove_size, depth, groove_size).val()\
                  .translate((groove_x, 0, groove_z_top))
    groove_bot = cq.Workplane("XY").box(groove_size, depth, groove_size).val()\
                  .translate((groove_x, 0, groove_z_bot))

    # Apply cuts to the wall
    wall = wall.cut(top_cut).cut(bot_cut).cut(groove_top).cut(groove_bot)
    return wall

def create_top_plate():
    """ Creates the top plate with two slots. """
    # Basic plate
    plate = cq.Workplane("XY").box(internal_plate_width, depth, plate_thickness)
    
    # Slot dimensions
    slot_len = 16.0
    slot_w = 3.0
    slot_y_offset = 7.0 # Offset from center line
    
    # Cut Slot 1
    plate = plate.faces(">Z").workplane().center(0, slot_y_offset).slot2D(slot_len, slot_w, 0).cutBlind(-plate_thickness)
    
    # Cut Slot 2
    plate = plate.faces(">Z").workplane().center(0, -slot_y_offset).slot2D(slot_len, slot_w, 0).cutBlind(-plate_thickness)
    
    return plate

def create_bottom_plate():
    """ Creates the bottom plate with corner holes. """
    plate = cq.Workplane("XY").box(internal_plate_width, depth, plate_thickness)
    
    # Hole dimensions
    hole_dia = 3.5
    # Distance between hole centers
    w_sep = internal_plate_width - 12.0
    d_sep = depth - 10.0
    
    # Create holes
    plate = plate.faces(">Z").workplane()\
                 .rect(w_sep, d_sep, forConstruction=True)\
                 .vertices().hole(hole_dia)
    return plate

# --- Assembly Construction ---

# 1. Instantiate Right Wall
# Move it to the positive X side
right_wall = create_side_wall().translate((width/2 - wall_thickness/2, 0, 0))

# 2. Instantiate Left Wall
# Rotate the right wall 180 degrees around Z so the notches face inwards (towards +X)
# Then move to negative X side
left_wall = create_side_wall().rotate((0,0,0), (0,0,1), 180).translate((-width/2 + wall_thickness/2, 0, 0))

# 3. Instantiate Top Plate
# Positioned at the top, fitting into the rabbets
top_plate = create_top_plate().translate((0, 0, height/2 - plate_thickness/2))

# 4. Instantiate Bottom Plate
# Positioned at the bottom
bottom_plate = create_bottom_plate().translate((0, 0, -height/2 + plate_thickness/2))

# --- Final Union ---
result = right_wall.union(left_wall).union(top_plate).union(bottom_plate)