import cadquery as cq

# Parameters for dimensions
body_width = 13.0
body_height = 13.0
body_depth = 10.0
fillet_radius = 0.8

# Bushing parameters
nut_circum_diameter = 10.0
nut_thickness = 2.0
shaft_diameter = 6.0
shaft_length = 7.0

# Lever parameters
lever_length = 10.0
lever_base_diam = 3.0
lever_tip_diam = 2.5
ball_diam = 4.0

# Terminal parameters
term_width = 2.0
term_height = 4.0
term_thickness = 0.5
term_hole_diam = 1.0
term_spacing = 3.0
num_terminals = 4

# 1. Main Body
# Create the main rectangular body, centered at origin
# We align it such that Front is -Y, Top is +Z
result = cq.Workplane("XY").box(body_width, body_depth, body_height)

# Apply fillets to vertical edges for a molded look
result = result.edges("|Z").fillet(fillet_radius)

# 2. Bushing Assembly (Front Face / -Y)
# We build sequentially outward from the front face

# Create Hex Nut
# Select the front face (minimum Y)
result = (
    result.faces("<Y").workplane()
    .polygon(6, nut_circum_diameter)
    .extrude(nut_thickness)
)

# Create Threaded Shaft Cylinder
# Select the new front face (face of the nut)
result = (
    result.faces("<Y").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Toggle Lever (Bat Handle)
# Create a tapered loft from the end of the shaft
# Start with a workplane on the end of the shaft
# Define the base circle, then offset for the tip circle
result = (
    result.faces("<Y").workplane()
    .circle(lever_base_diam / 2.0)
    .workplane(offset=lever_length)
    .circle(lever_tip_diam / 2.0)
    .loft(combine=True)
)

# Add the Ball tip
ball_center_offset = -body_depth/2.0 - nut_thickness - shaft_length - lever_length
result = result.union(
    cq.Workplane("XY")
    .sphere(ball_diam / 2.0)
    .translate((0, ball_center_offset, 0))
)

# 4. Terminals (Top Face / +Z)
# Create a separate object for terminals and union it
# Define the shape of a single terminal
def make_terminal():
    # Sketch on XZ plane (Width x Height), extrude thickness (Y)
    # Origin centered at the bottom width-wise
    w = term_width
    h = term_height
    th = term_thickness
    
    # Define profile with rounded top
    term = (
        cq.Workplane("XZ")
        .moveTo(-w/2, 0)
        .lineTo(w/2, 0)
        .lineTo(w/2, h - w/2)
        .radiusArc((-w/2, h - w/2), w/2)
        .lineTo(-w/2, 0)
        .close()
        .extrude(th)
    )
    
    # Cut hole near top
    hole_z = h - w/2
    term = (
        term.faces(">Y").workplane()
        .center(0, hole_z)
        .circle(term_hole_diam / 2.0)
        .cutThruAll()
    )
    return term

# Create one terminal instance
single_terminal = make_terminal()

# Position parameters
# Top face is at Z = body_height / 2
# Back edge is at Y = body_depth / 2
# Place terminals near the back edge
t_y_pos = body_depth / 2.0 - 1.5 
t_z_pos = body_height / 2.0

# Calculate X offsets to center the group of terminals
total_span = (num_terminals - 1) * term_spacing
start_x = -total_span / 2.0

# Union terminals into the result
for i in range(num_terminals):
    x_pos = start_x + (i * term_spacing)
    
    # Translate the terminal to the correct position on top of the body
    # The terminal base is at Z=0 in its local space, so moving to t_z_pos places it on top
    t_instance = single_terminal.translate((x_pos, t_y_pos, t_z_pos))
    
    result = result.union(t_instance)

# Final Result
# The 'result' variable contains the complete toggle switch model