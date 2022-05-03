import json


'''
This code will help you to edit a wrong json file into right one.
You can freely modify your json file. Here, we changed segmentation information.
'''


# Step / Set paths
path_source_annotations = "../../Media/v0/valid/annotations" # TODO;
path_dest_annotations = "../../Media/v0/valid/annotations" # TODO;



# Step / Open the original json annotations file
old_ann_filename = 'coco_annotations.json' # TODO;
# Step / We want to create a new annotations file
new_ann_filename = 'seg_coco_annotations.json' # TODO;


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
js_dicts_new['categories'] = js_dicts_categories
js_dicts_new['images'] = js_dicts_images
js_dicts_new['annotations'] = []


# Step / Modify annotation sections
for dict in js_dicts_annotations:
    # Modify information
    segmentation = [dict["segmentation"]]
    dict["segmentation"] = segmentation
    # Append new dictionary
    js_dicts_new['annotations'].append(dict)


js_dicts_new['annotations'] = js_dicts_annotations


# Step / Write down a new josn annotations file # TODO;
with open(path_dest_annotations + "/" + new_ann_filename, 'w', encoding='utf-8') as ef:
    json.dump(js_dicts_new, ef, ensure_ascii=False, indent="\t")