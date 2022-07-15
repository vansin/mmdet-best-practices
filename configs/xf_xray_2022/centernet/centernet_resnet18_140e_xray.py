_base_ = './centernet_resnet18_dcnv2_140e_xray.py'

model = dict(neck=dict(use_dcn=False))
