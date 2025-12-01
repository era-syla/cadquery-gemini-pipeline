import cadquery as cq

# 1. Define Dimensions (in mm) based on visual estimation of a Flanged Bearing
# The proportions suggest a standard flanged ball bearing (e.g., F6900 series).
bore_diameter = 10.0
outer_diameter = 22.0
flange_diameter = 25.0
total_width = 8.0
flange_width = 2.0
recess_depth = 1.0  # Depth of the seal/shield area
ring_wall_thickness = 2.5  # Radial thickness of the inner and outer rings

# Derived Geometry
r_bore = bore_diameter / 2.0
r_outer = outer_diameter / 2.0
r_flange = flange_diameter / 2.0

# Define inner and outer race boundaries
r_inner_race_end = r_bore + ring_wall_thickness
r_outer_race_start = r_outer - ring_wall_thickness

# 2. Define the Cross-Section Profile
# We sketch on the XZ plane. The Y-axis of the XZ plane (Global Z) will be the axis of revolution.
# Coordinates are (Radius, Z-height). Z=0 is the back (flange) face, Z=total_width is the front face.
points = [
    (r_bore, 0),                                      # Start at bore, back face
    (r_bore, total_width),                            # Bore, front face
    (r_inner_race_end, total_width),                  # Inner ring face outer edge
    (r_inner_race_end, total_width - recess_depth),   # Step down into shield recess
    (r_outer_race_start, total_width - recess_depth), # Step across shield recess
    (r_outer_race_start, total_width),                # Step up to outer ring
    (r_outer, total_width),                           # Outer ring front face outer edge
    (r_outer, flange_width),                          # Outer cylinder wall down to flange
    (r_flange, flange_width),                         # Step out to flange OD
    (r_flange, 0)                                     # Flange outer edge to back face
]

# 3. Generate the 3D Object
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# 4. Apply Chamfers
# The image shows chamfers on the bore and outer edges.
chamfer_size = 0.5

# Chamfer the front bore edge
result = result.edges(cq.NearestToPointSelector((r_bore, 0, total_width))).chamfer(chamfer_size)

# Chamfer the front outer ring edge
result = result.edges(cq.NearestToPointSelector((r_outer, 0, total_width))).chamfer(chamfer_size)

# Chamfer the back flange edge
result = result.edges(cq.NearestToPointSelector((r_flange, 0, 0))).chamfer(chamfer_size)