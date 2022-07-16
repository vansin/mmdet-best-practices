_base_ = './retinanet_free_anchor_r50_fpn_1x_coco.py'
model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet101')))
