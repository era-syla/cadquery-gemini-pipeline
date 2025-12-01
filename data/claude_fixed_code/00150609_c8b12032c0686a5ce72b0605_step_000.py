import cadquery as cq

# --- Dimensions and Parameters ---
plate_width = 45.0
plate_height = 80.0
plate_thickness = 3.0

chamfer_top = 4.0
chamfer_bottom = 8.0

hole_diameter = 6.0
hole_spacing = 26.0
hole_offset_from_top = 12.0

text_content = "MACHINE"
text_size = 8.0
text_font = "Arial"

# --- Geometry Construction ---

# 1. Base Plate
# Create the main rectangular body centered at the origin
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Corner Chamfers
# Select vertical edges (parallel to Z axis) for chamfering
# Apply chamfer to top edges
top_edges = result.edges("|Z").vals()
for edge in top_edges:
    if edge.Center().y > 0:
        result = result.edges(cq.selectors.NearestToPointSelector(edge.Center())).chamfer(chamfer_top)

# Apply chamfer to bottom edges
bottom_edges = result.edges("|Z").vals()
for edge in bottom_edges:
    if edge.Center().y < 0:
        result = result.edges(cq.selectors.NearestToPointSelector(edge.Center())).chamfer(chamfer_bottom)

# 3. Mounting Holes
# Locate the position for holes. Top edge is at Y = plate_height / 2.
hole_y_pos = (plate_height / 2) - hole_offset_from_top

# Select the top face, create a workplane, push points, and cut holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_spacing / 2, hole_y_pos),
        (hole_spacing / 2, hole_y_pos)
    ])
    .hole(hole_diameter)
)

# 4. Top Text Feature
# Create the text as a separate solid object first.
# It is extruded in Z to match the plate thickness.
text_obj = cq.Workplane("XY").text(
    text_content,
    text_size,
    plate_thickness,
    font=text_font,
    kind="bold"
)

# Calculate the position to move the text to.
# Text is generated centered at (0,0).
# We shift it up so it sits on the top edge of the plate.
# We include a small overlap to ensure a solid boolean union.
overlap = 0.5
text_shift_y = (plate_height / 2) + (text_size / 2) - overlap

# Apply translation
text_obj = text_obj.translate((0, text_shift_y, 0))

# Union the text with the main plate
result = result.union(text_obj)