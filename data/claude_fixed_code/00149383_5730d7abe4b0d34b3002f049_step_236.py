import cadquery as cq
import math

# -----------------------------------------------------------------------------
# 1. Parameter Definitions
# -----------------------------------------------------------------------------
# Overall dimensions estimated from the image
od = 60.0                # Outer diameter of the component
id = 25.0                # Diameter of the central hole
height = 18.0            # Total height/thickness
wall_thickness = 4.0     # Thickness of the inner and outer cylindrical walls
pocket_floor_thick = 5.0 # Thickness of the material remaining at the bottom of pockets
bolt_circle_dia = 42.5   # Diameter of the circle on which mounting holes are placed
bolt_hole_dia = 6.0      # Diameter of the 4 mounting holes
pocket_angle = 55.0      # Angular width of the kidney-shaped pockets (degrees)
fillet_radius = 2.0      # Corner radius for the pockets

# -----------------------------------------------------------------------------
# 2. Base Geometry
# -----------------------------------------------------------------------------
# Create the main cylinder
result = cq.Workplane("XY").circle(od / 2.0).extrude(height)

# Cut the central through-hole
result = result.faces(">Z").workplane().circle(id / 2.0).cutThruAll()

# -----------------------------------------------------------------------------
# 3. Pocket Creation
# -----------------------------------------------------------------------------
# Calculations for pocket geometry constraints
r_inner_pocket = (id / 2.0) + wall_thickness
r_outer_pocket = (od / 2.0) - wall_thickness
pocket_depth = height - pocket_floor_thick

# Helper function to generate the solid tool for one pocket
def create_pocket_tool(r_in, r_out, angle, depth, fillet_r):
    # Convert angle to radians for calculations
    half_angle_rad = math.radians(angle / 2.0)
    
    # Calculate key points for the "kidney" shape centered on the X-axis
    # Inner arc start/mid/end (Counter-Clockwise)
    p_in_start = (r_in * math.cos(-half_angle_rad), r_in * math.sin(-half_angle_rad))
    p_in_mid   = (r_in, 0)
    p_in_end   = (r_in * math.cos(half_angle_rad), r_in * math.sin(half_angle_rad))
    
    # Outer arc start/mid/end (Counter-Clockwise)
    p_out_start = (r_out * math.cos(-half_angle_rad), r_out * math.sin(-half_angle_rad))
    p_out_mid   = (r_out, 0)
    p_out_end   = (r_out * math.cos(half_angle_rad), r_out * math.sin(half_angle_rad))
    
    # Draw the shape: Inner Arc -> Line to Outer -> Outer Arc (reverse) -> Close
    # We draw the outer arc from end to start to close the loop correctly
    tool = (
        cq.Workplane("XY")
        .moveTo(*p_in_start)
        .threePointArc(p_in_mid, p_in_end)     # Draw inner arc
        .lineTo(*p_out_end)                    # Line to outer radius
        .threePointArc(p_out_mid, p_out_start) # Draw outer arc back
        .close()                               # Line back to start
        .extrude(depth)
    )
    
    # Fillet the vertical edges to give rounded corners
    # Select edges parallel to Z axis ("|Z")
    tool = tool.edges("|Z").fillet(fillet_r)
    return tool

# Generate the base tool for one pocket
single_pocket = create_pocket_tool(r_inner_pocket, r_outer_pocket, pocket_angle, pocket_depth, fillet_radius)

# Create a compound of 4 pockets rotated to 45, 135, 225, 315 degrees
# The mounting holes will be at 0, 90, 180, 270, so pockets go in between.
# Start by rotating the first tool to 45 degrees
pocket_tools = single_pocket.translate((0, 0, height - pocket_depth)).rotate((0, 0, 0), (0, 0, 1), 45)

# Union the other 3 pockets
for i in range(1, 4):
    angle = 45 + (i * 90)
    pocket_tools = pocket_tools.union(
        single_pocket.translate((0, 0, height - pocket_depth)).rotate((0, 0, 0), (0, 0, 1), angle)
    )

# Cut the pockets from the main body
result = result.cut(pocket_tools)

# -----------------------------------------------------------------------------
# 4. Mounting Holes
# -----------------------------------------------------------------------------
# Create 4 mounting holes on the bolt circle, positioned at 0, 90, 180, 270 degrees
# These fall exactly between the pockets (in the "spokes")
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_dia / 2.0, 0, 360, 4)
    .circle(bolt_hole_dia / 2.0)
    .cutThruAll()
)