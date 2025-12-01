import cadquery as cq
import math

def naca_profile_points(chord, thickness_percent=0.12, num_points=50):
    """
    Generates a list of (x, y) coordinates for a symmetric NACA airfoil.
    
    :param chord: The chord length of the airfoil.
    :param thickness_percent: Maximum thickness as a percentage of chord (e.g., 0.12).
    :param num_points: Number of points for the upper/lower curve resolution.
    :return: List of (x, y) tuples representing the closed airfoil profile.
    """
    points = []
    t = thickness_percent
    
    # Coefficients for NACA 00xx symmetric airfoils
    a0 = 0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = 0.2843
    a4 = -0.1015

    # Generate upper surface points (Leading Edge to Trailing Edge)
    for i in range(num_points + 1):
        # Use cosine spacing for better resolution at the leading/trailing edges
        beta = (i / num_points) * math.pi
        x_norm = 0.5 * (1 - math.cos(beta)) 
        
        y_norm = 5 * t * (a0 * math.sqrt(x_norm) + 
                          a1 * x_norm + 
                          a2 * x_norm**2 + 
                          a3 * x_norm**3 + 
                          a4 * x_norm**4)
        
        points.append((x_norm * chord, y_norm * chord))
        
    # Generate lower surface points (Trailing Edge to Leading Edge)
    # Skip the last point (TE) to avoid duplicate, and stop before 0 to close manually or via loop
    for i in range(num_points - 1, 0, -1):
        beta = (i / num_points) * math.pi
        x_norm = 0.5 * (1 - math.cos(beta))
        
        y_norm = 5 * t * (a0 * math.sqrt(x_norm) + 
                          a1 * x_norm + 
                          a2 * x_norm**2 + 
                          a3 * x_norm**3 + 
                          a4 * x_norm**4)
        
        points.append((x_norm * chord, -y_norm * chord))
        
    return points

# --- Geometry Definition ---
# Estimated dimensions based on the provided image
span = 100.0         # Length of the wing section
root_chord = 60.0    # Width of the airfoil at the root
tip_chord = 30.0     # Width of the airfoil at the tip (taper ratio 0.5)
sweep_offset = 15.0  # Distance the tip is shifted back (sweep back)
airfoil_thick = 0.12 # Relative thickness (NACA 0012 style)

# 1. Generate point lists for Root and Tip profiles
root_points = naca_profile_points(root_chord, airfoil_thick)
tip_points_local = naca_profile_points(tip_chord, airfoil_thick)

# 2. Apply sweep to the tip profile
# The tip profile is shifted in the X direction relative to the root
tip_points = [(x + sweep_offset, y) for x, y in tip_points_local]

# 3. Create the Solid using a Loft operation
# We construct the root wire on the XY plane and the tip wire on a plane offset by the span in Z.
root_wire = cq.Workplane("XY").polyline(root_points).close()
tip_wire = cq.Workplane("XY").workplane(offset=span).polyline(tip_points).close()

result = cq.Workplane("XY").add(root_wire).add(tip_wire).loft()