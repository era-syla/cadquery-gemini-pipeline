import cadquery as cq

# Parameters for the dish geometry
diameter = 100.0
radius = diameter / 2.0
flat_radius = 20.0
height_center = 1.5
height_rim = 6.0
wall_thickness = 1.0

# Define the cross-section points for the revolution
# We draw the profile in the XZ plane
# Top surface profile
p_center_top = (0, height_center)
p_flat_end = (flat_radius, height_center)
p_ridge_top = (flat_radius + 2, height_center + 2.0)
p_groove_bot = (flat_radius + 5, height_center + 1.5)
p_rim_peak = (radius - 8, height_rim)
p_rim_edge_top = (radius, 1.0)

# Bottom surface profile (offset inwards to create thickness)
p_rim_edge_bot = (radius, 0)
p_rim_peak_bot = (radius - 8, height_rim - wall_thickness)
p_groove_bot_inner = (flat_radius + 5, height_center + 1.5 - wall_thickness)
p_ridge_bot = (flat_radius + 2, height_center + 2.0 - wall_thickness)
p_flat_bot = (flat_radius, height_center - wall_thickness)
p_center_bot = (0, height_center - wall_thickness)

# Construct the profile wire
# Note: Using spline for organic curves of the rim
profile = (
    cq.Workplane("XZ")
    .moveTo(*p_center_top)
    .lineTo(*p_flat_end)
    # Create the ridge and outer rim profile
    .spline([p_ridge_top, p_groove_bot, p_rim_peak, p_rim_edge_top], includeCurrent=True)
    .lineTo(*p_rim_edge_bot)
    # Return path for the bottom surface
    .spline([p_rim_peak_bot, p_groove_bot_inner, p_ridge_bot, p_flat_bot], includeCurrent=True)
    .lineTo(*p_center_bot)
    .close()
)

# Revolve the profile to create the main dish body
main_body = profile.revolve()

# Create the small hole in the central flat area
# Positioned off-center
hole_cutter = (
    cq.Workplane("XY")
    .workplane(offset=height_center)
    .center(flat_radius * 0.75, -5)
    .circle(1.5)
    .extrude(-10)
)

# Create the notch/defect on the rim
# Positioned on the opposite side on the rim
notch_cutter = (
    cq.Workplane("XY")
    .workplane(offset=height_rim)
    .center(-radius + 5, 8)
    .circle(2.5)
    .extrude(-10)
)

# Apply the cuts to the main body
result = main_body.cut(hole_cutter).cut(notch_cutter)