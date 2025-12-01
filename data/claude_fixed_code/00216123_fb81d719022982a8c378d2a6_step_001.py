import cadquery as cq

# --- Dimensions & Parameters ---
# Bounding box approx 100 x 50 x 15
thickness = 15
ribbon_w = 8  # Width of the solid frame

# --- Outer Profile Points ---
# Right Side
o_valley = (0, 30)
o_peak_r = (25, 50)
o_leg_top_r = (50, 20)
o_leg_bot_r = (50, 0)
o_bot_cen = (0, 10)

# Left Side (Symmetrical)
o_peak_l = (-25, 50)
o_leg_top_l = (-50, 20)
o_leg_bot_l = (-50, 0)

# --- Inner Profile Points ---
# Offset inwards to create the frame/hole
# Calculated to maintain roughly constant visual thickness
i_valley = (0, 22)
i_peak_r = (25, 42)
i_leg_top_r = (42, 18)
i_leg_bot_r = (42, 8)
i_bot_cen = (0, 18)

i_peak_l = (-25, 42)
i_leg_top_l = (-42, 18)
i_leg_bot_l = (-42, 8)

# --- Tangent Definitions for Splines ---
# (dx, dy) vectors to control curve shapes
tan_flat = (1, 0)
tan_slope_down = (0.5, -1)
tan_slope_up = (0.5, 1)

# Arc intermediate points for bottom curve
# Calculated to fit an arc through the leg bottoms and center peak
o_arc_mid_r = (25, 7.6)
o_arc_mid_l = (-25, 7.6)
i_arc_mid_r = (21, 15.6)
i_arc_mid_l = (-21, 15.6)

# --- Construction ---
# Create outer profile
outer = (
    cq.Workplane("XY")
    .moveTo(*o_valley)
    # Right hump: Valley -> Peak -> Leg Top
    .spline([o_peak_r], tangents=[tan_flat, tan_flat])
    .spline([o_leg_top_r], tangents=[tan_flat, tan_slope_down])
    # Right vertical leg
    .lineTo(*o_leg_bot_r)
    # Bottom Arch: Right Leg -> Center -> Left Leg
    .threePointArc(o_arc_mid_r, o_bot_cen)
    .threePointArc(o_arc_mid_l, o_leg_bot_l)
    # Left vertical leg
    .lineTo(*o_leg_top_l)
    # Left hump: Leg Top -> Peak -> Valley
    .spline([o_peak_l], tangents=[tan_slope_up, tan_flat])
    .spline([o_valley], tangents=[tan_flat, tan_flat])
    .close()
    .extrude(thickness)
)

# Create inner profile (hole)
inner = (
    cq.Workplane("XY")
    .moveTo(*i_valley)
    # Inner Right Hump
    .spline([i_peak_r], tangents=[tan_flat, tan_flat])
    .spline([i_leg_top_r], tangents=[tan_flat, tan_slope_down])
    # Inner Right Leg
    .lineTo(*i_leg_bot_r)
    # Inner Bottom Arch
    .threePointArc(i_arc_mid_r, i_bot_cen)
    .threePointArc(i_arc_mid_l, i_leg_bot_l)
    # Inner Left Leg
    .lineTo(*i_leg_top_l)
    # Inner Left Hump
    .spline([i_peak_l], tangents=[tan_slope_up, tan_flat])
    .spline([i_valley], tangents=[tan_flat, tan_flat])
    .close()
    .extrude(thickness)
)

# Subtract inner from outer to create frame
result = outer.cut(inner)