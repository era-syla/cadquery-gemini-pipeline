import cadquery as cq

# --- Parameters ---
# Estimated dimensions based on visual proportions
base_width = 60.0       # Width of the base of the triangle
peak_height = 35.0      # Height of the two peaks
valley_height = 18.0    # Height of the central valley
peak_offset_x = 15.0    # X distance of peaks from the center
extrusion_thickness = 4.0
wall_thickness = 4.0    # Width of the frame
eyelet_outer_radius = 4.0
eyelet_inner_radius = 2.0
eyelet_overlap = 1.0    # Amount the eyelet merges into the peak

# --- Geometry Construction ---

# 1. Define the outer profile coordinates
#    Tracing the shape: Bottom-Right -> Right-Peak -> Valley -> Left-Peak -> Bottom-Left
#    The .close() method will automatically create the bottom edge
pts = [
    (base_width / 2, 0),
    (peak_offset_x, peak_height),
    (0, valley_height),
    (-peak_offset_x, peak_height),
    (-base_width / 2, 0)
]

# Create the base polygon and extrude it
base_profile = cq.Workplane("XY").polyline(pts).close().extrude(extrusion_thickness)

# 2. Create the frame
#    Generate the inner profile by offsetting and cut from the base
inner_profile = cq.Workplane("XY").polyline(pts).close().offset2D(-wall_thickness, kind="intersection").extrude(extrusion_thickness)
frame = base_profile.cut(inner_profile)

# 3. Create the eyelet (loop)
#    Positioned on the right peak (positive X)
#    Center Y is adjusted so the ring sits on top with a slight structural overlap
eyelet_center_x = peak_offset_x
eyelet_center_y = peak_height + eyelet_outer_radius - eyelet_overlap

# Define the outer circle of the ring and extrude
eyelet_outer = cq.Workplane("XY").center(eyelet_center_x, eyelet_center_y).circle(eyelet_outer_radius).extrude(extrusion_thickness)

# Define the hole of the ring and extrude
eyelet_hole = cq.Workplane("XY").center(eyelet_center_x, eyelet_center_y).circle(eyelet_inner_radius).extrude(extrusion_thickness)

# 4. Combine
#    Union the eyelet outer shape with the frame
#    Cut the eyelet hole from the result
result = frame.union(eyelet_outer).cut(eyelet_hole)