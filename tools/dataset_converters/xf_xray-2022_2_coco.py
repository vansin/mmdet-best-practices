# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import os
# import os.path as osp
import xml.etree.ElementTree as ET

# import cv2 as cv
import mmcv
import numpy as np

from mmdet_custom.datasets import XrayDataset


def dataset_classes():
    return XrayDataset.CLASSES


label_ids = {name: i for i, name in enumerate(dataset_classes())}


def parse_xml(args):
    xml_path, img_path, data_root, valid_img_path = args
    tree = ET.parse(data_root + xml_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    bboxes = []
    labels = []
    bboxes_ignore = []
    labels_ignore = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        label = label_ids[name]
        # difficult = float(obj.find('difficult').text)
        difficult = None
        bnd_box = obj.find('bndbox')
        bbox = [
            float(bnd_box.find('xmin').text),
            float(bnd_box.find('ymin').text),
            float(bnd_box.find('xmax').text),
            float(bnd_box.find('ymax').text)
        ]
        if difficult:
            bboxes_ignore.append(bbox)
            labels_ignore.append(label)
        else:
            bboxes.append(bbox)
            labels.append(label)
    if not bboxes:
        bboxes = np.zeros((0, 4))
        labels = np.zeros((0, ))
    else:
        bboxes = np.array(bboxes, ndmin=2) - 1
        labels = np.array(labels)
    if not bboxes_ignore:
        bboxes_ignore = np.zeros((0, 4))
        labels_ignore = np.zeros((0, ))
    else:
        bboxes_ignore = np.array(bboxes_ignore, ndmin=2) - 1
        labels_ignore = np.array(labels_ignore)
    annotation = {
        'filename': img_path,
        'width': w,
        'height': h,
        'ann': {
            'bboxes': bboxes.astype(np.float32),
            'labels': labels.astype(np.int64),
            'bboxes_ignore': bboxes_ignore.astype(np.float32),
            'labels_ignore': labels_ignore.astype(np.int64)
        }
    }
    return annotation


def cvt_annotations(xml_dirs,
                    out_ann_file,
                    data_root,
                    out_valid_img_dir,
                    every_n_num_img_save=1):

    annotations = []

    xml_paths = []
    img_paths = []
    valid_img_paths = []
    data_roots = []

    cout_nums = 0

    for xml_dir in xml_dirs:

        xmls = os.listdir(data_root + xml_dir)

        for item in xmls:
            if '.xml' in item:
                cout_nums += 1
                if cout_nums % every_n_num_img_save != 0:
                    continue

                valid_img_paths.append(out_valid_img_dir + '/' +
                                       item.replace('.xml', '.jpg'))
                xml_paths.append(xml_dir + '/' + item)
                jpg_item_jpg = item.replace('.xml', '.jpg')
                jpg_item_JPN = item.replace('.xml', '.JPG')
                jpg_item_png = item.replace('.xml', '.png')
                jpg_item_PNG = item.replace('.xml', '.PNG')
                jpg_item_TIFF = item.replace('.xml', '.TIFF')

                if jpg_item_jpg in xmls:
                    img_paths.append(xml_dir + '/' + jpg_item_jpg)
                elif jpg_item_JPN in xmls:
                    img_paths.append(xml_dir + '/' + jpg_item_JPN)
                elif jpg_item_png in xmls:
                    img_paths.append(xml_dir + '/' + jpg_item_png)
                elif jpg_item_PNG in xmls:
                    img_paths.append(xml_dir + '/' + jpg_item_PNG)
                elif jpg_item_TIFF in xmls:
                    img_paths.append(xml_dir + '/' + jpg_item_TIFF)
                else:
                    print(item)
                    break
                data_roots.append(data_root)

    part_annotations = mmcv.track_progress(
        parse_xml, list(zip(xml_paths, img_paths, data_roots,
                            valid_img_paths)))
    annotations.extend(part_annotations)

    if out_ann_file.endswith('json'):
        annotations = cvt_to_coco_json(annotations)
    mmcv.dump(annotations, out_ann_file)
    return annotations


def cvt_to_coco_json(annotations):
    image_id = 0
    annotation_id = 0
    coco = dict()
    coco['images'] = []
    coco['type'] = 'instance'
    coco['categories'] = []
    coco['annotations'] = []
    image_set = set()

    def addAnnItem(annotation_id, image_id, category_id, bbox, difficult_flag):
        annotation_item = dict()
        annotation_item['segmentation'] = []

        seg = []
        # bbox[] is x1,y1,x2,y2
        # left_top
        seg.append(int(bbox[0]))
        seg.append(int(bbox[1]))
        # left_bottom
        seg.append(int(bbox[0]))
        seg.append(int(bbox[3]))
        # right_bottom
        seg.append(int(bbox[2]))
        seg.append(int(bbox[3]))
        # right_top
        seg.append(int(bbox[2]))
        seg.append(int(bbox[1]))

        annotation_item['segmentation'].append(seg)

        xywh = np.array(
            [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]])
        annotation_item['area'] = int(xywh[2] * xywh[3])
        if difficult_flag == 1:
            annotation_item['ignore'] = 0
            annotation_item['iscrowd'] = 1
        else:
            annotation_item['ignore'] = 0
            annotation_item['iscrowd'] = 0
        annotation_item['image_id'] = int(image_id)
        annotation_item['bbox'] = xywh.astype(int).tolist()
        annotation_item['category_id'] = int(category_id)
        annotation_item['id'] = int(annotation_id)
        coco['annotations'].append(annotation_item)
        return annotation_id + 1

    for category_id, name in enumerate(dataset_classes()):
        category_item = dict()
        category_item['supercategory'] = str('none')
        category_item['id'] = int(category_id)
        category_item['name'] = str(name)
        coco['categories'].append(category_item)

    for ann_dict in annotations:
        file_name = ann_dict['filename']
        ann = ann_dict['ann']
        assert file_name not in image_set
        image_item = dict()
        image_item['id'] = int(image_id)
        image_item['file_name'] = str(file_name)
        image_item['height'] = int(ann_dict['height'])
        image_item['width'] = int(ann_dict['width'])
        coco['images'].append(image_item)
        image_set.add(file_name)

        bboxes = ann['bboxes'][:, :4]
        labels = ann['labels']
        for bbox_id in range(len(bboxes)):
            bbox = bboxes[bbox_id]
            label = labels[bbox_id]
            annotation_id = addAnnItem(annotation_id,
                                       image_id,
                                       label,
                                       bbox,
                                       difficult_flag=0)

        # bboxes_ignore = ann['bboxes_ignore'][:, :4]
        # labels_ignore = ann['labels_ignore']
        # for bbox_id in range(len(bboxes_ignore)):
        #     bbox = bboxes_ignore[bbox_id]
        #     label = labels_ignore[bbox_id]
        #     annotation_id = addAnnItem(
        #         annotation_id, image_id, label, bbox, difficult_flag=1)

        image_id += 1

    return coco


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert PASCAL VOC annotations to mmdetection format')
    parser.add_argument('devkit_path', help='pascal voc devkit path')
    parser.add_argument('-o', '--out-dir', help='output path')
    parser.add_argument(
        '--out-format',
        default='pkl',
        choices=('pkl', 'coco'),
        help='output format, "coco" indicates coco annotation format')
    args = parser.parse_args()
    return args


def main():

    data_root = 'data/xray-2022/'
    # 设置所有训练集
    xml_path = ['train/domain1', 'train/domain2', 'train/domain3']
    json_out_path = data_root + 'train_all.json'
    cvt_annotations(xml_path,
                    json_out_path,
                    data_root=data_root,
                    out_valid_img_dir='data/valid')

    xml_path = ['train/domain1', 'train/domain2', 'train/domain3']
    json_out_path = data_root + 'val.json'
    cvt_annotations(xml_path,
                    json_out_path,
                    data_root=data_root,
                    out_valid_img_dir='data/valid',
                    every_n_num_img_save=10)


if __name__ == '__main__':
    main()
