import cadquery as cq

# --- Dimensions & Parameters ---
cyl_od = 16.0          # Outer diameter of battery holder
cyl_id = 14.0          # Inner diameter
cyl_height = 35.0      # Height of the block
floor_thickness = 2.0  # Thickness of the bottom floor
pitch = 15.5           # Distance between centers (slightly less than OD for wall fusion)
text_depth = 1.5       # How much the text protrudes
text_size = 12.0       # Font size
block_gap = 4.0        # Gap between the two blocks

# --- Helper Function to Create Battery Block ---
def create_battery_block(num_cols, label):
    # Generate grid points for cylinders (2 rows x num_cols)
    # Row 0 is Front (Y=0), Row 1 is Back (Y=pitch)
    pts = []
    for r in range(2):
        for c in range(num_cols):
            pts.append((c * pitch, r * pitch))
            
    # 1. Create Base Geometry
    # Use a Sketch to define the overlapping circles and fuse them in 2D
    s = cq.Sketch().push(pts).circle(cyl_od / 2.0)
    body = cq.Workplane("XY").placeSketch(s).extrude(cyl_height)
    
    # 2. Cut Holes
    # Select top face, push points, cut blind holes
    body = (body.faces(">Z")
            .workplane()
            .pushPoints(pts)
            .hole(cyl_id, depth=cyl_height - floor_thickness))
            
    # 3. Add Chamfer to Top Edges
    # Improves look and printability
    try:
        body = body.faces(">Z").edges().chamfer(0.5)
    except:
        # Fallback if topology is complex, though standard circles usually work
        pass

    # 4. Add Text
    # Calculate geometric center of the block's front face
    center_x = (num_cols - 1) * pitch / 2.0
    center_z = cyl_height / 2.0
    
    # Position text plane slightly in front of the cylinders
    # Front tangent of cylinder is at Y = -cyl_od/2
    # We position plane at Y = -cyl_od/2 - text_depth (outer surface of text)
    # Then extrude back into the object
    text_face_y = -cyl_od / 2.0 - text_depth
    
    text_obj = (cq.Workplane("XZ")
                .workplane(offset=text_face_y) # Offset in Y direction (XZ normal)
                .center(center_x, center_z)
                .text(label, fontsize=text_size, distance=text_depth + 1.0, 
                      halign="center", valign="center")
               )
    
    # Union text with body
    return body.union(text_obj)

# --- Create Components ---

# 1. Left Block ("EMPTY") - 4 columns
left_block = create_battery_block(4, "EMPTY")

# 2. Right Block ("FULL") - 3 columns
right_block = create_battery_block(3, "FULL")

# 3. Position Right Block
# Calculate the X offset to place the right block after the left block with a gap
# Left block max X extents approx: (3 * pitch) + (cyl_od / 2)
# Right block min X extents: offset - (cyl_od / 2)
# Gap = Right_min - Left_max
# Offset = Left_max + Gap + cyl_od/2
offset_x = (3 * pitch) + cyl_od + block_gap
right_block = right_block.translate((offset_x, 0, 0))

# 4. Create Hinge/Bridge Connection
# Connects the two blocks in the valley between rows
bridge_y = pitch / 2.0
bridge_x_start = (3 * pitch) + (cyl_od / 2.0) - 1.0 # 1mm overlap into left
bridge_x_end = offset_x - (cyl_od / 2.0) + 1.0      # 1mm overlap into right
bridge_width = bridge_x_end - bridge_x_start
bridge_center_x = bridge_x_start + bridge_width / 2.0

# Rectangular connector
bridge = (cq.Workplane("XY")
          .center(bridge_center_x, bridge_y)
          .rect(bridge_width, 2.0) # 2mm thick connection
          .extrude(cyl_height)
         )

# Add a cylindrical hinge detail in the center of the gap
hinge_center_x = (3 * pitch) + (cyl_od / 2.0) + (block_gap / 2.0)
hinge = (cq.Workplane("XY")
         .center(hinge_center_x, bridge_y)
         .circle(block_gap / 1.5) # Small cylinder filling the gap
         .extrude(cyl_height)
        )

# --- Final Assembly ---
result = left_block.union(right_block).union(bridge).union(hinge)