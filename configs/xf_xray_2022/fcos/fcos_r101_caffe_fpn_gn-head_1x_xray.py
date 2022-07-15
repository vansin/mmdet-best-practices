_base_ = './fcos_r50_caffe_fpn_gn-head_1x_xray.py'
model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained',
                  checkpoint='open-mmlab://detectron/resnet101_caffe')))
