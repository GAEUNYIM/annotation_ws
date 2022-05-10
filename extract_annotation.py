import json
import os
import shutil
from pycocotools.coco import COCO

'''
This code will help you to extract annotations which you want to pick up.
You can freely select annotations with `list of file names` from original json file.
'''


# Step / Set paths
path_source_images = "../../Media/v0/valid/images"
path_source_annotations = "../../Media/v0/valid/annotations" # TODO;

path_target_images = "../../Media/v0/valid/per_case/root/images" # TODO;

path_dest = ("../../Media/v0.1/valid/per_case/root")
path_dest_images = path_dest + "/images"  # TODO;
path_dest_annotations =  path_dest + "/annotations" # TODO;

os.mkdir(path_dest)
os.mkdir(path_dest_images)
os.mkdir(path_dest_annotations)

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

cnt_img = 0
cnt_ann = 0
new_img_info = []
new_annot_info = []


# Step / Create inversed dictionaries with "image_id"
ids_dict_with_file_names = {}
for dict in js_dicts_images:
    key = dict['file_name']
    value = dict['id']
    ids_dict_with_file_names[key] = value


# Step / Returns lists of the file names
target_list_images = os.listdir(path_target_images)
print("number of target images: ", len(target_list_images))

# Step / Use coco api with old annotation file
coco = COCO(path_source_annotations + "/" + old_ann_filename)

# Step / Extract the annotations you want
for file_name in target_list_images:

    # Move images into destination path
    shutil.copy(path_source_images + "/" + file_name, path_dest_images)

    # Extract annotations into new annotation file
    image_id = ids_dict_with_file_names[file_name]
    img_dict = coco.loadImgs(image_id)
    assert len(img_dict) == 1

    new_img_info.append(img_dict[0])


    ann_ids = coco.getAnnIds(imgIds=image_id)
    anns = coco.loadAnns(ann_ids) 

    # Create new objects that are augmented
    for ann in anns:
        new_annot_info.append(ann)
        cnt_ann += 1

js_dicts_new['images'] = new_img_info
js_dicts_new['annotations'] = new_annot_info

print("number of annotatios: ", cnt_ann)

# Step / Write down a new josn annotations file # TODO;
with open(path_dest_annotations + "/" + new_ann_filename, 'w', encoding='utf-8') as ef:
    json.dump(js_dicts_new, ef, ensure_ascii=False, indent="\t")