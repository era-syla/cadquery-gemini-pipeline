import cadquery as cq

# Object dimensions based on visual analysis
length = 100.0          # Total length of the fin/wing
tip_width = 15.0        # Width of the flat tip
max_width = 45.0        # Approximate maximum width (chord)
thickness = 6.0         # Thickness of the main plate
nose_radius = 12.0      # Fillet radius for the rounded nose
chamfer_size = 3.0      # Width of the chamfer on the leading edge
cutout_length = 15.0    # Length of the step cutout at the tip
cutout_depth = 3.0      # Depth of the cutout (half thickness)

# 1. Create the base shape
# The shape is a triangle-like polygon with a curved hypotenuse (leading edge).
# We orient the straight 'back' edge along the X-axis.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length, 0)                 # Straight back edge
    .lineTo(length, tip_width)         # Tip edge
    # Curved leading edge. Using a 3-point arc to approximate the convex curve.
    # The midpoint is chosen to bulge outwards.
    .threePointArc((length * 0.4, max_width), (0, 0))
    .close()
    .extrude(thickness)
)

# 2. Fillet the nose
# The nose is the corner at (0,0). We select the vertical edge at this location.
# nearestToPoint selects the edge closest to the specified coordinates.
result = result.edges("|Z").edges(cq.selectors.NearestToPointSelector((0, 0, thickness / 2))).fillet(nose_radius)

# 3. Chamfer the leading edge
# The leading edge is the curved edge on the top face.
# We select the top face (>Z) and then the edge closest to the curve's peak.
# The curve peak is roughly at (length*0.4, max_width).
result = result.faces(">Z").edges(cq.selectors.NearestToPointSelector((length * 0.4, max_width, thickness))).chamfer(chamfer_size)

# 4. Create the tip cutout
# This is a rectangular relief cut (step) at the tip of the object.
# We create a workplane on the top face, position a rectangle at the tip, and cut down.
cut_center_x = length - (cutout_length / 2)
result = (
    result.faces(">Z")
    .workplane()
    .center(cut_center_x, 0)
    # Rectangle width is cutout_length. Height is generous (100) to ensure it cuts 
    # through the entire width of the tip, regardless of Y alignment.
    .rect(cutout_length, 100) 
    .cutBlind(-cutout_depth)
)