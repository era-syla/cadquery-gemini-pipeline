import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_w = 5.2        # Width (along the side with leads)
body_l = 5.0        # Length (depth)
body_h = 1.8        # Housing height
corner_r = 0.2      # Corner fillet radius

# Knob/Rotor dimensions
knob_dia = 2.8
knob_h = 1.0        # Height of knob above body
knob_recess_gap = 0.15

# Lead dimensions
lead_count = 3      # Number of leads per side
lead_pitch = 1.5    # Distance between lead centers
lead_width = 0.6
lead_thick = 0.15
lead_length = 1.2   # Total extension from body wall
foot_length = 0.6   # Length of the flat foot pad
standoff = 0.2      # Clearance between body bottom and mounting plane
exit_h = 0.7        # Height at which leads exit the body (from bottom of body)

# Calculated positions
body_elev = standoff  # Z height of body bottom
lead_z_center = body_elev + exit_h

# --- 1. Main Housing Body ---
# Create the base box
body = (cq.Workplane("XY")
        .workplane(offset=body_elev)
        .box(body_w, body_l, body_h, centered=(True, True, False))
        )

# Apply fillets to vertical corners
body = body.edges("|Z").fillet(corner_r)

# Apply small chamfer to top edges for molded look
body = body.faces(">Z").edges().chamfer(0.15)

# Create side molding recesses (rectangular indents on the non-lead sides)
recess_w = body_l * 0.5
recess_h = body_h * 0.4

# Create a shell to limit the recess depth
recess_cut_tool = (cq.Workplane("YZ")
                   .workplane(offset=body_w/2 - 0.2) # Shallow cut depth
                   .rect(recess_w, recess_h)
                   .extrude(1.0) # Cut outward
                   )
# Cut right side
body = body.cut(recess_cut_tool)
# Cut left side (mirror)
body = body.cut(recess_cut_tool.mirror("YZ"))


# --- 2. Rotor/Knob ---
# Create the cylindrical knob
knob = (cq.Workplane("XY")
        .workplane(offset=body_elev + body_h)
        .circle(knob_dia / 2.0)
        .extrude(knob_h)
        )
# Chamfer/Fillet knob top
knob = knob.faces(">Z").edges().fillet(0.1)

# Cut a circular clearance gap in the main body around the knob
knob_hole = (cq.Workplane("XY")
             .workplane(offset=body_elev + body_h - 0.2)
             .circle((knob_dia / 2.0) + knob_recess_gap)
             .extrude(0.3)
             )
body = body.cut(knob_hole)

# Union the knob to the body
body = body.union(knob)


# --- 3. Leads (Gull-wing style) ---
def create_lead_profile(is_front=True):
    """Generates a generic gull-wing lead solid."""
    sign = -1 if is_front else 1
    
    # Y coordinates relative to center
    y_wall = sign * body_l / 2.0
    y_knee = y_wall + (sign * 0.4)
    y_toe = y_wall + (sign * lead_length)
    
    # Z coordinates
    z_exit_top = lead_z_center + lead_thick/2.0
    z_exit_bot = lead_z_center - lead_thick/2.0
    z_foot_top = lead_thick
    z_foot_bot = 0.0
    
    # Inner anchor point
    y_inner = y_wall - (sign * 0.5)
    
    # Define points for the side profile polygon
    pts = [
        (y_inner, z_exit_top),        # Top Inner
        (y_knee, z_exit_top),         # Top Knee (bend start)
        (y_knee + sign*0.3, z_foot_top), # Top Foot start (bend end)
        (y_toe, z_foot_top),          # Top Toe
        (y_toe, z_foot_bot),          # Bottom Toe
        (y_knee + sign*0.2, z_foot_bot), # Bottom Foot start
        (y_knee - sign*0.1, z_exit_bot), # Bottom Knee
        (y_inner, z_exit_bot)         # Bottom Inner
    ]
    
    # Create wire and extrude
    # Drawn in YZ plane, extruded along X (centered)
    prof = cq.Workplane("YZ").polyline(pts).close()
    lead = prof.extrude(lead_width, both=True)
    return lead

# Generate and place leads
leads_union = None

# Calculate offsets for 3 leads
x_offsets = [ (i - (lead_count-1)/2) * lead_pitch for i in range(lead_count) ]

for x in x_offsets:
    # Front Lead
    l_front = create_lead_profile(is_front=True).translate((x, 0, 0))
    # Back Lead
    l_back = create_lead_profile(is_front=False).translate((x, 0, 0))
    
    if leads_union is None:
        leads_union = l_front.union(l_back)
    else:
        leads_union = leads_union.union(l_front).union(l_back)

    # Optional: Cut small slots in body where leads exit
    slot_tool = (cq.Workplane("XY")
                 .workplane(offset=lead_z_center)
                 .box(lead_width + 0.1, 2.0, lead_thick + 0.1, centered=(True, True, True))
                 )
    # Cut front slot
    body = body.cut(slot_tool.translate((x, -body_l/2, 0)))
    # Cut back slot
    body = body.cut(slot_tool.translate((x, body_l/2, 0)))

# --- 4. Final Result ---
result = body.union(leads_union)