_base_ = './mask2former_r50_lsj_8x2_50e_xray-panoptic.py'

model = dict(backbone=dict(
    depth=101,
    init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet101')))
