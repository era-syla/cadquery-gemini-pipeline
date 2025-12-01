import cadquery as cq

# Define the geometry parameters for cross-sections at various Z heights
# The shape is defined by a stack of profiles to create the "Moai" nose/face shape.
# Format: (Z_height, Total_Width, Depth_from_back)
sections = [
    (0, 32.0, 22.0),   # Bottom base: Moderately wide and deep
    (15, 30.0, 18.0),  # Philtrum area: Slightly narrower and retracted
    (28, 38.0, 34.0),  # Nose tip: The widest and most protruding point
    (44, 22.0, 12.0),  # Bridge of nose: Distinctly narrow and shallow (indented)
    (60, 34.0, 18.0)   # Forehead/Top: Widening again
]

# Initialize the Workplane
wp = cq.Workplane("XY")

# Loop to create the stack of profiles
# We construct the right half of the object to mirror it later. 
# This ensures symmetry and creates the visible center seam line.
for i, (z, width, depth) in enumerate(sections):
    # Calculate the relative Z offset from the previous plane
    # If it's the first section, offset is just its Z height (usually 0)
    offset = z if i == 0 else z - sections[i-1][0]
    
    # Create a new workplane relative to the current one
    wp = wp.workplane(offset=offset)
    
    # Define dimensions for the half-profile
    w_half = width / 2.0
    
    # Define points for the profile:
    # 1. Center Back (on the axis of symmetry)
    # 2. Corner Back (width edge)
    # 3. Front Tip (depth edge, axis of symmetry)
    p_center_back = (0, 0)
    p_corner_back = (w_half, 0)
    p_front_tip = (0, depth)
    
    # Define a control point for the arc to give the nose its bulbous shape.
    # A weighted midpoint between the corner and tip works well for this organic form.
    p_arc_mid = (w_half * 0.65, depth * 0.65)
    
    # Draw the wire for this section
    # The shape is effectively a "D" cut in half: straight back, curved side/front.
    wp = (wp
          .moveTo(*p_center_back)
          .lineTo(*p_corner_back)
          .threePointArc(p_arc_mid, p_front_tip)
          .close()  # Closes back to p_center_back, creating the center seam line
          )

# Loft through all the generated profiles to create the right half of the solid
right_half = wp.loft()

# Mirror the right half across the YZ plane (X=0) and union to form the complete object
result = right_half.union(right_half.mirror("YZ"))