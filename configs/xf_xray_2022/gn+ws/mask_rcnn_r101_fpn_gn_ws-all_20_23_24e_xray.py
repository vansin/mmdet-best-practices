_base_ = './mask_rcnn_r101_fpn_gn_ws-all_2x_xray.py'
# learning policy
lr_config = dict(step=[20, 23])
runner = dict(type='EpochBasedRunner', max_epochs=24)
