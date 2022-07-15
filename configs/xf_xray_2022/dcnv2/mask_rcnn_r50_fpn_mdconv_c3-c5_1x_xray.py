_base_ = '../mask_rcnn/mask_rcnn_r50_fpn_1x_xray.py'
model = dict(backbone=dict(dcn=dict(
    type='DCNv2', deform_groups=1, fallback_on_stride=False),
                           stage_with_dcn=(False, True, True, True)))
