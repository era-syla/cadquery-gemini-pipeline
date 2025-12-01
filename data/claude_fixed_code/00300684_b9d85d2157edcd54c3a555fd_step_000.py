import cadquery as cq
import math

# --- Parametric Dimensions ---
outer_diameter = 100.0
height = 10.0
rim_thickness = 5.0
hub_diameter = 15.0
shaft_diameter = 4.0
num_blades = 10

# Blade profile parameters (angles in degrees)
blade_sweep = 60.0       # Angle between root start and tip start
blade_width_root = 15.0  # Angular width at the hub
blade_width_tip = 25.0   # Angular width at the rim
curve_bow = 10.0         # Controls the curvature of the blade

# --- Derived Geometry Calculations ---
r_outer = outer_diameter / 2.0
r_rim_inner = r_outer - rim_thickness
r_hub = hub_diameter / 2.0
r_mid = (r_hub + r_rim_inner) / 2.0

# Helper function: Polar to Cartesian coordinates
def p2c(r, angle_deg):
    rad = math.radians(angle_deg)
    return (r * math.cos(rad), r * math.sin(rad))

# Define the 4 corner points of a single blade profile
angle_p1 = 0.0
angle_p2 = blade_sweep
angle_p3 = blade_sweep + blade_width_tip
angle_p4 = blade_width_root

p1 = p2c(r_hub, angle_p1)
p2 = p2c(r_rim_inner, angle_p2)
p3 = p2c(r_rim_inner, angle_p3)
p4 = p2c(r_hub, angle_p4)

# Define midpoints for 3-point arcs to control curvature
angle_mid_leading = (angle_p1 + angle_p2) / 2.0 - curve_bow
p_mid_leading = p2c(r_mid, angle_mid_leading)

angle_mid_trailing = (angle_p4 + angle_p3) / 2.0 - curve_bow
p_mid_trailing = p2c(r_mid, angle_mid_trailing)

angle_mid_rim = (angle_p2 + angle_p3) / 2.0
p_mid_rim = p2c(r_rim_inner, angle_mid_rim)

angle_mid_hub = (angle_p4 + angle_p1) / 2.0
p_mid_hub = p2c(r_hub, angle_mid_hub)

# --- Geometry Creation ---

# 1. Create the Hub (Cylinder with hole)
hub = (cq.Workplane("XY")
       .circle(r_hub)
       .circle(shaft_diameter / 2.0)
       .extrude(height))

# 2. Create the Outer Rim (Hollow Tube)
rim = (cq.Workplane("XY")
       .circle(r_outer)
       .circle(r_rim_inner)
       .extrude(height))

# 3. Create a Single Blade
blade_solid = (cq.Workplane("XY")
               .moveTo(*p1)
               .threePointArc(p_mid_leading, p2)   # Leading edge curve
               .threePointArc(p_mid_rim, p3)       # Arc along rim
               .threePointArc(p_mid_trailing, p4)  # Trailing edge curve
               .threePointArc(p_mid_hub, p1)       # Arc along hub
               .close()
               .extrude(height))

# 4. Pattern the Blades and Union
result = hub.union(rim)

for i in range(num_blades):
    angle = 360.0 * i / num_blades
    rotated_blade = blade_solid.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_blade)