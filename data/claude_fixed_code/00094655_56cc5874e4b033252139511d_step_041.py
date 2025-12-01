import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
main_length = 50.0
main_width = 24.0
main_height = 20.0
wall_thickness = 4.0
channel_depth = 15.0

# Top pocket dimensions
pocket_length = 38.0
pocket_width = 14.0
pocket_depth = 2.0

# Clamp dimensions
clamp_length = 15.0
clamp_protrusion = 12.0
clamp_height = 16.0
clamp_hole_dia = 8.0
clamp_hole_offset_x = 2.0 # Offset from the end of the main body

# --- Construction ---

# 1. Create the Main Body Block
result = cq.Workplane("XY").box(main_length, main_width, main_height)

# 2. Cut the Bottom Channel (Inverted U-Profile)
# The channel runs along the length (X-axis) on the bottom face
channel_width = main_width - (2 * wall_thickness)
result = result.faces("<Z").workplane().rect(main_length, channel_width).cutBlind(-channel_depth)

# 3. Cut the Top Recess/Pocket
result = result.faces(">Z").workplane().rect(pocket_length, pocket_width).cutBlind(-pocket_depth)

# 4. Drill Mounting Holes
# Top holes inside the pocket
hole_spacing = pocket_length - 12
result = result.faces(">Z").workplane().pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)]).hole(3.2)

# Side holes on the main body (visible in the right image view)
# Located on the +Y face (opposite to clamp)
side_hole_spacing = main_length - 15
result = result.faces(">Y").workplane().center(0, -main_height/4).pushPoints([(-side_hole_spacing/2, 0), (side_hole_spacing/2, 0)]).hole(3.2)

# 5. Create the Clamp Assembly
# Calculate position: Attached to -Y face, near the -X end
clamp_center_x = -main_length/2 + clamp_length/2 + clamp_hole_offset_x
clamp_center_y = -main_width/2 - clamp_protrusion/2
clamp_center_z = -main_height/2 + clamp_height/2

# Generate the basic clamp block
clamp = cq.Workplane("XY").box(clamp_length, clamp_protrusion, clamp_height).translate((clamp_center_x, clamp_center_y, clamp_center_z))

# Cut the main rod hole (Horizontal along X)
clamp = clamp.faces(">X").workplane().center(0, 0).hole(clamp_hole_dia)

# Cut the tightening slit
# Vertical slit from the outer face inwards, or horizontal cut. 
# Visuals suggest a side cut making a 'C' profile.
clamp = clamp.faces("<Y").workplane().rect(clamp_length, 2.0).cutBlind(-clamp_protrusion/2 - 1)

# Drill Clamp Screw Hole (Vertical with Counterbore)
# Positioned to cross the slit for tightening
clamp = clamp.faces(">Z").workplane().center(0, -2).cboreHole(3.0, 6.0, 3.0)

# 6. Join Clamp to Main Body
result = result.union(clamp)

# 7. Add Fillets/Ribs for Structural Support
# Fillet the vertical intersection between clamp and main body to create the web/rib structure
# We select edges near the intersection point
result = result.edges("|Z").fillet(0.5)