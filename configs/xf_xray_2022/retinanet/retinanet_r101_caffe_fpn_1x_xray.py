_base_ = './retinanet_r50_caffe_fpn_1x_xray.py'
model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained',
                  checkpoint='open-mmlab://detectron2/resnet101_caffe')))
