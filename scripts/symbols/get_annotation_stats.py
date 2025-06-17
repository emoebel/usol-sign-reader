import pandas as pd

# path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-11-06-45-3f6bbaaa.json'
# path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-11-10-40-e1595299.json'
path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-12-09-00-c3c15364.json'

path_to_csv = '/Users/manu/boulot/unit_solutions/data/annotations/bbox/class_instances_in_dset.csv'

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

df_dict = {
    'Class name': class_instance_nb.keys(),
    'Instance number': class_instance_nb.values(),
}
df_new = pd.DataFrame(df_dict)
df_new.to_csv(path_to_csv)


# last_row = df.tail(1)
# for row in last_row.itertuples():
#     bbox_list = row.annotations[0]['result']