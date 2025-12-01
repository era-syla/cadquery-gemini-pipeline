import cadquery as cq

# --- Parameters ---
die_size = 20.0          # Length of the cube side
edge_fillet = 2.0        # Radius for rounded edges
pip_radius = 2.0         # Radius of the pip (dot)
pip_depth = 0.6          # Depth of the pip indentation
pip_spacing = 5.0        # Distance from center to outer pip rows/cols

# --- Helper Function to get pip coordinates ---
def get_pip_locations(number, s):
    """Returns a list of (x,y) coordinates for the pips based on the number."""
    locs = []
    # Center dot for odd numbers (1, 3, 5)
    if number % 2 == 1:
        locs.append((0, 0))
    # Diagonal pair for 2+ (2, 3, 4, 5, 6)
    if number > 1:
        locs.extend([(-s, -s), (s, s)])
    # Other diagonal pair for 4+ (4, 5, 6)
    if number > 3:
        locs.extend([(-s, s), (s, -s)])
    # Middle side dots for 6
    if number == 6:
        locs.extend([(-s, 0), (s, 0)])
    return locs

# --- 1. Base Geometry ---
# Create a cube and fillet all edges to get the basic die shape
result = (
    cq.Workplane("XY")
    .box(die_size, die_size, die_size)
    .edges()
    .fillet(edge_fillet)
)

# --- 2. Face Mapping ---
# Map numbers to faces. Using a standard die layout where opposite sides sum to 7.
# Directions: +Z (Top), -Z (Bottom), +X (Right), -X (Left), +Y (Back), -Y (Front)
face_map = {
    ">Z": 1,
    "<Z": 6,
    ">Y": 2,
    "<Y": 5,
    ">X": 3,
    "<X": 4
}

# --- 3. Create Pips ---
# Iterate through each face definition to cut the pips
for direction, number in face_map.items():
    # Get the list of (x,y) points for the pips on this face
    pts = get_pip_locations(number, pip_spacing)
    
    # Create a workplane on the selected face
    # CenterOfBoundBox ensures (0,0) is the visual center of the face
    wp = result.faces(direction).workplane(centerOption="CenterOfBoundBox")
    
    # Generate the cutting tools (spheres)
    # We calculate an offset so the sphere center is slightly outside the face,
    # resulting in a shallow spherical cut (cap) rather than a full hemisphere.
    offset = pip_radius - pip_depth
    
    # Cut spheres at each pip location
    for pt in pts:
        sphere = cq.Workplane("XY").sphere(pip_radius).translate((pt[0], pt[1], offset))
        sphere_solid = sphere.val()
        # Transform the sphere to the face workplane coordinate system
        sphere_transformed = sphere_solid.located(wp.plane.location)
        result = result.cut(sphere_transformed)

# The 'result' variable now contains the final 3D die object