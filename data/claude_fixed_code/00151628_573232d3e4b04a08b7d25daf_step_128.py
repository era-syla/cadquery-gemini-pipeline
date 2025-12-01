import cadquery as cq
from math import pi, tan, radians, cos, sin

# --- Parameters ---
# Geometry estimated from the provided image
# Standard spur gear proportions assumed
module = 2.0              # Scaling factor
num_teeth = 48            # Counted approximately 12 teeth per quadrant
pressure_angle = 20.0     # Standard pressure angle
thickness = 10.0          # Estimated gear thickness

# Calculated Gear Dimensions
pitch_radius = (module * num_teeth) / 2.0
addendum = module
dedendum = 1.25 * module
root_radius = pitch_radius - dedendum
tip_radius = pitch_radius + addendum

# Hole Dimensions
bore_diameter = 30.0         # Central bore, approx 30% of OD
mounting_pcd = 60.0          # Pitch Circle Diameter for mounting holes
large_hole_dia = 12.0        # Larger mounting holes (horizontal)
small_hole_dia = 6.0         # Smaller mounting holes (vertical)

# --- Tooth Profile Calculation ---
# Calculating a trapezoidal tooth profile for robust generation
# Tooth thickness at pitch circle
circular_pitch = pi * module
tooth_thick_pitch = circular_pitch / 2.0
half_thick_pitch = tooth_thick_pitch / 2.0

# Calculate width at tip and base based on pressure angle
# We extend the base slightly into the root cylinder for a solid union
overlap = 0.5
base_radius_calc = root_radius - overlap
tan_pa = tan(radians(pressure_angle))

# Width adjustments
# w_tip = w_pitch - 2 * (dist_to_tip * tan(pa))
# w_base = w_pitch + 2 * (dist_to_base * tan(pa))
half_thick_tip = half_thick_pitch - (tip_radius - pitch_radius) * tan_pa
half_thick_base = half_thick_pitch - (base_radius_calc - pitch_radius) * tan_pa

# Define vertices for one tooth (Counter-Clockwise)
tooth_pts = [
    (base_radius_calc, -half_thick_base),
    (tip_radius, -half_thick_tip),
    (tip_radius, half_thick_tip),
    (base_radius_calc, half_thick_base)
]

# --- 3D Generation ---

# 1. Create the main hub (root cylinder)
result = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# 2. Generate Teeth
# Create teeth using a loop instead of polarArray
for i in range(num_teeth):
    angle = 360.0 * i / num_teeth
    tooth = (
        cq.Workplane("XY")
        .polyline(tooth_pts)
        .close()
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(tooth)

# 3. Cut Central Bore
result = result.faces(">Z").workplane().hole(bore_diameter)

# 4. Cut Mounting Holes
# The image shows two larger holes on the horizontal axis 
# and two smaller holes on the vertical axis.

# Large holes (X-axis)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(mounting_pcd / 2.0, 0), (-mounting_pcd / 2.0, 0)])
    .hole(large_hole_dia)
)

# Small holes (Y-axis)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(0, mounting_pcd / 2.0), (0, -mounting_pcd / 2.0)])
    .hole(small_hole_dia)
)