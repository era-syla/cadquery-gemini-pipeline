import cadquery as cq

# --- Parameter Definitions ---
# Main plate dimensions
plate_width = 75.0
plate_height = 55.0
plate_thickness = 6.0

# Motor parameters (NEMA 17 style footprint)
motor_center_x = 24.0
motor_center_y = 26.0
motor_bore_dia = 22.5
motor_mount_pitch = 31.0
motor_screw_dia = 3.5

# Linear bearing holder parameters
bearing_center_x = 58.0
bearing_center_y = 21.0
bearing_bore_dia = 15.2
cylinder_od = 24.0
cylinder_len = 32.0  # Length extending from the plate face
collar_od = 27.0
collar_len = 5.0
notch_dia = 3.0

# Gusset parameters
gusset_thickness = 4.0

# Top mounting features
slot_pos = (12.0, 44.0)
slot_size = (3.0, 8.0)
small_hole_dia = 2.5
large_hole_dia = 4.0

# --- Construction ---

# 1. Base Plate
# Create the main rectangular volume aligned with positive XY quadrant
# centered=(False, False, False) places the origin at the bottom-left corner of the back face
base = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness, centered=(False, False, False))

# Apply Corner Fillets and Chamfers based on visual geometry
base = base.edges("|Z").fillet(5.0)

# 2. Cylinder Extension
# Create a workplane on the front face of the plate
face_wp = base.faces(">Z").workplane()

# Calculate center relative to the face centroid
# Face center is (plate_width/2, plate_height/2)
dx = bearing_center_x - plate_width/2
dy = bearing_center_y - plate_height/2

# Extrude the main cylinder body
cylinder = face_wp.center(dx, dy).circle(cylinder_od/2).extrude(cylinder_len)

# Extrude the collar at the end of the cylinder
collar = cylinder.faces(">Z").workplane().circle(collar_od/2).extrude(collar_len)

result = collar

# 3. Gusset Rib
# Create a rib connecting the top of the plate to the cylinder
# Use a workplane parallel to YZ, offset to the cylinder's X position (bearing_center_x)
gusset_wp = cq.Workplane("YZ").workplane(offset=bearing_center_x)

# Define triangular profile points in local coordinates (Local X=Global Y, Local Y=Global Z)
y_cyl_top = bearing_center_y + cylinder_od/2
z_plate_front = plate_thickness
z_gusset_end = plate_thickness + cylinder_len - 5.0
y_gusset_top = plate_height - 5.0

p1 = (y_cyl_top, z_plate_front)      # Point at cylinder/plate junction
p2 = (y_gusset_top, z_plate_front)   # Point high on the plate
p3 = (y_cyl_top, z_gusset_end)       # Point further out on the cylinder

# Draw triangle and extrude symmetrically
gusset = gusset_wp.moveTo(*p1).lineTo(*p2).lineTo(*p3).close().extrude(gusset_thickness, both=True)

result = result.union(gusset)

# 4. Machining/Holes
# Create a drilling plane that starts below the object to cut through everything
drill_plane = cq.Workplane("XY").workplane(offset=-10)

# Motor Bore
result = result.cut(drill_plane.moveTo(motor_center_x, motor_center_y).circle(motor_bore_dia/2).extrude(200))

# Motor Mounting Holes
offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
for ox, oy in offsets:
    hx = motor_center_x + ox * (motor_mount_pitch/2)
    hy = motor_center_y + oy * (motor_mount_pitch/2)
    result = result.cut(drill_plane.moveTo(hx, hy).circle(motor_screw_dia/2).extrude(200))

# Bearing Bore
result = result.cut(drill_plane.moveTo(bearing_center_x, bearing_center_y).circle(bearing_bore_dia/2).extrude(200))
# Bearing Notch (small circular relief at bottom of the bearing hole)
result = result.cut(drill_plane.moveTo(bearing_center_x, bearing_center_y - bearing_bore_dia/2).circle(notch_dia/2).extrude(200))

# Top Slot (Vertical)
result = result.cut(drill_plane.moveTo(slot_pos[0], slot_pos[1]).rect(slot_size[0], slot_size[1]).extrude(200))

# Top Holes (Small and Large sets)
hole_locations_small = [(5.0, 42.0), (5.0, 50.0)]
hole_locations_large = [(30.0, 48.0), (45.0, 45.0)]

for loc in hole_locations_small:
    result = result.cut(drill_plane.moveTo(*loc).circle(small_hole_dia/2).extrude(200))

for loc in hole_locations_large:
    result = result.cut(drill_plane.moveTo(*loc).circle(large_hole_dia/2).extrude(200))

# 5. Final Fillets
# Add a fillet at the junction of the cylinder and the plate for strength
# Selecting the edge circle that lies on the plate face centered at the bearing position
try:
    result = result.edges(cq.selectors.NearestToPointSelector((bearing_center_x, bearing_center_y + cylinder_od/2, plate_thickness))).fillet(2.0)
except Exception:
    pass