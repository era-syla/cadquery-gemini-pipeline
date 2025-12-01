import cadquery as cq

# Define the geometry parameters for the Batman logo shape
thickness = 2.0

# Coordinates for the right half of the profile
# Coordinates are defined as (x, y) assuming the center is near origin
p_tail = (0, -15)          # Bottom center point (tail)
p_wing_tip = (60, 20)      # Right wing tip
p_shoulder = (15, 8)       # Shoulder (connection between wing and head)
p_ear_tip = (6, 25)        # Right ear tip
p_head_center = (0, 15)    # Center point between ears (dip)

# Intermediate points for the 3-point arcs
# Bottom wing curve: curves inwards (concave), so point is "above" the straight line
p_arc_bottom = (30, 5)
# Top wing curve: curves inwards (concave), so point is "below" the straight line
p_arc_top = (38, 11)

# Generate the 3D object
result = (
    cq.Workplane("XY")
    .moveTo(p_tail[0], p_tail[1])
    # Draw Right Side
    .threePointArc(p_arc_bottom, p_wing_tip)
    .threePointArc(p_arc_top, p_shoulder)
    .lineTo(p_ear_tip[0], p_ear_tip[1])
    .lineTo(p_head_center[0], p_head_center[1])
    # Draw Left Side (Mirror of Right Side)
    .lineTo(-p_ear_tip[0], p_ear_tip[1])
    .lineTo(-p_shoulder[0], p_shoulder[1])
    # Mirror x-coordinates for the arcs
    .threePointArc((-p_arc_top[0], p_arc_top[1]), (-p_wing_tip[0], p_wing_tip[1]))
    .threePointArc((-p_arc_bottom[0], p_arc_bottom[1]), (p_tail[0], p_tail[1]))
    .close()
    .extrude(thickness)
)