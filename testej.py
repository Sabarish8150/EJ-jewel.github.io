import rhinoscriptsyntax as rs
import math

def get_grade(value, grade_type):
    """
    Function to calculate the grade based on weight or pieces.
    """
    grade_ranges = {
        "weight": {
            (0, 1.99): 0.2,
            (2, 3.99): 0.4,
            (4, 5.99): 0.6,
        },
        "pieces": {
            (0, 10): 0.1,
            (10, 20): 0.25,
            (20, 30): 0.4,
        }
    }
    
    for range_key, grade in grade_ranges[grade_type].items():
        if range_key[0] <= value <= range_key[1]:
            return grade
    return 0

def calculate_area_without_stones():
    # Get selected objects (design and stones)
    selected_objects = rs.GetObject("Select the jewelry design object", rs.filter.surface | rs.filter.polysurface)
    if not selected_objects:
        return "No object selected."

    stones = rs.GetObject("Select the stones (or multiple stones)", rs.filter.surface | rs.filter.polysurface)
    if not stones:
        return "No stones selected."

    # Calculate the total area of the jewelry design (without stones)
    design_area = rs.SurfaceArea(selected_objects)[0] if rs.IsSurface(selected_objects) else rs.PolySurfaceArea(selected_objects)[0]
    
    # Initialize the total area of the stones
    total_stone_area = 0

    # Loop through selected stones and calculate their total area
    if isinstance(stones, list):  # If multiple stones are selected
        for stone in stones:
            stone_area = rs.SurfaceArea(stone)[0] if rs.IsSurface(stone) else rs.PolySurfaceArea(stone)[0]
            total_stone_area += stone_area
    else:  # If only one stone is selected
        total_stone_area = rs.SurfaceArea(stones)[0] if rs.IsSurface(stones) else rs.PolySurfaceArea(stones)[0]

    # Calculate the remaining area (without stones)
    remaining_area = design_area - total_stone_area
    
    # Display the output
    report = f"Design Area: {design_area:.2f} sq.mm\n"
    report += f"Total Stone Area: {total_stone_area:.2f} sq.mm\n"
    report += f"Remaining Area (without stones): {remaining_area:.2f} sq.mm\n"
    
    # Display final report in Rhino message box
    rs.MessageBox(report)
    return report

# Run the function to calculate and display the area without stones
calculate_area_without_stones()
