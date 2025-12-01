import cadquery as cq

# ---------------------------------------------------------
# Dimensions and Geometry Setup
# ---------------------------------------------------------

# Main body dimensions
body_radius = 13.0
body_center = (0, 4, 0)

# Head dimensions
head_radius = 10.0
head_center = (0, -8, 0)

# Bulb dimensions (on the back)
bulb_radius = 11.0
bulb_center = (0, 4, 10)
bulb_tip_height = 8.0

# Leg dimensions
leg_radius = 3.5
leg_length = 10.0
leg_offset_x = 9.0
leg_offset_y_front = -9.0
leg_offset_y_back = 7.0
leg_floor_z = -10.0

# ---------------------------------------------------------
# Part Construction
# ---------------------------------------------------------

# 1. Torso (Body)
# Modeled as a sphere
body = cq.Workplane("XY").center(body_center[0], body_center[1]).workplane(offset=body_center[2]).sphere(body_radius)

# 2. Head
# Modeled as a sphere attached to the front
head = cq.Workplane("XY").center(head_center[0], head_center[1]).workplane(offset=head_center[2]).sphere(head_radius)

# 3. Bulb (Back Plant)
# Modeled as a sphere base with a cone tip
bulb_base = cq.Workplane("XY").center(bulb_center[0], bulb_center[1]).workplane(offset=bulb_center[2]).sphere(bulb_radius)

# The tip of the bulb (onion shape)
bulb_tip = (cq.Workplane("XY")
            .center(bulb_center[0], bulb_center[1])
            .workplane(offset=bulb_center[2] + 6)
            .circle(bulb_radius * 0.75)
            .workplane(offset=bulb_tip_height)
            .circle(0.001)
            .loft())

# 4. Legs
# Modeled as capsules (cylinders with filleted bottoms)
def create_leg(x, y):
    # Create cylinder starting from the ground up into the body
    return (cq.Workplane("XY")
            .center(x, y)
            .workplane(offset=leg_floor_z)
            .circle(leg_radius)
            .extrude(leg_length + 5)
            .edges("<Z").fillet(leg_radius * 0.5))

leg_fl = create_leg(-leg_offset_x, leg_offset_y_front)
leg_fr = create_leg(leg_offset_x, leg_offset_y_front)
leg_bl = create_leg(-leg_offset_x - 1, leg_offset_y_back)
leg_br = create_leg(leg_offset_x + 1, leg_offset_y_back)

# 5. Ears
# Modeled as triangular prisms/cones on top of the head
def create_ear(x_dir):
    # Position relative to head
    ear_x = x_dir * 5.5
    ear_y = head_center[1]
    ear_z = head_center[2] + head_radius * 0.8
    
    # Rotation to angle ears outwards
    rot_z = -30 if x_dir > 0 else 30
    
    return (cq.Workplane("XY")
            .center(ear_x, ear_y)
            .workplane(offset=ear_z)
            .polygon(3, 5.0)
            .extrude(6.0, taper=20)
            .rotate((0, 0, 0), (1, 0, 0), 45)
            .rotate((0, 0, 0), (0, 0, 1), rot_z))

ear_l = create_ear(-1)
ear_r = create_ear(1)

# ---------------------------------------------------------
# Assembly (Union)
# ---------------------------------------------------------

# Combine all positive geometry
result = (body
          .union(head)
          .union(bulb_base)
          .union(bulb_tip)
          .union(leg_fl)
          .union(leg_fr)
          .union(leg_bl)
          .union(leg_br)
          .union(ear_l)
          .union(ear_r)
          )

# ---------------------------------------------------------
# Facial Features (Cuts)
# ---------------------------------------------------------

# Eyes: Triangular cuts
def make_eye_sketch(x_offset):
    # Define triangle points
    pts = [(x_offset - 2.8, 3 + 1.5), (x_offset + 2.8, 3 + 1.5), (x_offset, 3 - 2.5)]
    return (cq.Workplane("XZ")
            .workplane(offset=-25)
            .moveTo(pts[0][0], pts[0][1])
            .lineTo(pts[1][0], pts[1][1])
            .lineTo(pts[2][0], pts[2][1])
            .close()
            .extrude(15))

eye_l_cut = make_eye_sketch(-4.5)
eye_r_cut = make_eye_sketch(4.5)

# Mouth: V-shaped smile cut
mouth_pts = [(-6, -0.5), (0, -4.5), (6, -0.5), (0, -2.5)]
mouth_cut = (cq.Workplane("XZ")
             .workplane(offset=-25)
             .moveTo(mouth_pts[0][0], mouth_pts[0][1])
             .lineTo(mouth_pts[1][0], mouth_pts[1][1])
             .lineTo(mouth_pts[2][0], mouth_pts[2][1])
             .lineTo(mouth_pts[3][0], mouth_pts[3][1])
             .close()
             .extrude(15))

# Apply cuts to the main body
result = result.cut(eye_l_cut).cut(eye_r_cut).cut(mouth_cut)