import json
import os
from pycocotools.coco import COCO

'''
This code will help you to extract annotations which you want to pick up.
You can freely select annotations with `list of file names` from original json file.
'''


# Step / Set paths
path_source_annotations = "../../Media/v0/valid/annotations" # TODO;
path_target_annotations = "../../Media/v0/valid/blade/annotations" # TODO;
path_target_images = "../../Media/v0/valid/blade/images" # TODO;


# Step / Set file names
old_ann_filename = 'coco_annotations.json' # TODO;
new_ann_filename = 'coco_annotations.json' # TODO;


# Step / Open json file
with open(path_source_annotations + '/' + old_ann_filename, 'r') as jf:
    json_data = json.load(jf)
# Check : Print out all the keys in json_data (You can easily see the structure of json file)
dict_keys = json_data.keys()
print(dict_keys)



# Step / Split json : Dictionaries of images, and annotations (It is useful to handle each part of json file)
js_dicts_categories = json_data['categories']
js_dicts_images = json_data['images']
js_dicts_annotations = json_data['annotations']



# Step / Just copy the original file first
js_dicts_new = json_data


# Step / Overlap the file contents
js_dicts_new['categories'] = js_dicts_categories # Will be maintained
js_dicts_new['images'] = []
js_dicts_new['annotations'] = []


# Step / Create inversed dictionaries with "image_id"
ids_dict_with_file_names = {}
for dict in js_dicts_images:
    key = dict['file_name']
    value = dict['id']
    ids_dict_with_file_names[key] = value


# Step / Returns lists of the file names
list_images = os.listdir(path_target_images)


# Step / Use coco api with old annotation file
coco = COCO(path_source_annotations + "/" + old_ann_filename)

# Step / Extract the annotations you want
for file_name in list_images:

    image_id = ids_dict_with_file_names[file_name]
    ann_ids = coco.getAnnIds(imgIds=image_id)
    anns = coco.loadAnns(ann_ids) 

    img_dict = {

    }
    js_dicts_new['images'].append(img_dict)

    # Create new objects that are augmented
    for ann in anns:
        js_dicts_new['annotations'].append(ann)



# Step / Write down a new josn annotations file # TODO;
with open(path_target_annotations + "/" + new_ann_filename, 'w', encoding='utf-8') as ef:
    json.dump(js_dicts_new, ef, ensure_ascii=False, indent="\t")