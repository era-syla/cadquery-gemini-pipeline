import cadquery as cq

# Create the main body profile
# Coordinates are estimated based on visual proportions relative to a central hole of radius 10mm.
# The shape features a 'claw' or 'cam' like profile with two prongs on the left and a hooked arm on the right.

thickness = 12
main_hole_radius = 10
small_hole_radius = 3.5

result = (
    cq.Workplane("XY")
    # Start at the top-left area
    .moveTo(-20, 28)
    
    # Top edge: A slightly sloping straight line towards the right
    .lineTo(35, 32)
    
    # Right Arm Tip: Convex curve down to the tip
    .threePointArc((48, 28), (52, 18))
    
    # Right Cutout: Concave curve forming the underside of the right arm
    .threePointArc((42, 8), (28, -5))
    
    # Bottom Belly: Convex curve sweeping across the bottom
    .threePointArc((10, -20), (-10, -25))
    
    # Bottom Left Prong: Curve extending to the bottom-left tip
    .threePointArc((-40, -25), (-55, -18))
    
    # Left Cutout ("Mouth"): Deep concave curve between the two left prongs
    .threePointArc((-22, 0), (-58, 20))
    
    # Top Left Prong Return: Convex curve back to the start point
    .threePointArc((-45, 28), (-20, 28))
    
    .close()
    .extrude(thickness)
)

# Cut the large central bore
result = (
    result.faces(">Z").workplane()
    .circle(main_hole_radius)
    .cutThruAll()
)

# Cut the smaller secondary hole
# Positioned roughly at the 4-5 o'clock position relative to the main hole
result = (
    result.faces(">Z").workplane()
    .center(14, -8)
    .circle(small_hole_radius)
    .cutThruAll()
)

# Apply a small chamfer to the top and bottom edges to match the rendered look
# Using a small value to ensure it doesn't consume the sharp tips
try:
    result = result.edges("|Z").chamfer(0.5)
except Exception:
    # Fallback if geometry is too complex for chamfer at tips
    pass