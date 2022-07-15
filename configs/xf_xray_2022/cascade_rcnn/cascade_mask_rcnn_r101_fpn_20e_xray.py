_base_ = './cascade_mask_rcnn_r50_fpn_20e_xray.py'
model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet101')))
