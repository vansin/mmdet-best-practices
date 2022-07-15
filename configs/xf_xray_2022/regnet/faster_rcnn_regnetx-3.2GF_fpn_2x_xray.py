_base_ = './faster_rcnn_regnetx-3.2GF_fpn_1x_xray.py'
lr_config = dict(step=[16, 22])
runner = dict(type='EpochBasedRunner', max_epochs=24)
