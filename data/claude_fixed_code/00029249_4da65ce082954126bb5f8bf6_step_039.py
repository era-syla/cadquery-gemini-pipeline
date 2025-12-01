import cadquery as cq

def create_belt_clamp(letter):
    """
    Creates one side of the belt clamp assembly.
    :param letter: The character ('L' or 'R') to emboss on the top.
    """
    # Dimensions
    l_flat = 14.0         # Length of the lower flat section
    l_high = 18.0         # Length of the raised section
    l_total = l_flat + l_high
    width = 12.0          # Width of the part
    h_flat = 5.0          # Height of the flat section
    h_high = 13.0         # Height of the raised section
    fillet_r = 5.0        # Radius of the top back edge
    slot_w = 5.0          # Width of the internal slot
    slot_h = 9.0          # Height of the internal slot cut from bottom
    hole_dia = 5.0        # Diameter of the main side hole
    
    # 1. Base Extrusion (Side Profile)
    # Define points for the side profile on the XZ plane
    pts = [
        (0, 0),
        (l_total, 0),
        (l_total, h_high),
        (l_flat, h_high),
        (l_flat, h_flat),
        (0, h_flat)
    ]
    
    # Create the base block by extruding the profile centered along Y
    part = (cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(width/2.0, both=True))
            
    # 2. Fillet the top back edge of the raised section
    # We select the edge at the maximum X and maximum Z
    part = part.edges(cq.selectors.NearestToPointSelector((l_total, 0, h_high))).fillet(fillet_r)
    
    # 3. Countersunk Hole in the Flat Section
    # Located in the center of the flat area
    part = (part.faces(">Z").workplane()
            .center(l_flat/2, 0)
            .cboreHole(3.2, 6.5, 3.5)) # M3 Screw dimensions
            
    # 4. Vertical Slot Cutout (From Bottom)
    # This creates the "legs" for the tensioner mechanism
    part = (part.faces("<Z").workplane()
            .center(l_flat + l_high/2, 0)
            .rect(l_high, slot_w)
            .cutBlind(slot_h))
            
    # 5. Side Holes
    # Main hole for axle/pin
    hole_x = l_flat + l_high/2
    hole_z_main = 7.5
    
    part = (part.faces(">Y").workplane()
            .center(hole_x, hole_z_main)
            .hole(hole_dia))
            
    # Small locking/grub screw hole below the main hole
    hole_z_small = 3.5
    part = (part.faces(">Y").workplane()
            .center(hole_x, hole_z_small)
            .hole(2.5))
            
    # 6. Side Grooves
    # Decorative or functional groove along the bottom side
    groove_z = 2.0
    groove_h = 1.0
    
    # Front side groove
    part = (part.faces(">Y").workplane()
            .center(l_total/2, groove_z)
            .rect(l_total + 5, groove_h) # Extra length to ensure full cut
            .cutBlind(-0.5))
            
    # Back side groove
    part = (part.faces("<Y").workplane()
            .center(l_total/2, groove_z)
            .rect(l_total + 5, groove_h)
            .cutBlind(-0.5))
            
    # 7. Embossed Text
    # Rotate workplane -90 deg so text top points towards the high end (+X)
    part = (part.faces(">Z").workplane()
            .center(hole_x, 0)
            .transformed(rotate=(0, 0, -90))
            .text(letter, 8.0, -0.6))
            
    return part

# Generate the two parts
part_R = create_belt_clamp("R")
part_L = create_belt_clamp("L")

# Arrange them in the scene to match the image
# 'R' part is on the left, Flat end pointing -X (Left)
# We translate it so the high end faces the center
offset = 4.0 # Half gap

# The created part has Flat at X=0..14, High at X=14..32
# To place R on the left side facing center:
# Move it left by its total length + offset
part_R_positioned = part_R.translate((-32 - offset, 0, 0))

# 'L' part is on the right, Flat end pointing +X (Right)
# We rotate it 180 degrees so High end faces -X (Center)
part_L_positioned = part_L.rotate((0,0,0), (0,0,1), 180).translate((32 + offset, 0, 0))

# Combine into final result
result = part_R_positioned.union(part_L_positioned)