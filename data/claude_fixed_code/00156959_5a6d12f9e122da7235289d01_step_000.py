import cadquery as cq

# --- Parameters ---
channel_length = 140.0
channel_width = 20.0
channel_height = 35.0
wall_thickness = 3.0

clip_od = 14.0
clip_id = 10.0
clip_height = 18.0
clip_opening_gap = 8.0
clip_spacing = 15.5
num_side_clips = 8

# --- 1. Create the U-Channel Base ---

# Define the U-profile points
w_half = channel_width / 2.0
pts = [
    (-w_half, 0),
    (w_half, 0),
    (w_half, channel_height),
    (w_half - wall_thickness, channel_height),
    (w_half - wall_thickness, wall_thickness),
    (-w_half + wall_thickness, wall_thickness),
    (-w_half + wall_thickness, channel_height),
    (-w_half, channel_height),
    (-w_half, 0)
]

# Extrude the U-channel
channel = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(channel_length)
    .translate((-channel_length / 2.0, 0, 0))
)

# Add rounded beads/lips to the top edges of the walls
bead_radius = wall_thickness / 1.5
bead_left = (
    cq.Workplane("YZ")
    .center(-w_half + wall_thickness / 2.0, channel_height)
    .circle(bead_radius)
    .extrude(channel_length)
    .translate((-channel_length / 2.0, 0, 0))
)
bead_right = (
    cq.Workplane("YZ")
    .center(w_half - wall_thickness / 2.0, channel_height)
    .circle(bead_radius)
    .extrude(channel_length)
    .translate((-channel_length / 2.0, 0, 0))
)

base_body = channel.union(bead_left).union(bead_right)

# --- 2. Create the Clip Geometry ---

def create_clip_shape():
    # Base cylinder
    clip = cq.Workplane("XY").circle(clip_od / 2.0).extrude(clip_height)
    
    # Inner hole
    hole = cq.Workplane("XY").circle(clip_id / 2.0).extrude(clip_height)
    clip = clip.cut(hole)
    
    # Opening cutout (facing negative Y direction)
    cutout = (
        cq.Workplane("XY")
        .center(0, -clip_od / 2.0)
        .rect(clip_opening_gap, clip_od)
        .extrude(clip_height)
    )
    clip = clip.cut(cutout)
    
    # Fillet the tips of the 'C' shape
    # We select vertical edges near the opening
    p_near_gap_1 = (clip_opening_gap / 2.0, -clip_od / 2.0 + 1.0, clip_height / 2.0)
    p_near_gap_2 = (-clip_opening_gap / 2.0, -clip_od / 2.0 + 1.0, clip_height / 2.0)
    
    clip = clip.edges(cq.selectors.NearestToPointSelector(p_near_gap_1)).fillet(1.0)
    clip = clip.edges(cq.selectors.NearestToPointSelector(p_near_gap_2)).fillet(1.0)
    
    return clip

single_clip = create_clip_shape()

# --- 3. Pattern Clips on the Side ---

# Calculate positions
overlap = 1.5
side_y_pos = -w_half - (clip_od / 2.0) + overlap
total_span = (num_side_clips - 1) * clip_spacing
start_x = -total_span / 2.0

final_assembly = base_body

for i in range(num_side_clips):
    x_pos = start_x + i * clip_spacing
    # The clip opening naturally faces -Y, which is outward from the wall at -Y
    clip_instance = single_clip.translate((x_pos, side_y_pos, 0))
    final_assembly = final_assembly.union(clip_instance)

# --- 4. Add End Clip ---

# The end clip is attached to the +X face
# Rotate clip 90 deg so opening faces +X
end_clip = single_clip.rotate((0, 0, 0), (0, 0, 1), 90)

# Position it
end_x_pos = (channel_length / 2.0) + (clip_od / 2.0) - overlap
end_clip = end_clip.translate((end_x_pos, 0, 0))

final_assembly = final_assembly.union(end_clip)

# --- 5. Add Mounting Holes (Optional but visible in reference) ---

# Add counterbored holes on the floor of the channel
result = (
    final_assembly.faces("<Z")
    .workplane()
    .pushPoints([(-channel_length/2.0 + 15, 0), (channel_length/2.0 - 15, 0)])
    .cboreHole(3.5, 6.5, 2.0)
)