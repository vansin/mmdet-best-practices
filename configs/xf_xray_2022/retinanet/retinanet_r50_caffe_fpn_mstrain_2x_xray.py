_base_ = './retinanet_r50_caffe_fpn_mstrain_1x_xray.py'
# learning policy
lr_config = dict(step=[16, 23])
runner = dict(type='EpochBasedRunner', max_epochs=24)
