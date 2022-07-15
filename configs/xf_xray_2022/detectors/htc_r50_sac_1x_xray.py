_base_ = '../htc/htc_r50_fpn_1x_xray.py'

model = dict(backbone=dict(type='DetectoRS_ResNet',
                           conv_cfg=dict(type='ConvAWS'),
                           sac=dict(type='SAC', use_deform=True),
                           stage_with_sac=(False, True, True, True)))
