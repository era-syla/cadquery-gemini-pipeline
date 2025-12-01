import cadquery as cq

# --- Dimensions & Parameters ---
# Based on standard US Duplex Receptacle Wall Plate dimensions
plate_width = 69.85   # ~2.75 inches
plate_height = 114.3  # ~4.5 inches
plate_thickness = 2.4 # Standard plastic plate thickness

# Duplex Cutout Geometry
# The shape is a "stadium" modified to have flat top/bottom and curved sides
# Represented as the intersection of a circle and a horizontal rectangular strip
cutout_diameter = 33.5       # Diameter of the curved side portions
cutout_flat_height = 29.2    # Distance between the top and bottom flat edges
cutout_spacing = 38.1        # Center-to-center distance between outlets (1.5 inches)

# Center Mounting Hole
screw_hole_diameter = 3.6    # Clearance for #6 screw
csk_diameter = 7.5           # Countersink diameter
csk_angle = 82               # Standard countersink angle

# --- 3D Model Construction ---

# 1. Create the Base Plate
# A simple rectangular box centered on the origin
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Define the Cutout Profile (Sketch)
# Create the specific shape of a duplex outlet opening
cutout_sketch = (
    cq.Sketch()
    .rect(cutout_diameter + 5.0, cutout_flat_height)
    .circle(cutout_diameter / 2.0, mode='i')
)

# 3. Apply the Cutouts
# Position the sketch at the two outlet locations and cut through the plate
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, cutout_spacing / 2.0), (0, -cutout_spacing / 2.0)])
    .placeSketch(cutout_sketch)
    .cutBlind(-plate_thickness * 2)
)

# 4. Create Center Screw Hole
# Add a countersunk hole in the geometric center (0,0)
result = (
    result.faces(">Z")
    .workplane()
    .cskHole(screw_hole_diameter, csk_diameter, csk_angle)
)