import cadquery as cq

# 1. Define Dimensions
length = 60.0
width = 40.0
height = 50.0

# Feature dimensions
left_wall_thickness = 10.0
slot_width = 15.0
right_block_width = length - left_wall_thickness - slot_width

# The slot has a stepped depth (shelf inside)
shelf_height = 20.0        # Height of the shelf from the bottom
upper_slot_depth = 25.0    # Deeper cut for the top section
lower_slot_depth = 15.0    # Shallower cut for the bottom section

# Hole dimensions
hole_diameter = 12.0
hole_height_from_bottom = 15.0

# 2. Create Base Block
# Centered at (0,0,0) helps with symmetry, but we will calculate offsets manually
result = cq.Workplane("XY").box(length, width, height)

# 3. Calculate Coordinates for Features relative to the Front Face center
# Global bounds: X[-30, 30], Y[-20, 20], Z[-25, 25]
# Front face center is roughly at (0, 0) in the Workplane's local (X, Z) coords

# Slot X position
# Left wall ends at x = -30 + 10 = -20. Slot spans -20 to -5.
# Slot center x = -12.5
slot_center_x = -length/2 + left_wall_thickness + slot_width/2

# Upper Slot (Deep cut) Geometry
# Spans from shelf (z=-5) to top (z=25). Height = 30. Center Z = 10.
upper_slot_height = height - shelf_height
upper_slot_center_z = height/2 - upper_slot_height/2

# Lower Slot (Shallow cut) Geometry
# Spans from bottom (z=-25) to shelf (z=-5). Height = 20. Center Z = -15.
lower_slot_height = shelf_height
lower_slot_center_z = -height/2 + lower_slot_height/2

# Hole Position
# Centered on the right block (x = -5 to 30). Width 35. Center X = 12.5.
hole_center_x = -length/2 + left_wall_thickness + slot_width + right_block_width/2
hole_center_z = -height/2 + hole_height_from_bottom

# 4. Apply Cuts
result = (
    result
    .faces("<Y").workplane()  # Select the front face
    
    # Cut the upper, deeper part of the slot
    .center(slot_center_x, upper_slot_center_z)
    .rect(slot_width, upper_slot_height)
    .cutBlind(upper_slot_depth)
)

# Cut the lower, shallower part of the slot (creates the step)
result = (
    result
    .faces("<Y").workplane()
    .center(slot_center_x, lower_slot_center_z)
    .rect(slot_width, lower_slot_height)
    .cutBlind(lower_slot_depth)
)

# Cut the circular hole
result = (
    result
    .faces("<Y").workplane()
    .center(hole_center_x, hole_center_z)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# For visualization in CQ-editor or similar tools
# show_object(result)