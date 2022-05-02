import os
import json
from pycocotools.coco import COCO
import ast

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
path_source_images = "../../Media/v0/train/images" 
path_source_annotations = "../../Media/v0/train/annotations"



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
new_ann_filename = 'weather_coco_annotations.json' # TODO;



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

    image_file_name = file_name.split('.')[:-1]
    prefix0 = image_file_name[0]

    if len(image_file_name) > 1:
        prefix0 = ast.literal_eval(prefix0)
        if prefix0 >= 1560210000 and prefix0 <= 1560330000: # Taegisan
            image_dict[0]['weather'] = 'Sunny'
        elif prefix0 >= 1560730000 and prefix0 <= 1560760998: # Gyeongju
            image_dict[0]['weather'] = 'Sunny'
        elif prefix0 >= 1560818133 and prefix0 <= 1560824365: # Gyeongju
            image_dict[0]['weather'] = 'Cloudy'
        elif prefix0 >= 1560826336 and prefix0 <= 1560840000: # Gyeongju
            image_dict[0]['weather'] = 'Sunny'
        elif prefix0 >= 1560990000 and prefix0 <= 1561000000: # Yongdaeri
            image_dict[0]['weather'] = 'Sunny'
        elif prefix0 >= 1561330000 and prefix0 <= 1561450000: # Gimnyeong
            image_dict[0]['weather'] = 'Sunny'
        elif prefix0 >= 1561600000 and prefix0 <= 1561620000: # Hamada
            image_dict[0]['weather'] = 'Cloudy'
        elif prefix0 >= 1666290000 and prefix0 <= 1666790000: # Yongdaeri
            image_dict[0]['weather'] = 'Sunny'
    else:
        prefix1 = prefix0.split('_')
        if len(prefix1) == 3:
            if prefix1[0] == '191030': # Gagosima
                image_dict[0]['weather'] = 'Sunny'
            elif prefix1[0] == '191112': # Tamla
                image_dict[0]['weather'] = 'Sunny'
            # elif prefix1[0] == '200130':
            #     image_dict[0]['farm'] = 'Whitecreek'
            elif prefix1[0] == '200121': # Gyeongju
                image_dict[0]['weather'] = 'Sunny'
            elif prefix1[0] == '200122': # Gyeongju
                image_dict[0]['weather'] = 'Cloudy'
            elif prefix1[0] == '200620': # Uljin
                image_dict[0]['weather'] = 'Sunny'

        elif len(prefix1) == 2:
            prefix2 = prefix1[1]
            prefix2 = int(prefix2)
            if prefix2 >= 17634 and prefix2 <= 24564: # Hangwon
                image_dict[0]['weather'] = 'Sunny'
            elif prefix2 <= 32433:
                image_dict[0]['weather'] = 'Cloudy'
            elif prefix2 >= 33099 and prefix2 <= 35625: # Yongdaeri
                image_dict[0]['weather'] = 'Snow'
            elif prefix2 >= 36009 and prefix2 <= 36371: # Yongdaeri
                image_dict[0]['weather'] = 'Sunny'
            elif prefix2 == 19064: # Yongdaeri
                image_dict[0]['weather'] = 'Snow'

        elif len(prefix1) == 1:
            prefix2 = int(prefix1[0])
            # if prefix2 >= 55535 and prefix2 <= 67334: # Gyeongju
            if prefix2 >= 55535 and prefix2 <= 56362:
                image_dict[0]['weather'] = 'Sunny'
            elif prefix2 <= 56861: 
                image_dict[0]['weather'] = 'Cloudy'
            elif prefix2 <= 61748: 
                image_dict[0]['weather'] = 'Sunny'
            elif prefix2 <= 64269: 
                image_dict[0]['weather'] = 'Cloudy'
            elif prefix2 <= 65231:
                image_dict[0]['weather'] = 'Sunny'
            elif prefix2 <= 66354:
                image_dict[0]['weather'] = 'Cloudy'
            elif prefix2 <= 67334:
                image_dict[0]['weather'] = 'Snow'


    assert len(image_dict[0]) == 5 # Check whether the image has farm information

    new_img_info.append(image_dict[0])
    img_id += 1 


    

js_dicts_new['images'] = new_img_info



# # Step / Write down a new josn annotations file # TODO;
with open(path_source_annotations + "/" + new_ann_filename, 'w', encoding='utf-8') as ef:
    json.dump(js_dicts_new, ef, ensure_ascii=False, indent="\t")