import numpy as np

def distance_btw_point_and_line(pos_point, pos_line_1, pos_line_2):
    '''
    Computes the distance between a points (pos_point) and a line (defined by two points pos_line_1 and pos_line_2).
    :param pos_point: (tupple) (x,y)
    :param pos_line_1: (tupple) (x,y)
    :param pos_line_2: (tupple) (x,y)
    :return:(float) distance
    '''
    pos_line_1 = np.array(pos_line_1)
    pos_line_2 = np.array(pos_line_2)
    pos_point = np.array(pos_point)
    dist = np.abs(np.cross(pos_line_2 - pos_line_1, pos_point - pos_line_1) / np.linalg.norm(pos_line_2 - pos_line_1))
    return float(dist)


def get_lines_for_boxes(boxes, scontent):
    '''
    For each box in boxes, get the closest line.
    :param boxes: (ultralytics.engine.results.Boxes) detected boxes and associated classes
    :param scontent: (list of dict) sign content
    :return: (list of int) list containing closest line index for each box. The list idx corresponds to box idx
    '''
    idx_closest_line_per_box = []
    for box in boxes:
        x_box, y_box, _, _ = box.xywh[0]
        dist_list = []
        for lcontent in scontent: # for each line in sign
            dist = distance_btw_point_and_line((x_box, y_box), lcontent['pos_dest'], lcontent['pos_dura'])
            dist_list.append(dist)

        idx_closest_line = int(np.argmin(dist_list))
        idx_closest_line_per_box.append(idx_closest_line)
    return idx_closest_line_per_box