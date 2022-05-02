import os
import json
from pycocotools.coco import COCO
import ast
import shutil

'''
################################################
##### Description : What is this code for? #####
################################################

This code will help you to split a directory into several sub directories according to
a specific information. During the code split sub directories, it will also create 
annotation file according to the splits.

###########################
##### Detailed Guide  #####
###########################



'''

name_dir = "Cloudy"

# Path for images, and annotations 
path_source = "../../Media/v0/valid"
path_source_images = path_source + "/images" 
path_source_annotations = path_source + "/annotations"

path_dest = "../../Media/v0/valid/per_weather"
# os.makedirs(path_dest)

path_dest_images = path_dest + "/" + name_dir + "/images"
path_dest_annotations = path_dest + "/" + name_dir + "/annotations"

os.makedirs(path_dest_images)
os.makedirs(path_dest_annotations)



# Step / Open the original json annotations file
old_ann_filename = 'weather_coco_annotations.json' # TODO;
with open(path_source_annotations + '/' + old_ann_filename, 'r') as jf:
    json_data = json.load(jf)
# Check : Print out all the keys in json_data (You can easily see the structure of json file)
dict_keys = json_data.keys()
print(dict_keys)


# Split json : Dictionaries of images, and annotations (It is useful to handle each part of json file)
js_dicts_categories = json_data['categories']
js_dicts_images = json_data['images']
js_dicts_annotations = json_data['annotations']
print("number of original annotations : ", len(js_dicts_annotations))



# Step / We want to create a new annotations file extracted from the original annotations file
new_ann_filename = 'coco_annotations.json' # TODO;



# Step / Prepare the new json file as a base structure, to modify it
# Just copy it first
js_dicts_new = json_data



# Returns lists of the file names
list_images = os.listdir(path_source_images)



# Define img & annotation id
img_id = 1
ann_id = 1
new_img_info = []
new_ann_info = []
print("number of images : ", len(list_images))



# Step / Create inversed dictionaries with "image_id"
ids_dict_with_file_names = {}

for dict in js_dicts_images:
    key = dict['file_name']

    value = dict['id']
    ids_dict_with_file_names[key] = value



# Step / COCO
coco = COCO(path_source_annotations + '/' + old_ann_filename)

for file_name in list_images:
    
    # Find the `image_id` with `file_name`
    image_id = ids_dict_with_file_names[file_name]
    ann_ids = coco.getAnnIds(image_id)
        
    # Load img dict with image_id
    image_dict = coco.loadImgs(image_id)
    ann_dicts = coco.loadAnns(ann_ids)


    if image_dict[0]['weather'] == name_dir:
        # Append img information
        new_img_info.append(image_dict[0])
        img_id += 1 

        for ann_dict in ann_dicts:
            new_ann_info.append(ann_dict)
            ann_id += 1

        shutil.copyfile(path_source_images + "/" + file_name, 
                            path_dest_images + "/" + file_name)
    

js_dicts_new['categories'] = js_dicts_categories
js_dicts_new['images'] = new_img_info
js_dicts_new['annotations'] = new_ann_info


print(img_id - 1)
print(ann_id - 1)

# # Step / Write down a new josn annotations file # TODO;
with open(path_dest_annotations + "/" + new_ann_filename, 'w', encoding='utf-8') as ef:
    json.dump(js_dicts_new, ef, ensure_ascii=False, indent="\t")