import cadquery as cq
import math

# Object Analysis and Dimensions:
# The object resembles a Thorlabs SM2A6 adapter or similar optical component.
# Shape: Flat cylindrical ring (washer/adapter plate).
# Dimensions estimated based on standard SM2 (approx 2") and SM1 (approx 1") sizing.
outer_diameter = 52.0  # Approx 52mm (2 inches)
inner_diameter = 26.0  # Approx 26mm (1 inch)
thickness = 4.5        # Estimated thickness
chamfer_outer = 1.0    # Prominent chamfer on the top outer edge
spanner_hole_dia = 1.8 # Small holes for spanner wrench
spanner_hole_depth = 2.0
# Spanner holes are located roughly midway between ID and OD
spanner_bc_radius = (outer_diameter/2.0 + inner_diameter/2.0) / 2.0

# 1. Create the main cylindrical body
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(thickness)

# 2. Cut the central hole (Through hole)
result = result.faces(">Z").workplane().circle(inner_diameter / 2.0).cutThruAll()

# 3. Add Spanner Wrench Holes
# These are two small blind holes on the top face, 180 degrees apart.
# Based on the image, they are oriented diagonally. We calculate positions for 135 and 315 degrees.
angle_deg = 135
x1 = spanner_bc_radius * math.cos(math.radians(angle_deg))
y1 = spanner_bc_radius * math.sin(math.radians(angle_deg))
x2 = spanner_bc_radius * math.cos(math.radians(angle_deg + 180))
y2 = spanner_bc_radius * math.sin(math.radians(angle_deg + 180))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(x1, y1), (x2, y2)])
    .circle(spanner_hole_dia / 2.0)
    .cutBlind(-spanner_hole_depth)
)

# 4. Apply Chamfers
# Top Outer Edge: Large visible chamfer.
result = result.faces(">Z").edges("%Circle").chamfer(chamfer_outer)

# Top Inner Edge: Small chamfer (deburring/thread relief), visually subtle but likely present.
result = result.faces(">Z").workplane().edges("<Circle").chamfer(0.2)