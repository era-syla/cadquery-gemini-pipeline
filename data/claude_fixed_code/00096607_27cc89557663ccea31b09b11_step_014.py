import cadquery as cq
import math

# --- Parameters ---
# Dimensions are estimated based on visual proportions
radius = 120.0        # Mean radius of the curved beam
width = 15.0          # Width of the beam cross-section
thickness = 12.0      # Thickness (height) of the beam
angle_sweep = 60.0    # Angle of the arc segment in degrees

# Head (mounting end) parameters
head_len = 25.0       # Length of the head extending from the beam start
head_width_scale = 1.8 # Head width relative to beam width
head_lobe_rad = 8.0   # Radius of the rounded lobes
lobe_spacing = 14.0   # Distance between the two rear lobe centers

# Hole parameters
hole_dia = 4.0

# --- Geometry Construction ---

# 1. Main Curved Beam
# Defined by constructing a face from arcs and lines, then extruding
r_inner = radius - width / 2
r_outer = radius + width / 2

# Calculate key points for the arc sketch
rad_start = 0
rad_end = math.radians(angle_sweep)
rad_mid = math.radians(angle_sweep / 2)

# Start points (at angle 0)
p_start_in = (r_inner, 0)
p_start_out = (r_outer, 0)

# Mid points (for defining the arc)
p_mid_in = (r_inner * math.cos(rad_mid), r_inner * math.sin(rad_mid))
p_mid_out = (r_outer * math.cos(rad_mid), r_outer * math.sin(rad_mid))

# End points (at angle sweep)
p_end_in = (r_inner * math.cos(rad_end), r_inner * math.sin(rad_end))
p_end_out = (r_outer * math.cos(rad_end), r_outer * math.sin(rad_end))

# Create the beam body
beam = (
    cq.Workplane("XY")
    .moveTo(*p_start_in)
    .lineTo(*p_start_out)
    .threePointArc(p_mid_out, p_end_out)
    .lineTo(*p_end_in)
    .threePointArc(p_mid_in, p_start_in)
    .close()
    .extrude(thickness)
)

# 2. Mounting Head
# Created as a separate shape at the start of the beam and unioned
# Modeled as two circular lobes and a central filler block
head_center_y = -10.0 # Shifted back from the beam start (y=0)
lobe_y = head_center_y

# Left Lobe
lobe_left = (
    cq.Workplane("XY")
    .center(radius - lobe_spacing/2, lobe_y)
    .circle(head_lobe_rad)
    .extrude(thickness)
)

# Right Lobe
lobe_right = (
    cq.Workplane("XY")
    .center(radius + lobe_spacing/2, lobe_y)
    .circle(head_lobe_rad)
    .extrude(thickness)
)

# Center filler (connects lobes to the beam start)
# It overlaps with the beam start (y=0) and the lobes
filler = (
    cq.Workplane("XY")
    .center(radius, lobe_y/2)
    .rect(lobe_spacing + 2, abs(lobe_y) + 5)
    .extrude(thickness)
)

# Combine head parts
head = lobe_left.union(lobe_right).union(filler)

# Union Head with Beam
result = beam.union(head)

# 3. Refinement: Fillets
# Fillet the vertical edges near the connection point (radius, 0)
try:
    result = result.edges(cq.NearestToPointSelector((radius - width/2, 0, thickness/2))).fillet(5.0)
    result = result.edges(cq.NearestToPointSelector((radius + width/2, 0, thickness/2))).fillet(5.0)
except:
    pass # In case selection fails, skip fillets

# 4. Holes
# 3 holes in a triangular pattern on the head
hole_locations = [
    (radius - lobe_spacing/2, lobe_y), # Lobe 1
    (radius + lobe_spacing/2, lobe_y), # Lobe 2
    (radius, -2.0)                     # Near the beam connection
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(hole_locations)
    .hole(hole_dia)
)

# 5. End Chamfer
# Chamfer the top edge of the far end of the beam
# Calculate the approximate position of the top edge at the end of the arc
end_edge_point = (radius * math.cos(rad_end), radius * math.sin(rad_end), thickness)

result = result.edges(cq.NearestToPointSelector(end_edge_point)).chamfer(3.0)