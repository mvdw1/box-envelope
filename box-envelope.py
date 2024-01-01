import sys
import svgwrite

px_to_mm = 3.7795275590551
perforation_color = "green"
cut_color = "red"

# create the flap for the top/bottom sides
def top_bottom_side_flap(inner_width, inner_height):
    """
    This function creates a list with points for the top/bottom flaps

    Args:
    - points: list of points
    - inner_width: desired width size
    - inner_height: desired height size

    Returns:
    list of point
    """
    # As the overlap and inset are ratios, they do not need to have a conversion here to mm
    top_flap_overlap = 5/75 # Used as reference: 5 mm overlap for a box of 75mm,
    top_flap_inset = 2/75 #  Used as reference: 2 mm inset for a box of 75mm
    points = [
        [0, 0],
        [top_flap_inset * inner_width, top_flap_overlap * inner_height],
        [inner_width / 2, inner_height / 2 + top_flap_overlap * inner_height],
        [inner_width - top_flap_inset * inner_width, top_flap_overlap * inner_height],
        [inner_width, 0]
    ]
    return points

# create the flap for the left/right sides
def left_right_side_flap(inner_width, inner_height):
    """
    This function creates a list with points for the side flaps

    Args:
    - points: list of points
    - inner_width: desired width size
    - inner_height: desired height size

    Returns:
    list of point
    """
    top_flap_overlap = 5/50 # Used as reference: 5 mm overlap for a box of 50mm
    top_flap_inset = 0/5 # Used as reference: 0 mm inset for a box of 50
    points = [
        [0, 0],
        [top_flap_overlap * inner_height, top_flap_inset * inner_width],
        [top_flap_overlap * inner_height+inner_width/2, inner_height/2],
        [top_flap_overlap * inner_height, inner_height - top_flap_inset * inner_width],
        [0, inner_height]
    ]
    return points

def move(points, x,y):
    """
    This function moves the points by x and y

    Args:
    - points: list of points
    - x: x to move
    - y: y to move

    Returns:
    list of moved points
    """
    for point in points:
        point[0] = point[0] + x
        point[1] = point[1] + y
    return points


def mirror(points, x,y):
    """
    This function can mirror the points in x and/or y

    Args:
    - points: list of points
    - x: True to mirror x value (e.g. mirror in y-axis). False won't adapt x values
    - y: True to mirror y value (e.g. mirror in x-axis). False won't adapt y values

    Returns:
    list of adapted points
    """
    for point in points:
        if(x):
            point[0] = -point[0]
        if(y):
            point[1] = -point[1] 
    return points

