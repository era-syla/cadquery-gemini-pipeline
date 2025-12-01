import cadquery as cq

# Parameters for the curved track geometry
radius = 120.0       # Radius to the center line of the track
track_width = 40.0   # Total width of the track bed
rail_width = 4.0     # Width of the raised side rails
rail_height = 4.0    # Height of rails above the base
base_thickness = 3.0 # Thickness of the track floor
angle = 45.0         # Arc angle of the segment

# Parameters for bottom supports (sleepers)
sleeper_width = 10.0
sleeper_depth = 3.0  # Height below the base
sleeper_len = track_width

# Parameters for end connectors (female dovetail/puzzle style)
conn_neck_w = 10.0
conn_neck_d = 4.0
conn_void_w = 16.0
conn_void_d = 7.0

# 1. Generate Main Track Body
# Define the cross-section profile on the XZ plane
# X axis corresponds to radial distance, Z axis to height
r_inner = radius - track_width / 2.0
r_outer = radius + track_width / 2.0

# Points for the profile (counter-clockwise)
pts = [
    (r_inner, 0),
    (r_inner, base_thickness + rail_height),
    (r_inner + rail_width, base_thickness + rail_height),
    (r_inner + rail_width, base_thickness),
    (r_outer - rail_width, base_thickness),
    (r_outer - rail_width, base_thickness + rail_height),
    (r_outer, base_thickness + rail_height),
    (r_outer, 0),
    (r_inner, 0)
]

# Create profile and revolve it to create the arc
# We revolve by the full angle, then rotate back by half to center it on the Y-axis
track = cq.Workplane("XZ").polyline(pts).close().revolve(angle, (0, 0, 0), (0, 0, 1))
track = track.rotate((0, 0, 0), (0, 0, 1), -angle / 2.0)

# 2. Generate Sleepers (Feet)
# Create a generic sleeper block centered at the origin
sleeper_solid = (cq.Workplane("XY")
                 .box(sleeper_len, sleeper_width, sleeper_depth)
                 .translate((0, 0, -sleeper_depth / 2.0))
                 .translate((radius, 0, 0)))

# Position 3 sleepers: Center, Left, Right
# Calculate angle offset to place side sleepers near the ends
sleeper_offset_deg = angle / 2.0 - 8.0

s_center = sleeper_solid
s_left = sleeper_solid.rotate((0, 0, 0), (0, 0, 1), -sleeper_offset_deg)
s_right = sleeper_solid.rotate((0, 0, 0), (0, 0, 1), sleeper_offset_deg)

# Union sleepers to the track
result = track.union(s_center).union(s_left).union(s_right)

# 3. Create End Connectors (Cutouts)
# Define the cutout shape on the XY plane.
# We create a shape pointing in -Y direction (cutting "inwards" if placed at +Y)
c_pts = [
    (conn_neck_w / 2.0, 0),
    (conn_neck_w / 2.0, -conn_neck_d),
    (conn_void_w / 2.0, -conn_neck_d),
    (conn_void_w / 2.0, -(conn_neck_d + conn_void_d)),
    (-conn_void_w / 2.0, -(conn_neck_d + conn_void_d)),
    (-conn_void_w / 2.0, -conn_neck_d),
    (-conn_neck_w / 2.0, -conn_neck_d),
    (-conn_neck_w / 2.0, 0),
    (conn_neck_w / 2.0, 0)
]

# Extrude cutter tool tall enough to cut through the base
cutter_height = base_thickness + rail_height + 10.0
cutter_neg_y = (cq.Workplane("XY")
                .polyline(c_pts)
                .close()
                .extrude(cutter_height)
                .translate((0, 0, -5)))

# Create the opposite cutter (pointing +Y) for the other end
cutter_pos_y = cutter_neg_y.rotate((0, 0, 0), (0, 0, 1), 180)

# Position Cutters
# Right End (+Angle/2): The end face normal points roughly +Y (tangential).
# To cut into the track, we need the cutter that points "backwards" (-Y relative to local tangent).
# We move the cutter to radius, then rotate by the end angle.
c_right = cutter_neg_y.translate((radius, 0, 0)).rotate((0, 0, 0), (0, 0, 1), angle / 2.0)

# Left End (-Angle/2): The end face normal points roughly -Y.
# We need the cutter pointing "forwards" (+Y relative to local tangent).
c_left = cutter_pos_y.translate((radius, 0, 0)).rotate((0, 0, 0), (0, 0, 1), -angle / 2.0)

# Apply cuts
result = result.cut(c_right).cut(c_left)

# 4. Final Details
# Apply fillets to the top edges of the rails for smoothness
try:
    result = result.faces(">Z").edges().fillet(0.5)
except Exception:
    pass