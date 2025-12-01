import cadquery as cq

# --- Parameters ---
thickness = 6.0
v_length = 75.0      # Vertical arm length (center-to-center)
h_length = 60.0      # Horizontal arm length (center-to-center)
z_offset = 15.0      # Z-height offset between arms
hole_dia = 9.0       # Diameter of holes

r_top = 12.0         # Radius of top end
r_corner = 16.0      # Radius of corner
r_end = 12.0         # Radius of horizontal end

ramp_start_x = 18.0  # X start of the transition ramp (relative to corner center)
ramp_end_x = 35.0    # X end of the transition ramp

# --- Modeling ---

# 1. Vertical Arm Construction (XY Plane)
# Main body created as a Hull of the top circle and the corner circle
v_arm_main = (
    cq.Workplane("XY")
    .moveTo(0, v_length).circle(r_top)
    .moveTo(0, 0).circle(r_corner)
    .consolidateWires()
    .extrude(thickness)
)

# Extension stub for the vertical arm to meet the ramp
# A rectangle from x=0 to x=ramp_start_x
v_ext = (
    cq.Workplane("XY")
    .moveTo(ramp_start_x / 2, 0)
    .rect(ramp_start_x, r_corner * 2)
    .extrude(thickness)
)

# 2. Horizontal Arm Construction (Offset Plane)
# End rounded tip cylinder
h_arm_tip = (
    cq.Workplane("XY")
    .workplane(offset=-z_offset)
    .moveTo(h_length, 0)
    .circle(r_end)
    .extrude(thickness)
)

# Extension stub for the horizontal arm to meet the ramp
# A rectangle from x=ramp_end_x to x=h_length
flat_len = h_length - ramp_end_x
h_ext_center_x = ramp_end_x + flat_len / 2
h_ext = (
    cq.Workplane("XY")
    .workplane(offset=-z_offset)
    .moveTo(h_ext_center_x, 0)
    .rect(flat_len, r_end * 2)
    .extrude(thickness)
)

# 3. Transition Ramp (Loft)
# Profile at the start of the ramp (matching vertical arm width, Z=0)
p_start = (
    cq.Workplane("YZ")
    .workplane(offset=ramp_start_x)
    .center(0, thickness / 2)
    .rect(r_corner * 2, thickness)
)

# Profile at the end of the ramp (matching horizontal arm width, Z=-z_offset)
p_end = (
    cq.Workplane("YZ")
    .workplane(offset=ramp_end_x)
    .center(0, -z_offset + thickness / 2)
    .rect(r_end * 2, thickness)
)

# Create the solid transition by lofting the two profiles
ramp = cq.Workplane("XY").add(p_start).add(p_end).loft()

# 4. Combine Solids
# Union all parts together
result = v_arm_main.union(v_ext).union(h_arm_tip).union(h_ext).union(ramp)

# 5. Cut Holes
# Top Hole
result = result.cut(
    cq.Workplane("XY").moveTo(0, v_length).circle(hole_dia / 2).extrude(thickness * 2, both=True)
)
# Corner Hole
result = result.cut(
    cq.Workplane("XY").moveTo(0, 0).circle(hole_dia / 2).extrude(thickness * 2, both=True)
)
# End Hole (defined on the lower plane)
result = result.cut(
    cq.Workplane("XY").workplane(offset=-z_offset).moveTo(h_length, 0).circle(hole_dia / 2).extrude(thickness * 2, both=True)
)