def draw_envelope(box_width_mm, box_height_mm, box_depth_mm, with_tabs, filename):
    """
    This function draws an envelope for the specified box and saves it

    Args:
    - box_width_mm: the width of the box in mm
    - box_height_mm: the height of the box in mm
    - box_depth_mm: the depth of the box in mm
    - filename: the filename to use
    """
    global px_to_mm
    # Convert millimeters to pixels (assuming 1mm = 3.7795275590551 pixels)
    box_width = box_width_mm *px_to_mm
    box_height = box_height_mm * px_to_mm
    box_depth = box_depth_mm * px_to_mm
    # 
    total_width = box_width + box_depth * 2
    total_height = box_height + box_depth * 2

    dwg = svgwrite.Drawing(filename, profile="tiny")

    # Calculate position and size for the inner square
    inner_width = box_width
    inner_height = box_height
    x_offset = (total_width - inner_width) / 2
    y_offset = (total_height - inner_height) / 2

    # The inner and outer square (perforation)
    dwg.add(dwg.rect(insert=(0, 0), size=(total_width, total_height), fill='none', stroke = perforation_color))
    dwg.add(dwg.rect(insert=(x_offset, y_offset), size=(inner_width, inner_height), fill='none', stroke = perforation_color))

    # Envelope
    # top flap
    points1 = top_bottom_side_flap(inner_width, inner_height)
    points1 = move(points1, box_depth,0)
    points1 = mirror(points1, False, True )

    # Not a ratio here: convert desires size of tab to px
    tab_width = 10*px_to_mm
    tab_offset = 2*px_to_mm

    points_corner12 = []
    if (with_tabs):
        start_point =[inner_width+box_depth,0]
        end_point = [inner_width+box_depth, box_depth]
        points_corner12 = [[start_point[0]+tab_width, start_point[1]+ tab_offset],[start_point[0]+tab_width, end_point[1]-tab_offset],[end_point[0], end_point[1]]]
        dwg.add(dwg.line(start=start_point,end=end_point, stroke=perforation_color))
    else:
        points_corner12 = [[inner_width+box_depth, box_depth]]

    # right flap
    points2 = left_right_side_flap(inner_width, inner_height)
    points2 = move(points2, total_width,box_depth)
    points2 = mirror(points2, False, False )
    points_corner23 = []
    if (with_tabs):
        start_point =[inner_width+box_depth, inner_height+box_depth]
        end_point = [inner_width+box_depth, inner_height+box_depth*2]
        points_corner23 = [start_point,[start_point[0]+tab_width, start_point[1]+ tab_offset],[start_point[0]+tab_width, end_point[1]-tab_offset],[end_point[0], end_point[1]]]
        dwg.add(dwg.line(start=start_point,end=end_point, stroke=perforation_color))
    else:
        points_corner23 = [[inner_width+box_depth, inner_height+box_depth]]

    # bottom flap
    points3 = top_bottom_side_flap(inner_width, inner_height)
    points3 = mirror(points3, True, False )
    points3 = move(points3, box_depth+inner_width,total_height)
    points3 = mirror(points3, False, False )
    points_corner34 = []
    if (with_tabs):
        start_point =[box_depth, inner_height+box_depth*2]
        end_point = [box_depth, inner_height+box_depth]
        points_corner34 = [[start_point[0]-tab_width, start_point[1]- tab_offset],[start_point[0]-tab_width, end_point[1]+tab_offset],[end_point[0], end_point[1]]]
        dwg.add(dwg.line(start=start_point,end=end_point, stroke=perforation_color))
    else:
        points_corner34 = [[box_depth, inner_height+box_depth]]



    # left flap
    points4 = left_right_side_flap(inner_width, inner_height)
    points4 = mirror(points4, True, True )
    points4 = move(points4, 0,box_depth+inner_height)


    points_corner41 = []
    if (with_tabs):
        start_point =[box_depth, box_depth]
        end_point = [box_depth, 0]
        points_corner41 = [start_point, [start_point[0]-tab_width, start_point[1]- tab_offset],[start_point[0]-tab_width, end_point[1]+tab_offset],[end_point[0], end_point[1]]]
        dwg.add(dwg.line(start=start_point,end=end_point, stroke=perforation_color))
    else:
        points_corner41 = [[box_depth, box_depth]]


    point_cornerlast = [points1[0]]
    points_all = points1 + points_corner12 + points2 + points_corner23 + points3 + points_corner34 + points4 + points_corner41 + point_cornerlast

    # Convert polyline to a path
    path = dwg.path(d='M {} {}'.format(*points_all[0]), fill='none', stroke=cut_color)  # Start the path at the first point

    # Create the path string
    for point in points_all[1:]:
        path.push('L', *point)  # Append line-to commands to the path

    # Add path to svg
    dwg.add(path)

    # Save the SVG document
    dwg.save()

if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("usage: {sys.argv[0]} width height depth tabs [filename]\n with width, height, depth as size in mm, with_tabs 0/1, and optionally output filename")
    else:
        box_width = float(sys.argv[1])
        box_height = float(sys.argv[2])
        box_depth = float(sys.argv[3])
        with_tabs = float(sys.argv[4])
        filename = "envelope.svg"
        if len(sys.argv) == 6:
            filename = sys.argv[5]
        draw_envelope(box_width, box_height, box_depth, with_tabs, filename)
        
        print(f"Envelope for box with dimensions h:{box_height} w:{box_width} d:{box_depth} created and stored as {filename}")
