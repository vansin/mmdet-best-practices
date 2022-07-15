_base_ = './fast_rcnn_r50_fpn_1x_xray.py'
model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet101')))
