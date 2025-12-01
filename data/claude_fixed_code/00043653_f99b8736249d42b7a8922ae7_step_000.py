import cadquery as cq

# Dimensions for the plates
plate_width = 80.0
plate_height = 40.0
plate_thickness = 3.0
gap = 5.0  # Gap between the plates

# Text parameters
font_size = 28.0
font_name = "Arial"  # Using standard font; a stencil font would require a specific file
text_depth = plate_thickness + 1.0  # Cut through with some margin

def create_labeled_plate(text, col_idx, row_idx):
    """
    Creates a rectangular plate with cut-out text.
    col_idx: -1 for left, 1 for right
    row_idx: 1 for top, -1 for bottom
    """
    # Calculate center position based on grid logic
    center_x = col_idx * (plate_width + gap) / 2.0
    center_y = row_idx * (plate_height + gap) / 2.0
    
    # Create the base rectangular plate
    plate = (cq.Workplane("XY")
             .box(plate_width, plate_height, plate_thickness)
             .translate((center_x, center_y, 0)))
    
    # Create the text cut-out
    # Select the top face (>Z), create a workplane, and cut text
    result_plate = (plate.faces(">Z")
                    .workplane()
                    .text(text, font_size, -text_depth, font=font_name, kind="bold", halign="center", valign="center"))
    
    return result_plate

# Generate the four plates based on the image layout
# Top-Left: DSL
plate_tl = create_labeled_plate("DSL", -1, 1)

# Top-Right: USL
plate_tr = create_labeled_plate("USL", 1, 1)

# Bottom-Left: DSR
plate_bl = create_labeled_plate("DSR", -1, -1)

# Bottom-Right: USR
plate_br = create_labeled_plate("USR", 1, -1)

# Combine all plates into a single compound object
result = plate_tl.union(plate_tr).union(plate_bl).union(plate_br)