_base_ = './faster_rcnn_r50_caffe_dc5_mstrain_1x_xray.py'
# learning policy
lr_config = dict(step=[28, 34])
runner = dict(type='EpochBasedRunner', max_epochs=36)
