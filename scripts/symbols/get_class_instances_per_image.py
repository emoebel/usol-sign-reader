import pandas as pd

path_annot_file = '/Users/manu/Downloads/project-3-at-2025-06-12-09-00-c3c15364.json'
path_to_csv = '/Users/manu/boulot/unit_solutions/data/annotations/bbox/class_instances_per_image.csv'

df = pd.read_json(path_annot_file)

data_list = []
for row in df.itertuples():
    # Get fname:
    fname_lstudio = row.file_upload
    fname = '-'.join(fname_lstudio.split('-')[1:])

    # Get nb of class instanes
    bbox_list = row.annotations[0]['result']

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

    for bbox in bbox_list:
        label = bbox['value']['rectanglelabels'][0]
        class_instance_nb[label] += 1

    df_dict = {'fname': fname,}
    df_dict.update(class_instance_nb)
    data_list.append(df_dict)


df_inst_per_img = pd.DataFrame(data_list)
df_inst_per_img.to_csv(path_to_csv)




