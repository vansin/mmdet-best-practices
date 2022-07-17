# PASCAL VOC2007

[PASCAL VOC官网地址](http://host.robots.ox.ac.uk/pascal/VOC/)

## 1. 方法一：国内OpenDataLab渠道

### 1.1. 下载

到国内镜像[OpenDataLab](https://opendatalab.com/PASCAL_VOC2007/download)上下载PASCAL VOC2007数据集到本地data文件夹

![](https://moonstarimg.oss-cn-hangzhou.aliyuncs.com/img/20220717104508.png)

### 1.2. 解压

```shell
python tools/misc/download_dataset.py --dataset-name voc2007 --save-dir data --unzip --delete
```

### 1.3. PASCAL转换为COCO格式数据集

```shell
python tools/dataset_converters/pascal_voc.py -o data/VOCdevkit --out-format coco data/VOCdevkit
```

同样经过一些操作整理成上图的形式。

## 方法二: 下载已经处理好的数据集

为了更快的上手，笔者已经把PASCAL VOC2007预处理好了成COCO格式，可以通过[下载到本地(密码nnqk)](https://pan.baidu.com/s/1rJcZ1afOemitGgCnpDYTww)，并整理解压到data文件夹中，如下图所示。

![](https://moonstarimg.oss-cn-hangzhou.aliyuncs.com/img/20220716230704.png)
