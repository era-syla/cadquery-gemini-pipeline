import cadquery as cq

# Parameters defining the geometry
length = 200.0              # Total length of the extrusion
total_width = 60.0          # Overall width of the assembly
rail_width = 2.0            # Thickness of the side vertical rails
rail_height = 10.0          # Total height of the side rails
rail_top_offset = 2.5       # How much the rail extends above the flange surface

trough_inner_width = 32.0   # Width of the inner curve at the top
trough_straight_depth = 6.0 # Depth of the vertical wall part of the trough before the curve
wall_thickness = 2.0        # Thickness of the sheet material

# Derived calculations for profile points
# We assume the top surface of the horizontal flanges is at Y=0 (local sketch coordinates)
flange_y_top = 0.0
flange_y_bottom = -wall_thickness

# Radii for the trough bottom
inner_radius = trough_inner_width / 2.0
outer_radius = inner_radius + wall_thickness

# X coordinates relative to center
x_rail_inner = (total_width / 2.0) - rail_width
x_channel_inner = trough_inner_width / 2.0
x_channel_outer = x_channel_inner + wall_thickness

# Y coordinates
y_rail_top = rail_top_offset
y_rail_bottom = rail_top_offset - rail_height
# The center of the circular bottom section is aligned with the end of the straight vertical section
y_arc_center = flange_y_bottom - trough_straight_depth

# Create the main central profile (U-channel with flanges)
# Drawing on "front" plane (XZ), so Y in code maps to global Z (height)
# The extrusion will be along global Y (length)
main_profile_sketch = (
    cq.Workplane("front")
    .moveTo(-x_rail_inner, flange_y_top)  # Start at top-left of left flange
    .lineTo(-x_channel_inner, flange_y_top)  # Left flange horizontal
    .lineTo(-x_channel_inner, y_arc_center)  # Left vertical wall down
    
    # Inner arc (semi-circle)
    # Using threePointArc: start, mid, end
    .threePointArc(
        (0, y_arc_center - inner_radius),    # Bottom-most point of inner arc
        (x_channel_inner, y_arc_center)      # End of inner arc
    )
    
    .lineTo(x_channel_inner, flange_y_top)   # Right vertical wall up
    .lineTo(x_rail_inner, flange_y_top)      # Right flange horizontal
    .lineTo(x_rail_inner, flange_y_bottom)   # Right flange thickness down
    .lineTo(x_channel_outer, flange_y_bottom)# Right outer wall start
    .lineTo(x_channel_outer, y_arc_center)   # Right outer wall straight down
    
    # Outer arc
    .threePointArc(
        (0, y_arc_center - outer_radius),    # Bottom-most point of outer arc
        (-x_channel_outer, y_arc_center)     # End of outer arc
    )
    
    .lineTo(-x_channel_outer, flange_y_bottom) # Left outer wall straight up
    .lineTo(-x_rail_inner, flange_y_bottom)    # Left flange thickness return
    .close()
)

# Extrude the main profile
main_body = main_profile_sketch.extrude(length)

# Create the side rails (rectangular profiles)
# Left Rail
left_rail = (
    cq.Workplane("front")
    .center(-x_rail_inner - (rail_width / 2.0), y_rail_top - (rail_height / 2.0))
    .rect(rail_width, rail_height)
    .extrude(length)
)

# Right Rail
right_rail = (
    cq.Workplane("front")
    .center(x_rail_inner + (rail_width / 2.0), y_rail_top - (rail_height / 2.0))
    .rect(rail_width, rail_height)
    .extrude(length)
)

# Combine all parts into the final object
result = main_body.union(left_rail).union(right_rail)