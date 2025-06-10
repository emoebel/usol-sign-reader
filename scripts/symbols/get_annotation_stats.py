import pandas as pd

path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-10-10-31-644aa820.json'

df = pd.read_json(path_annot_file)

class_instance_nb = {
    'bahnhof': 0,
    'bushof': 0,
    'schiffstation': 0,
    'zahnrad-standseilbahn': 0,
    'luftseilbahn': 0,
    'gondelbahn': 0,
    'sessellift': 0,
    'strassenbahn': 0,
    'huette': 0,
    'restaurant': 0,
    'feuerstelle': 0,
    'aussichtspunkt': 0,
    'other': 0,
}

for row in df.itertuples():
    bbox_list = row.annotations[0]['result']

    for bbox in bbox_list:
        label = bbox['value']['rectanglelabels'][0]
        class_instance_nb[label] += 1

print(class_instance_nb)