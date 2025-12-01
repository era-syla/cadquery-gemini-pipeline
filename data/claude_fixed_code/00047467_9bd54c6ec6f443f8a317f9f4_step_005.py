import cadquery as cq

# --- Dimensions ---
# Main body (post) dimensions
radius = 12.0
width = radius * 2
straight_length = 35.0  # Length of the rectangular section
# The total length of the profile is radius + straight_length

# Flange (plate) dimensions
flange_length = 75.0
flange_width = 45.0
flange_thickness = 8.0

# --- 1. Define the Post Profile Sketch ---
# A "D-shape" or "stadium" profile: flat on one end, rounded on the other.
# Origin (0,0) is placed at the center of the semi-circle.
# Flat face is at x = straight_length.
post_sketch = (
    cq.Sketch()
    .segment((0, -radius), (straight_length, -radius))
    .segment((straight_length, radius))
    .segment((0, radius))
    .arc((0, radius), (-radius, 0), (0, -radius))
    .close()
    .assemble()
)

# --- 2. Create the Raw Post Solid ---
# Extrude the profile vertically. We make it tall enough to be cut later.
# We start below the Z=0 plane and go high up.
raw_post = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -50))
    .placeSketch(post_sketch)
    .extrude(120)
)

# --- 3. Create Cutters for Slanted Surfaces ---
# We use the XZ plane to draw the side profile of the material we want to REMOVE.

# Top Cutter: Removes material above the top slope.
# The slope goes DOWN from back (curved end, -X) to front (flat end, +X).
# Points approximate the cutting plane line + a box above it.
top_cut_pts = [
    (-50, 32),    # High point at the back
    (60, 14),     # Low point at the front
    (60, 100),    # Extend upwards
    (-50, 100)    # Close loop
]
top_cutter = (
    cq.Workplane("XZ")
    .polyline(top_cut_pts)
    .close()
    .extrude(100, both=True)  # Extrude along Y to cover the entire width
)

# Bottom Cutter: Removes material below the bottom slope.
# The slope goes UP from back (deep, -X) to front (shallow, +X).
bottom_cut_pts = [
    (-50, -30),   # Deep point at the back
    (60, -6),     # Shallow point at the front
    (60, -100),   # Extend downwards
    (-50, -100)   # Close loop
]
bottom_cutter = (
    cq.Workplane("XZ")
    .polyline(bottom_cut_pts)
    .close()
    .extrude(100, both=True)
)

# Apply the cuts to the post
shaped_post = raw_post.cut(top_cutter).cut(bottom_cutter)

# --- 4. Create the Flange ---
# A rectangular plate intersected by the post.
# It sits horizontally. We position it so the post passes through it.
flange = (
    cq.Workplane("XY")
    .rect(flange_length, flange_width)
    .extrude(flange_thickness)
    .translate((15, 0, 0))
)

# --- 5. Combine Components ---
result = shaped_post.union(flange)