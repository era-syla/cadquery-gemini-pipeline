import cadquery as cq
import math

def create_spur_gear():
    # -------------------------------------------------------------------------
    # Parameters
    # -------------------------------------------------------------------------
    module = 1.0
    num_teeth = 90
    thickness = 5.0
    pressure_angle = 20.0
    
    # Hub and Spoke Dimensions
    hub_diameter = 26.0
    bore_diameter = 8.0
    rim_radial_thickness = 4.0  # Solid material thickness below the tooth root
    spoke_width = 5.0
    num_spokes = 8
    
    # Mounting Holes
    mounting_hole_diameter = 2.5
    mounting_hole_bcd = 17.0  # Bolt Circle Diameter
    
    # -------------------------------------------------------------------------
    # Calculations
    # -------------------------------------------------------------------------
    pitch_diameter = module * num_teeth
    outer_diameter = pitch_diameter + 2 * module
    root_diameter = pitch_diameter - 2.5 * module
    
    pitch_radius = pitch_diameter / 2.0
    outer_radius = outer_diameter / 2.0
    root_radius = root_diameter / 2.0
    
    # The inner radius of the rim (where spokes connect)
    rim_inner_radius = root_radius - rim_radial_thickness
    hub_radius = hub_diameter / 2.0
    
    # -------------------------------------------------------------------------
    # 1. Generate Gear Profile (Trapezoidal Approximation)
    # -------------------------------------------------------------------------
    # We generate a point list for a simplified gear tooth profile
    points = []
    angle_step = 2 * math.pi / num_teeth
    half_pitch_angle = (math.pi / num_teeth)
    
    # Factors to define tooth shape (Trapezoid)
    # Adjust these to change the tooth profile steepness
    tip_factor = 0.4 
    root_factor = 1.6 
    
    for i in range(num_teeth):
        theta = i * angle_step
        
        # Calculate angles for the four corners of a trapezoidal tooth
        theta_root_left = theta - (half_pitch_angle * root_factor) / 2
        theta_tip_left = theta - (half_pitch_angle * tip_factor) / 2
        theta_tip_right = theta + (half_pitch_angle * tip_factor) / 2
        theta_root_right = theta + (half_pitch_angle * root_factor) / 2
        
        # Add points (Counter-Clockwise)
        points.append((root_radius * math.cos(theta_root_left), root_radius * math.sin(theta_root_left)))
        points.append((outer_radius * math.cos(theta_tip_left), outer_radius * math.sin(theta_tip_left)))
        points.append((outer_radius * math.cos(theta_tip_right), outer_radius * math.sin(theta_tip_right)))
        points.append((root_radius * math.cos(theta_root_right), root_radius * math.sin(theta_root_right)))

    # Create the main solid gear blank with teeth
    gear_solid = (cq.Workplane("XY")
                  .polyline(points)
                  .close()
                  .extrude(thickness))

    # -------------------------------------------------------------------------
    # 2. Create Internal Cutouts (Windows between spokes)
    # -------------------------------------------------------------------------
    # We create a "Ring" representing the empty space area, and subtract "Spokes" from it
    # to get the shape of the windows.
    
    # Create the annulus (ring) solid
    # Outer radius is the rim inner edge, Inner radius is the hub
    cutter_ring = (cq.Workplane("XY")
                   .circle(rim_inner_radius)
                   .circle(hub_radius)
                   .extrude(thickness))
    
    # Create the Spoke structure to mask the ring
    # We use rectangles spanning the full diameter to ensure alignment
    
    # We need num_spokes / 2 rectangles because each rectangle creates 2 spokes
    num_rects = int(num_spokes / 2)
    angle_per_rect = 360 / num_spokes
    
    base_rect = (cq.Workplane("XY")
                 .rect(outer_diameter * 1.2, spoke_width)
                 .extrude(thickness))
                 
    # Combine rotated rectangles
    spoke_structure = base_rect
    for i in range(1, num_rects):
        rotated_rect = (cq.Workplane("XY")
                       .rect(outer_diameter * 1.2, spoke_width)
                       .extrude(thickness)
                       .rotate((0,0,0), (0,0,1), i * angle_per_rect))
        spoke_structure = spoke_structure.union(rotated_rect)
        
    # The windows are the parts of the ring NOT covered by spokes
    windows = cutter_ring.cut(spoke_structure)
    
    # Cut the windows from the main gear
    result_geo = gear_solid.cut(windows)
    
    # -------------------------------------------------------------------------
    # 3. Create Holes (Center Bore and Mounting Holes)
    # -------------------------------------------------------------------------
    # Center Bore
    result_geo = result_geo.faces(">Z").workplane().hole(bore_diameter)
    
    # Mounting Holes (Pattern of 4)
    # We align them with the axes (0, 90, 180, 270)
    result_geo = (result_geo.faces(">Z")
                  .workplane()
                  .polarArray(mounting_hole_bcd / 2, 0, 360, 4)
                  .hole(mounting_hole_diameter))
                  
    return result_geo

# Generate the model
result = create_spur_gear()