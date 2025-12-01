import cadquery as cq

# --- Parameter Definitions ---
# Main plate dimensions
plate_width = 90.0
plate_depth = 60.0
thickness = 3.0
fillet_radius = 6.0

# Wing/Tab dimensions
tab_width = 22.0
tab_length = 35.0
# Step down is the vertical drop from the top face of the main plate to the top face of the tabs
step_down_height = 12.0 

# Feature dimensions
center_hole_dia = 10.0
slot_width = 5.0
rear_slot_length = 45.0
front_slot_length = 22.0
front_slot_x_offset = 22.0
tab_hole_dia = 5.0

# --- Geometry Construction ---

# 1. Create the Main Plate
# Centered at origin, top face at Z = thickness/2
result = cq.Workplane("XY").box(plate_width, plate_depth, thickness)

# Fillet the front corners (assuming front is in -Y direction)
result = result.edges("|Z and <Y").fillet(fillet_radius)

# 2. Create Side Wings (Vertical Leg + Horizontal Tab)
# Function to create a wing geometry on one side
def make_wing(x_offset):
    # Vertical Leg Section (The drop)
    # Leg height matches the step down distance
    leg_h = step_down_height
    leg = cq.Workplane("XY").box(tab_width, thickness, leg_h).translate((
        x_offset, 
        plate_depth/2 + thickness/2, 
        thickness/2 - leg_h/2
    ))
    
    # Horizontal Tab Section
    tab = cq.Workplane("XY").box(tab_width, tab_length, thickness).translate((
        x_offset, 
        plate_depth/2 + thickness + tab_length/2, 
        -step_down_height
    ))
    
    # Fillet the rear corners of the tab
    # Select vertical edges at the far back (+Y)
    tab = tab.edges("|Z and >Y").fillet(fillet_radius)
    
    return leg.union(tab)

# Generate left and right wings
x_off = (plate_width / 2) - (tab_width / 2)
left_wing = make_wing(-x_off)
right_wing = make_wing(x_off)

# Union wings to the main plate
result = result.union(left_wing).union(right_wing)

# 3. Create Cutouts (Holes and Slots)

# Center Hole
result = result.faces(">Z").workplane().circle(center_hole_dia / 2).cutThruAll()

# Rear Slot (Single long slot behind center hole)
# Positioned at positive Y relative to center
result = result.faces(">Z").workplane().center(0, 16).slot2D(rear_slot_length, slot_width).cutThruAll()

# Front Slots (Two parallel slots in front of center hole)
# Positioned at negative Y, offset in X
result = result.faces(">Z").workplane() \
    .pushPoints([(-front_slot_x_offset, -16), (front_slot_x_offset, -16)]) \
    .slot2D(front_slot_length, slot_width).cutThruAll()

# 4. Tab Holes
# Define positions for holes on the tabs
# Y start of tab is at plate_depth/2 + thickness
tab_start_y = plate_depth/2 + thickness
hole_positions = []

# Add two holes per tab
for x in [-x_off, x_off]:
    hole_positions.append((x, tab_start_y + 8))
    hole_positions.append((x, tab_start_y + 24))

# Create a workplane offset above the tabs to cut downwards
# Tab top Z is roughly -9mm, so Z=0 (XY plane) is sufficient to cut down
result = cq.Workplane("XY").pushPoints(hole_positions).circle(tab_hole_dia / 2).cutThruAll().union(result)