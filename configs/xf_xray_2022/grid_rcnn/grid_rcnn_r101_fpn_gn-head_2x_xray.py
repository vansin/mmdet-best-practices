_base_ = './grid_rcnn_r50_fpn_gn-head_2x_xray.py'

model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet101')))
