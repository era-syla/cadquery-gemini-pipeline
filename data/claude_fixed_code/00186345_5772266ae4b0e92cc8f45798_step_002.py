import cadquery as cq

# --- Parameters & Dimensions ---
# Coordinates of the three pivots (based on visual estimation)
p1 = (0, 0)          # Bottom Center Pivot (Main)
p2 = (-40, 55)       # Top Left Pivot
p3 = (55, 25)        # Right Pivot

# Radii for the cylindrical bosses
radius_boss_main = 14.0
radius_boss_sub = 10.0

# Radii for the through holes
radius_hole_main = 9.0
radius_hole_sub = 6.0

# Thicknesses
thickness_boss_main = 30.0  # Main pivot width
thickness_boss_sub = 22.0   # Secondary pivots width
thickness_plate = 12.0      # Main structural arm thickness
pocket_depth = 2.5          # Depth of weight-saving recesses
rim_width = 3.5             # Width of the rim (flange) around edges
cutout_fillet = 5.0         # Fillet radius for internal truss cutouts

# --- 1. Base Structure Generation ---

# Helper to create a cylinder at a point
def make_cyl(point, r, h):
    return (cq.Workplane("XY")
            .center(*point)
            .circle(r)
            .extrude(h)
            .translate((0, 0, -h/2)))

# Create dummy cylinders for the plate hull generation
# We use the plate thickness for these
c1 = make_cyl(p1, radius_boss_main, thickness_plate)
c2 = make_cyl(p2, radius_boss_sub, thickness_plate)
c3 = make_cyl(p3, radius_boss_sub, thickness_plate)

# Create the main triangular body by hulling the three cylinders
# This creates the smooth tangential outer contour automatically
plate = c1.union(c2).union(c3).hull()

# --- 2. Internal Truss Cutouts ---

# Define the shapes of the holes (cutouts) inside the triangle.
# These coordinates are tuned to fit within the hull defined by p1, p2, p3
# leaving material for the ribs.
sketch_cutouts = (
    cq.Sketch()
    # Cutout 1: Left side (between p1 and p2)
    .polygon([(-6, 14), (-26, 48), (-2, 35)])
    .vertices().fillet(cutout_fillet)
    # Cutout 2: Top side (between p2 and p3)
    .polygon([(-15, 50), (35, 32), (5, 38)])
    .vertices().fillet(cutout_fillet)
    # Cutout 3: Right side (between p1 and p3)
    .polygon([(12, 8), (40, 18), (18, 26)])
    .vertices().fillet(cutout_fillet)
)

# Cut the truss holes through the plate
plate_truss = plate.cut(
    cq.Workplane("XY")
    .placeSketch(sketch_cutouts)
    .extrude(thickness_plate * 2, both=True)
)

# --- 3. Pocketing (Lightweighting Recesses) ---

# Function to create recessed pockets on a specific face.
# It uses offset2D to create a boundary 'rim_width' inside the outer edge
# and 'rim_width' away from the holes.
def add_pockets(part, face_selector):
    face_wp = part.faces(face_selector).workplane()
    
    # offset2D(-val): Shrinks outer loop, Expands inner loops (holes)
    # This leaves the rim area protected, generating a wire for the pocket area.
    pocket_wire = (
        face_wp.wires()
        .toPending()
        .offset2D(-rim_width, kind="intersection")
    )
    
    # Cut inwards (negative extrusion relative to face normal)
    return part.cut(pocket_wire.extrude(-pocket_depth))

# Apply pockets to top and bottom faces
part_pocketed = add_pockets(plate_truss, ">Z")
part_pocketed = add_pockets(part_pocketed, "<Z")

# --- 4. Bosses and Holes ---

# Create the full-width bosses
boss1 = make_cyl(p1, radius_boss_main, thickness_boss_main)
boss2 = make_cyl(p2, radius_boss_sub, thickness_boss_sub)
boss3 = make_cyl(p3, radius_boss_sub, thickness_boss_sub)

# Combine plate and bosses
structure = part_pocketed.union(boss1).union(boss2).union(boss3)

# Drill the pivot holes
result = (
    structure
    .faces(">Z").workplane()
    # Hole 1
    .center(*p1).circle(radius_hole_main).cutThruAll()
    # Hole 2 (relative move)
    .center(p2[0]-p1[0], p2[1]-p1[1]).circle(radius_hole_sub).cutThruAll()
    # Hole 3 (relative move)
    .center(p3[0]-p2[0], p3[1]-p2[1]).circle(radius_hole_sub).cutThruAll()
)

# --- 5. Final Details ---

# Add chamfers to the pivot holes for a finished look
# Select edges by Circle type and apply chamfer
result = (
    result
    .edges("%Circle")
    .chamfer(0.5)
)