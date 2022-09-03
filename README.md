# MMDet 3.x最佳实践

本仓库将介绍①包含无侵入式自定义模型、数据集、Hook的最佳实践②提供参加目标检测比赛的模板③组织MMDetection源码共读活动

## 1.环境配置


```shell
git clone -b 3.x https://github.com/vansin/mmdet-best-practices.git
```


```shell
conda create --name mmdetbp-3.x python=3.9 -y
# 进入虚拟环境，后续所有操作都需要在mmdetbp虚拟环境中操作
conda activate mmdetbp-3.x
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0rc1"
mim install "mmdet>=3.0.0rc0"
```

## 2. 数据集准备

推荐使用balloon气球数据集学习MMDetection

### balloon

```shell
python tools/misc/download_dataset.py  --dataset-name balloon --save-dir data --unzip
python tools/dataset_converters/ballon2coco.py
python tools/train.py configs/balloon/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py
```