import cadquery as cq

# ---------------------------------------------------------
# Parameters for Aluminum Extrusion Profile (approx 2020 size)
# ---------------------------------------------------------
length = 300.0           # Total length of the extrusion
size = 20.0              # Profile width/height (20mm)
corner_radius = 1.5      # Fillet radius for the outer corners
center_hole_dia = 5.0    # Diameter of the central hole

# T-Slot geometry dimensions
slot_opening = 6.0       # Width of the slot opening
slot_inner_width = 10.0  # Width of the internal cavity
slot_total_depth = 5.5   # Depth from outer surface to bottom of slot
slot_neck_depth = 1.5    # Depth of the narrow opening section

# ---------------------------------------------------------
# Geometry Construction
# ---------------------------------------------------------

def create_profile_sketch():
    """Generates the 2D cross-section of the extrusion."""
    
    # 1. Base Shape: Square with rounded corners
    s = cq.Sketch().rect(size, size).vertices().fillet(corner_radius)
    
    # 2. Center Hole: Subtract a circle from the center
    s = s.circle(center_hole_dia / 2.0, mode='s')
    
    # 3. Create the T-Slot Cutter
    # We construct the shape of one slot (void) and rotate it for the other 3 sides.
    # We define the slot on the +X face (Right side).
    # The profile center is (0,0), right edge is at x = size/2.
    
    half_size = size / 2.0
    
    # Part A: The Neck (Narrow entrance)
    # Dimensions: width along X, height along Y
    neck_w = slot_neck_depth
    neck_h = slot_opening
    # Center position: standard rect is centered at origin, so we move it.
    # X Center = Edge - half_width
    neck_x = half_size - (neck_w / 2.0)
    neck = cq.Sketch().push([(neck_x, 0)]).rect(neck_w, neck_h)
    
    # Part B: The Cavity (Inner wide section)
    cavity_w = slot_total_depth - slot_neck_depth
    cavity_h = slot_inner_width
    # X Center = (Edge - neck_depth) - half_cavity_width
    cavity_x = (half_size - slot_neck_depth) - (cavity_w / 2.0)
    cavity = cq.Sketch().push([(cavity_x, 0)]).rect(cavity_w, cavity_h)
    
    # Union the neck and cavity to form the full T-slot shape
    slot_cutter = neck + cavity
    
    # 4. Apply the T-Slot Cutter to all 4 sides
    for i in range(4):
        angle = i * 90.0
        # Rotate the cutter around the Z-axis (0,0,0)
        rotated_cutter = slot_cutter.moved(cq.Location(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), angle))
        # Subtract the cutter from the main profile sketch
        s = s - rotated_cutter
        
    return s

# Generate the 2D profile
profile = create_profile_sketch()

# Extrude to create the 3D object
result = cq.Workplane("XY").placeSketch(profile).extrude(length)