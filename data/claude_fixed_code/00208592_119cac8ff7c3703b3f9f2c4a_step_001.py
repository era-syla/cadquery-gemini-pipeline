import cadquery as cq
import math

# --- Parameters ---
total_length = 25.0
shank_len = 14.0
hex_flat_size = 6.35  # 1/4 inch
# CadQuery polygon uses the circumscribed diameter
hex_circum_dia = hex_flat_size / (math.sqrt(3) / 2)

neck_len = 3.0
head_radius = 2.4  # Approx 4.8mm diameter for the cylindrical part of the head
tip_len = total_length - shank_len - neck_len  # Remaining length for the head

# --- 1. Hex Shank ---
# Create the hexagonal body
shank = (
    cq.Workplane("XY")
    .polygon(6, hex_circum_dia)
    .extrude(shank_len)
)

# Add a chamfer to the back end
shank = shank.edges("|Z").chamfer(0.5)

# --- 2. Transition Neck ---
# Loft from a circle fitting the hex flat to the head radius
# This simulates the turned section often found on bits
neck_base_radius = hex_flat_size / 2.0
neck = (
    cq.Workplane("XY")
    .workplane(offset=shank_len)
    .circle(neck_base_radius)
    .workplane(offset=neck_len)
    .circle(head_radius)
    .loft()
)

# --- 3. Head (Cylinder + Tapered Tip) ---
# The head consists of a short cylindrical section and then the tapered cone
head_cyl_len = 2.0
head_cone_len = tip_len - head_cyl_len

head = (
    cq.Workplane("XY")
    .workplane(offset=shank_len + neck_len)
    .circle(head_radius)
    .extrude(head_cyl_len)
    .faces(">Z")
    .workplane()
    .circle(head_radius)
    .workplane(offset=head_cone_len)
    .circle(0.6)  # Blunt tip diameter
    .loft()
)

# Combine the main body parts
body = shank.union(neck).union(head)

# --- 4. Phillips Flute Cutters ---
def create_cutter(angle):
    """
    Creates a wedge-shaped cutting tool to remove material between the wings.
    The cutter is defined on a plane rotated by 'angle' around Z.
    """
    # Z-heights for the cut
    z_start = shank_len + neck_len + 0.5  # Start the cut slightly up the head
    z_end = total_length + 1.0  # Cut past the tip
    
    # Parameters for the V-shape (the empty space)
    # r_inner determines the web thickness of the cross
    r_inner_base = 1.4  # Thicker web at base
    r_inner_tip = 0.4   # Thin web at tip
    
    r_outer = 8.0  # Large enough to clear the outside
    w_outer = 8.0  # Width of the wedge at the outside
    
    # Define the cutter using a loft between two triangular profiles
    cutter = (
        cq.Workplane("XY").transformed(rotate=(0, 0, angle))
        .workplane(offset=z_start)
        .moveTo(r_inner_base, 0)
        .lineTo(r_outer, w_outer/2)
        .lineTo(r_outer, -w_outer/2)
        .close()
        .workplane(offset=z_end - z_start)
        .moveTo(r_inner_tip, 0)
        .lineTo(r_outer, w_outer/2)
        .lineTo(r_outer, -w_outer/2)
        .close()
        .loft(combine=True)
    )
    return cutter

# Generate the 4 cutters at 45 degree offsets to the main axes
# (Phillips wings are typically aligned with X/Y, cuts are diagonal)
cutters = create_cutter(45)
for ang in [135, 225, 315]:
    cutters = cutters.union(create_cutter(ang))

# Apply the cuts to the body
result = body.cut(cutters)

# --- 5. Engraved Text "PH1" ---
# Select a flat face on the hex shank. 
# For a hexagon with points on X axis, faces are at 30, 90, etc. >Y selects the face at 90.
try:
    # Setup workplane on the face
    text_wp = (
        result.faces(">Y")
        .workplane(centerOption="CenterOfBoundBox")
        .transformed(rotate=(0, 0, 90)) # Rotate 90 deg so text runs along the shank length
    )
    
    # Cut the text
    result = result.cut(
        text_wp.text("PH1", 3.5, -0.4)
    )
except Exception:
    # Fallback if face selection fails (depending on exact kernel orientation)
    pass