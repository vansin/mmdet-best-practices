_base_ = './faster_rcnn_r50_fpn_gn_ws-all_1x_xray.py'
model = dict(backbone=dict(depth=101,
                           init_cfg=dict(
                               type='Pretrained',
                               checkpoint='open-mmlab://jhu/resnet101_gn_ws')))
