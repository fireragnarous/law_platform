import json
import os
import sys
import cv2
import csv
import numpy as np
from copy import deepcopy

def trans_poly_to_bbox(poly):
    x1 = np.min([p[0] for p in poly])
    x2 = np.max([p[0] for p in poly])
    y1 = np.min([p[1] for p in poly])
    y2 = np.max([p[1] for p in poly])
    return [x1, y1, x2, y2]


def get_outer_poly(bbox_list):
    x1 = min([bbox[0] for bbox in bbox_list])
    y1 = min([bbox[1] for bbox in bbox_list])
    x2 = max([bbox[2] for bbox in bbox_list])
    y2 = max([bbox[3] for bbox in bbox_list])
    return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]

def trans_csv(image_dir, anno_dir,output_root):
    imgs = os.listdir(image_dir)
    annos = os.listdir(anno_dir)

    imgs = [img.replace(".png", "") for img in imgs]
    annos = [anno.replace(".json", "") for anno in annos]
    csv_output=[["picture_id","download_url","transcription","label","points","linking","label_id"]]
    for anno_fn in annos:
        res = []
        one_row_output=[]
        with open(os.path.join(anno_dir, anno_fn + ".json"), "r",encoding='utf-8') as fin:
            infos = json.load(fin)
            infos = infos["form"]
            old_id2new_id_map = dict()
            global_new_id = 0
            for info in infos:
                if info["text"] is None:
                    continue
                words = info["words"]
                if len(words) <= 0:
                    continue
                word_idx = 1
                curr_bboxes = [words[0]["box"]]
                curr_texts = [words[0]["text"]]
                while word_idx < len(words):
                    # switch to a new link
                    if words[word_idx]["box"][0] + 10 <= words[word_idx - 1][
                            "box"][2]:
                        if len("".join(curr_texts[0])) > 0:
                            res.append({
                                "transcription": " ".join(curr_texts),
                                "label": info["label"],
                                "points": get_outer_poly(curr_bboxes),
                                "linking": info["linking"],
                                "id": global_new_id,
                            })
                            if info["id"] not in old_id2new_id_map:
                                old_id2new_id_map[info["id"]] = []
                            old_id2new_id_map[info["id"]].append(global_new_id)
                            global_new_id += 1
                        curr_bboxes = [words[word_idx]["box"]]
                        curr_texts = [words[word_idx]["text"]]
                    else:
                        curr_bboxes.append(words[word_idx]["box"])
                        curr_texts.append(words[word_idx]["text"])
                    word_idx += 1
                if len("".join(curr_texts[0])) > 0:
                    res.append({
                        "transcription": " ".join(curr_texts),
                        "label": info["label"],
                        "points": get_outer_poly(curr_bboxes),
                        "linking": info["linking"],
                        "id": global_new_id,
                    })
                    if info["id"] not in old_id2new_id_map:
                        old_id2new_id_map[info["id"]] = []
                    old_id2new_id_map[info["id"]].append(global_new_id)
                    global_new_id += 1
            res = sorted(
                res, key=lambda r: (r["points"][0][1], r["points"][0][0]))
            for i in range(len(res) - 1):
                for j in range(i, 0, -1):
                    if abs(res[j + 1]["points"][0][1] - res[j]["points"][0][1]) < 20 and \
                            (res[j + 1]["points"][0][0] < res[j]["points"][0][0]):
                        tmp = deepcopy(res[j])
                        res[j] = deepcopy(res[j + 1])
                        res[j + 1] = deepcopy(tmp)
                    else:
                        break
            # re-generate unique ids
            for idx, r in enumerate(res):
                new_links = []
                for link in r["linking"]:
                    # illegal links will be removed
                    if link[0] not in old_id2new_id_map or link[
                            1] not in old_id2new_id_map:
                        continue
                    for src in old_id2new_id_map[link[0]]:
                        for dst in old_id2new_id_map[link[1]]:
                            new_links.append([src, dst])
                res[idx]["linking"] = deepcopy(new_links)
            for i in range (len(res) - 1):
                one_row_output=[]
                one_row_output.append(anno_fn)
                one_row_output.append(os.path.join(os.path.abspath(image_dir)+"\\"+anno_fn+".png"))
                one_row_output.append(res[i]["transcription"])
                one_row_output.append(res[i]["label"])
                one_row_output.append(res[i]["points"])
                one_row_output.append(res[i]["linking"])
                one_row_output.append(res[i]["id"])
                csv_output.append(one_row_output)
    with open(output_root, 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_output)

test_image_dir = "testing_data/images/"
test_anno_dir = "testing_data/annotations/"
trans_csv(test_image_dir, test_anno_dir,"test.csv")
train_image_dir = "training_data/images/"
train_anno_dir = "training_data/annotations/"
trans_csv(train_image_dir, train_anno_dir,"train.csv")