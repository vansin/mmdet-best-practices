_base_ = '../mask_rcnn/mask_rcnn_x101_32x4d_fpn_1x_xray.py'
model = dict(
    backbone=dict(norm_cfg=dict(type='SyncBN', requires_grad=True),
                  norm_eval=False,
                  plugins=[
                      dict(cfg=dict(type='ContextBlock', ratio=1. / 16),
                           stages=(False, True, True, True),
                           position='after_conv3')
                  ]))
