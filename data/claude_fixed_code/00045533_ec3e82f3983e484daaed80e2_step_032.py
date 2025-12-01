import cadquery as cq

# --- Parameters ---
# Main body dimensions
body_length = 32.0
body_width = 30.0
body_height = 12.0
fillet_radius = 1.5  # Radius for vertical corners

# Mounting flange dimensions
flange_length = 6.0   # Protrusion length
flange_width = 28.0   # Width along the side
flange_thickness = 3.5
# Position flange relative to top face (simulating the lid step)
flange_z_offset = -2.5 

# Cable parameters
relief_length = 4.0
wire_length = 20.0
wire_radius = 0.65
wire_pitch = 1.4

# --- 1. Main Body ---
# Create the main box centered at origin
main_body = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Add countersunk screw holes to the top corners
screw_inset = 2.5
screw_locations = [
    (body_length/2 - screw_inset, body_width/2 - screw_inset),
    (body_length/2 - screw_inset, -body_width/2 + screw_inset),
    (-body_length/2 + screw_inset, body_width/2 - screw_inset),
    (-body_length/2 + screw_inset, -body_width/2 + screw_inset),
]

main_body = (
    main_body.faces(">Z").workplane()
    .pushPoints(screw_locations)
    .cskHole(2.0, 3.5, 90) # diameter, csk_dia, angle
)

# --- 2. Mounting Flanges ---
def create_flange_geometry():
    """Creates a single mounting flange with holes and notch."""
    # Base plate
    flange = cq.Workplane("XY").box(flange_length, flange_width, flange_thickness)
    
    # Mounting holes
    hole_y_offset = flange_width/2 - 4.0
    flange = (
        flange.faces(">Z").workplane()
        .pushPoints([(0, hole_y_offset), (0, -hole_y_offset)])
        .hole(2.4)
    )
    
    # U-shaped notch on the outer edge
    # Center the cut rect on the edge (+X local)
    notch_depth = 2.5
    notch_width = 4.5
    flange = (
        flange.faces(">Z").workplane()
        .center(flange_length/2, 0)
        .rect(notch_depth * 2, notch_width)
        .cutBlind(-flange_thickness)
    )
    return flange

flange_geo = create_flange_geometry()

# Calculate Z position for flanges (offset from top)
# Top of body is at +body_height/2
# We want top of flange to be below that by some amount
top_z = body_height / 2
flange_center_z = top_z + flange_z_offset - (flange_thickness / 2)

# Position Right Flange (+X)
right_flange = (
    flange_geo
    .translate((body_length/2 + flange_length/2 - 0.1, 0, flange_center_z))
)

# Position Left Flange (-X)
left_flange = (
    create_flange_geometry()
    .rotate((0,0,0), (0,0,1), 180)
    .translate((-body_length/2 - flange_length/2 + 0.1, 0, flange_center_z))
)

# --- 3. Cable Exit and Wires ---
# Strain relief block on the left face (-X)
strain_relief = (
    cq.Workplane("YZ")
    .workplane(offset=-body_length/2)
    .center(0, flange_center_z) # Align with flange level
    .rect(5.0, 4.0)
    .extrude(-relief_length) # Extrude outwards (-X direction)
)

# Wires (3-strand flat ribbon)
wires = (
    cq.Workplane("YZ")
    .workplane(offset=-body_length/2 - relief_length)
    .center(0, flange_center_z)
    # Create points for flat ribbon orientation (spread in Y)
    .pushPoints([(0, 0), (wire_pitch, 0), (-wire_pitch, 0)]) 
    .circle(wire_radius)
    .extrude(-wire_length)
)

# --- 4. Assembly ---
result = (
    main_body
    .union(right_flange)
    .union(left_flange)
    .union(strain_relief)
    .union(wires)
)