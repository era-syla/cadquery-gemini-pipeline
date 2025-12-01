import cadquery as cq

# --- Dimensions & Parameters ---
# Modeled after a standard 6-inch aluminum robotics channel (e.g., Actobotics-style)
length = 152.4      # Total Length (6 inches)
width = 38.1        # Outer Width (1.5 inches)
height = 38.1       # Outer Height/Depth (1.5 inches)
thickness = 2.5     # Wall thickness (~0.1 inches)
fillet_corner = 6.0 # Radius for the rounded corners of the flanges
fillet_bend = 3.0   # Radius for the structural bends

# Hole Parameters
r_large = 12.7 / 2.0      # Large center hole radius (0.5" dia)
r_small = 3.8 / 2.0       # Small mounting hole radius (~#6 screw)
r_sat_bc = 19.56 / 2.0    # Radius of satellite hole pattern (0.77" PCD)
pitch = 38.1              # Pitch between pattern cells (1.5 inches)

# --- 1. Create Base U-Channel ---
# Define the U-profile points in the XY plane.
# The U opens towards +Y. The web is at -Y.
pts = [
    (-width/2 + thickness, height/2),          # Top-Left Inner
    (-width/2 + thickness, -height/2 + thickness), # Bottom-Left Inner
    (width/2 - thickness, -height/2 + thickness),  # Bottom-Right Inner
    (width/2 - thickness, height/2),           # Top-Right Inner
    (width/2, height/2),                       # Top-Right Outer
    (width/2, -height/2),                      # Bottom-Right Outer
    (-width/2, -height/2),                     # Bottom-Left Outer
    (-width/2, height/2)                       # Top-Left Outer
]

# Extrude the profile along the Z-axis centered at origin
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(length / 2.0, both=True)
)

# --- 2. Apply Fillets ---
# Fillet the long structural bends (edges parallel to Z at the bottom of the U)
result = result.edges("|Z and <Y").fillet(fillet_bend)

# Fillet the exposed corners of the flanges (edges parallel to X at the top of the U)
result = result.edges("|X and >Y").fillet(fillet_corner)

# --- 3. Drill Hole Patterns ---
# Define Z-coordinates for the features
# 4 large holes centered along the length
z_large = [-1.5 * pitch, -0.5 * pitch, 0.5 * pitch, 1.5 * pitch]
# Small holes located halfway between the large holes
z_inter = [-1.0 * pitch, 0.0, 1.0 * pitch]

# Define which faces to drill.
# ">X" is the Right face (cutThruAll will penetrate the Left face too).
# "<Y" is the Back face (web).
faces_to_process = [">X", "<Y"]

for face_sel in faces_to_process:
    # 1. Main Large Holes (Center of each cell)
    result = (
        result.faces(face_sel)
        .workplane()
        .pushPoints([(0, z) for z in z_large])
        .circle(r_large)
        .cutThruAll()
    )

    # 2. Satellite Pattern (8 small holes)
    # Applied to the top (index 3) and bottom (index 0) large holes
    for z in [z_large[0], z_large[3]]:
        import math
        sat_points = []
        for i in range(8):
            angle = i * 360.0 / 8.0
            x = r_sat_bc * math.cos(math.radians(angle))
            y = r_sat_bc * math.sin(math.radians(angle)) + z
            sat_points.append((x, y))
        
        result = (
            result.faces(face_sel)
            .workplane()
            .pushPoints(sat_points)
            .circle(r_small)
            .cutThruAll()
        )

    # 3. Intermediate Small Holes
    # Single small holes centered between the pattern blocks
    result = (
        result.faces(face_sel)
        .workplane()
        .pushPoints([(0, z) for z in z_inter])
        .circle(r_small)
        .cutThruAll()
    )

# Result is ready in 'result' variable