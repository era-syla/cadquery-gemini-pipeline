import cadquery as cq
import math

# --- Parameters ---
thickness = 6.0          # Thickness of the tool
w_handle = 18.0          # Width of the handle section
l_handle = 85.0          # Vertical distance from bottom hole center to head center
r_outer = 35.0           # Outer radius of the hook head
r_inner = 22.0           # Inner radius of the hook head
r_fillet = 30.0          # Radius of the transition fillet between handle and head
hole_dia = 10.0          # Diameter of the hanging hole

# --- Geometric Calculations ---

# 1. Define Centers
# Origin (0,0) is at the center of the bottom hole
# Head Center Calculation:
# The left edge of the handle (x = -w_handle/2) transitions tangentially into the outer head radius.
# Therefore, Head Center X is offset by r_outer from the left edge.
head_center_x = -w_handle/2 + r_outer
head_center_y = l_handle

# 2. Key Points Definition
p_start = (w_handle/2, 0)
p_bottom_mid = (0, -w_handle/2)
p_bottom_end = (-w_handle/2, 0)
p_head_start = (-w_handle/2, l_handle)  # Start of outer arc (left side)

# 3. Outer Hook Arc Points
# Arc starts at 180 degrees (left) relative to head center
# Arc ends at the tip. Let's assume the tip is at -15 degrees (pointing slightly down/right)
angle_tip = -15
p_tip = (
    head_center_x + r_outer * math.cos(math.radians(angle_tip)),
    head_center_y + r_outer * math.sin(math.radians(angle_tip))
)
# Intermediate point for the outer arc (Top / 90 degrees) to ensure correct curvature direction
p_outer_mid = (head_center_x, head_center_y + r_outer)

# 4. Tooth/Hook Tip Geometry
# Define a point on the inner radius to connect the tooth to.
# We create a small "hook" shape by cutting back to a slightly lower angle on the inner circle.
angle_tooth_inner = -25
p_tooth_inner = (
    head_center_x + r_inner * math.cos(math.radians(angle_tooth_inner)),
    head_center_y + r_inner * math.sin(math.radians(angle_tooth_inner))
)

# 5. Transition Fillet (Throat)
# We need an arc tangent to the Inner Circle and the Right Handle Edge (x = w_handle/2)
# Fillet Center (fx, fy):
# fx must be (w_handle/2 + r_fillet)
fx = w_handle/2 + r_fillet
# Distance from Fillet Center to Head Center must be (r_inner + r_fillet)
dist_centers = r_inner + r_fillet
dx = fx - head_center_x
# Solve for fy: dist^2 = dx^2 + (head_center_y - fy)^2
dy = math.sqrt(dist_centers**2 - dx**2)
fy = head_center_y - dy # The fillet is below the head

# Calculate Start and End points of this fillet arc
# p_fillet_start is on the inner circle (intersection of the line connecting centers)
vec_len = dist_centers
vx = (fx - head_center_x) / vec_len
vy = (fy - head_center_y) / vec_len
p_fillet_start = (head_center_x + r_inner * vx, head_center_y + r_inner * vy)

# p_fillet_end is on the handle edge
p_fillet_end = (w_handle/2, fy)

# Calculate midpoint for the fillet arc for threePointArc
angle_f_start = math.degrees(math.atan2(p_fillet_start[1] - fy, p_fillet_start[0] - fx))
angle_f_end = 180.0 # Tangent to vertical line on the left of the circle center implies 180 deg
angle_f_mid = (angle_f_start + angle_f_end) / 2
p_fillet_mid = (
    fx + r_fillet * math.cos(math.radians(angle_f_mid)),
    fy + r_fillet * math.sin(math.radians(angle_f_mid))
)

# Calculate midpoint for the Inner Arc (between tooth and fillet start)
angle_i_start = angle_tooth_inner
angle_i_end = math.degrees(math.atan2(p_fillet_start[1] - head_center_y, p_fillet_start[0] - head_center_x))
angle_i_mid = (angle_i_start + angle_i_end) / 2
p_inner_mid = (
    head_center_x + r_inner * math.cos(math.radians(angle_i_mid)),
    head_center_y + r_inner * math.sin(math.radians(angle_i_mid))
)

# --- Build Geometry ---

result = (
    cq.Workplane("XY")
    .moveTo(*p_start)
    # 1. Bottom rounded end
    .threePointArc(p_bottom_mid, p_bottom_end)
    # 2. Left straight side
    .lineTo(*p_head_start)
    # 3. Outer Hook Curve
    .threePointArc(p_outer_mid, p_tip)
    # 4. Tooth Cut (Straight line in)
    .lineTo(*p_tooth_inner)
    # 5. Inner Curve
    .threePointArc(p_inner_mid, p_fillet_start)
    # 6. Throat Fillet
    .threePointArc(p_fillet_mid, p_fillet_end)
    # 7. Right straight side back to start
    .lineTo(*p_start)
    .close()
    # 8. Create Solid
    .extrude(thickness)
    # 9. Cut the hanging hole
    .faces(">Z").workplane()
    .circle(hole_dia / 2)
    .cutThruAll()
)