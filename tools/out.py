# from mmdet.apis import init_detector, inference_detector
from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector)

import os
from tqdm import tqdm
import json

from mmdet.utils import register_all_modules

register_all_modules()

config_file = '/project/openmmlab2/mmdet-best-practices-3.x/work_dirs/algae/convnext/cascade-mask-rcnn_convnext-t-p4-w7_fpn_4conv1fc-giou_amp-ms-crop-3x_coco/cascade-mask-rcnn_convnext-t-p4-w7_fpn_4conv1fc-giou_amp-ms-crop-3x_coco.py'
# checkpoint_file = '/project/openmmlab2/mmdet-best-practices-3.x/work_dirs/algae/convnext/cascade-mask-rcnn_convnext-t-p4-w7_fpn_4conv1fc-giou_amp-ms-crop-3x_coco/epoch_11.pth'
checkpoint_file = '/project/openmmlab2/mmdet-best-practices-3.x/work_dirs/algae/convnext/cascade-mask-rcnn_convnext-t-p4-w7_fpn_4conv1fc-giou_amp-ms-crop-3x_coco/epoch_36.pth'
device = 'cuda:0'
input_folder = "/project/openmmlab2/mmdet-best-practices-3.x/data/algae/images"
output_folder = "/project/openmmlab2/mmdet-best-practices-3.x/data/algae/outputs"
score_thr = 0.0001

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

filelist = os.listdir(input_folder)
filelist = sorted(filelist, key=lambda x: int(x[4:-4]))


# init a detector
# model = init_detector(config_file, checkpoint_file, device=device)
model = init_detector(config_file, checkpoint_file, device=device, palette='coco')
instances = []
for idx, filename in enumerate(tqdm(filelist)):
    file_path = os.path.join(input_folder, filename)
    result = inference_detector(model, file_path)
    # for cls_idx, det_boxes in enumerate(result):
    #     for box in det_boxes:
    #         box = box.astype(float)
    #         if box[-1] > score_thr:
    #             instance = {}
    #             instance['image_id'] = os.path.splitext(filename)[0]
    #             instance['category_id'] = cls_idx
    #             instance['bbox'] = [float(box[0]), float(
    #                 box[1]), float(box[2]-box[0]), float(box[3]-box[1])]
    #             # instance['bbox'] = [float((box[0]+box[2])/2),float((box[1]+box[3])/2),float(box[2]-box[0]),float(box[3]-box[1])]
    #             # instance['bbox'] = [float(box[0]),float(box[1]),float(box[2]),float(box[3])]
    #             instance['score'] = float(box[-1])
    #             instances.append(instance)


    for box,label,score in zip(list(result.pred_instances.bboxes.cpu().numpy()), list(result.pred_instances.labels.cpu().numpy()), list(result.pred_instances.scores.cpu().numpy())):

        print(box, label, score)
        instance = {}
        instance['image_id'] = os.path.splitext(filename)[0]
        instance['category_id'] = int(label)
        instance['bbox'] = [float(box[0]), float(
            box[1]), float(box[2]-box[0]), float(box[3]-box[1])]
        # instance['bbox'] = [float((box[0]+box[2])/2),float((box[1]+box[3])/2),float(box[2]-box[0]),float(box[3]-box[1])]
        # instance['bbox'] = [float(box[0]),float(box[1]),float(box[2]),float(box[3])]
        instance['score'] = float(score)
        instances.append(instance)
json.dump(instances, open('./data/1.json', 'w',
          encoding='utf-8'), ensure_ascii=False, indent=1)


# # Copyright (c) OpenMMLab. All rights reserved.
# import asyncio
# from argparse import ArgumentParser

# import mmcv

# from mmdet.apis import (async_inference_detector, inference_detector,
#                         init_detector)
# from mmdet.registry import VISUALIZERS
# from mmdet.utils import register_all_modules


# def parse_args():
#     parser = ArgumentParser()
#     parser.add_argument('img', help='Image file')
#     parser.add_argument('config', help='Config file')
#     parser.add_argument('checkpoint', help='Checkpoint file')
#     parser.add_argument('--out-file', default=None, help='Path to output file')
#     parser.add_argument(
#         '--device', default='cuda:0', help='Device used for inference')
#     parser.add_argument(
#         '--palette',
#         default='coco',
#         choices=['coco', 'voc', 'citys', 'random'],
#         help='Color palette used for visualization')
#     parser.add_argument(
#         '--score-thr', type=float, default=0.3, help='bbox score threshold')
#     parser.add_argument(
#         '--async-test',
#         action='store_true',
#         help='whether to set async options for async inference.')
#     args = parser.parse_args()
#     return args


# def main(args):
#     # register all modules in mmdet into the registries
#     register_all_modules()

#     # TODO: Support inference of image directory.
#     # build the model from a config file and a checkpoint file
#     model = init_detector(
#         args.config, args.checkpoint, palette=args.palette, device=args.device)

#     # init visualizer
#     visualizer = VISUALIZERS.build(model.cfg.visualizer)
#     # the dataset_meta is loaded from the checkpoint and
#     # then pass to the model in init_detector
#     visualizer.dataset_meta = model.dataset_meta

#     # test a single image
#     result = inference_detector(model, args.img)

#     # show the results
#     img = mmcv.imread(args.img)
#     img = mmcv.imconvert(img, 'bgr', 'rgb')
#     visualizer.add_datasample(
#         'result',
#         img,
#         data_sample=result,
#         draw_gt=False,
#         show=args.out_file is None,
#         wait_time=0,
#         out_file=args.out_file,
#         pred_score_thr=args.score_thr)