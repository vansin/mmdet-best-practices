_base_ = './mask_rcnn_r50_fpn_gn-all_contrib_2x_xray.py'

# learning policy
lr_config = dict(step=[28, 34])
runner = dict(type='EpochBasedRunner', max_epochs=36)
