_base_ = './mask_rcnn_hrnetv2p_w40_1x_xray.py'
# learning policy
lr_config = dict(step=[16, 22])
runner = dict(type='EpochBasedRunner', max_epochs=24)
