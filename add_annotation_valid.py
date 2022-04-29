import os
import json
from pycocotools.coco import COCO


'''
################################################
##### Description : What is this code for? #####
################################################

This code will help you to add a `farm` information into original annotation file.
Before start this task, you need to know prefix information of images.
For example, img_0001.jpg ~ img_2000.jpg are taken from offshore farm, and
img_2001.jpg img_4000.jpg are taken from mountain farm.

###########################
##### Detailed Guide  #####
###########################



'''



# Path for images, and annotations 
path_source_images = "../../Media/v0/valid/images" 
path_source_annotations = "../../Media/v0/valid/annotations"



# Step / Open the original json annotations file
old_ann_filename = 'coco_annotations.json' # TODO;
with open(path_source_annotations + '/' + old_ann_filename, 'r') as jf:
    json_data = json.load(jf)
# Check : Print out all the keys in json_data (You can easily see the structure of json file)
dict_keys = json_data.keys()
print(dict_keys)


# Split json : Dictionaries of images, and annotations (It is useful to handle each part of json file)
js_dicts_images = json_data['categories']
js_dicts_images = json_data['images']
js_dicts_annotations = json_data['annotations']
print("number of original annotations : ", len(js_dicts_annotations))



# Step / We want to create a new annotations file extracted from the original annotations file
new_ann_filename = 'farm_coco_annotations.json' # TODO;



# Step / Prepare the new json file as a base structure, to modify it
# Just copy it first
js_dicts_new = json_data



# Returns lists of the file names
list_images = os.listdir(path_source_images)



# Define img & annotation id
img_id = 1

new_img_info = []

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
        
    # Load img dict with image_id
    image_dict = coco.loadImgs(image_id)

    # Get prefix of file_name
    prefix = file_name.split('_')[0]

    if prefix == '191228':
        image_dict[0]['farm'] = 'Gasiri'
    elif prefix == '200121':
        image_dict[0]['farm'] = 'Gyeongju'
    elif prefix == '191107':
        image_dict[0]['farm'] = 'Siwha'
    elif prefix == '200706':
        image_dict[0]['farm'] = 'Honam'

    assert len(image_dict[0]) == 5 # Check whether the image has farm information

    new_img_info.append(image_dict[0])
    img_id += 1 


    

js_dicts_new['images'] = new_img_info



# # Step / Write down a new josn annotations file # TODO;
with open(path_source_annotations + "/" + new_ann_filename, 'w', encoding='utf-8') as ef:
    json.dump(js_dicts_new, ef, ensure_ascii=False, indent="\t")