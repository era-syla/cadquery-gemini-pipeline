import cadquery as cq

# Parameters for the geometry
thickness = 10.0
skull_height = 110.0  # Approx total height

# 1. Define the base skull shape (Right Half)
# We draw the right half profile, extrude it, and then mirror it to form the full base.
def create_skull_base():
    # Key points for the profile
    p_top = (0, 55)
    p_cranium_max = (38, 30)
    p_cheek_indent = (28, 10)
    p_cheek_spike = (34, 5)
    p_jaw_top = (22, 5)
    p_jaw_bottom = (22, -55)
    p_bottom_center = (0, -55)

    # Generate the wire
    # We use splines for the organic upper curve and lines for the angular jaw
    sk = (
        cq.Workplane("XY")
        .moveTo(*p_top)
        # Smooth spline for cranium side and cheek curve
        .spline([(20, 54), p_cranium_max, (36, 20), p_cheek_indent], includeCurrent=True)
        # Sharp protrusion for the cheekbone
        .lineTo(*p_cheek_spike)
        # Step in for the jaw
        .lineTo(*p_jaw_top)
        # Vertical side of the jaw
        .lineTo(*p_jaw_bottom)
        # Bottom edge to center
        .lineTo(*p_bottom_center)
        .close()
    )
    
    # Extrude and Mirror
    right_half = sk.extrude(thickness)
    left_half = right_half.mirror("YZ")
    
    return right_half.union(left_half)

# 2. Define the Eyes
def create_eye_cut():
    # Coordinates for a stylized angry eye
    pts = [
        (7, 18),   # Inner corner
        (20, 34),  # Top arch peak
        (30, 24),  # Outer corner
        (20, 19)   # Bottom curve control
    ]
    
    # Create the shape
    eye = (
        cq.Workplane("XY")
        .moveTo(*pts[0])
        .spline([pts[1], pts[2]], includeCurrent=True) # Upper eyelid
        .spline([pts[3], pts[0]], includeCurrent=True) # Lower eyelid
        .close()
        .extrude(thickness)
    )
    return eye

# 3. Define the Nose
def create_nose_cut():
    # A simple angular tear-drop shape for the nostril
    nose = (
        cq.Workplane("XY")
        .polyline([(1, 5), (6, 9), (4, 14), (0.5, 7)])
        .close()
        .extrude(thickness)
    )
    return nose

# 4. Define the Teeth Slots
def create_teeth_cuts():
    # Slots configuration
    slot_width = 4.0
    slot_height = 45.0
    jaw_bottom_y = -55.0
    
    # Calculate center Y for the rectangles
    center_y = jaw_bottom_y + (slot_height / 2.0)
    
    # Use pushPoints to create multiple rectangles at once
    # Slots located at x=0 (center), x=12, and x=-12
    slots = (
        cq.Workplane("XY")
        .pushPoints([(0, center_y), (12, center_y), (-12, center_y)])
        .center(0, 0)
        .rect(slot_width, slot_height)
        .extrude(thickness)
    )
    return slots

# -- Assembly --

# Generate Base
skull = create_skull_base()

# Cut Eyes (Right and Mirrored Left)
eye_tool = create_eye_cut()
skull = skull.cut(eye_tool).cut(eye_tool.mirror("YZ"))

# Cut Nose (Right and Mirrored Left)
nose_tool = create_nose_cut()
skull = skull.cut(nose_tool).cut(nose_tool.mirror("YZ"))

# Cut Teeth Slots
slots_tool = create_teeth_cuts()
skull = skull.cut(slots_tool)

# Final Result
result = skull