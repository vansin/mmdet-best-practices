# PASCAL VOC2007

[PASCAL VOC官网地址](http://host.robots.ox.ac.uk/pascal/VOC/)

## 方法一: 下载已经处理好的数据集

为了更快的上手，笔者已经把PASCAL VOC2007预处理好了成COCO格式，可以通过[下载到本地(密码nnqk)](https://pan.baidu.com/s/1rJcZ1afOemitGgCnpDYTww)，并整理解压到data文件夹中，如下图所示。

![](https://moonstarimg.oss-cn-hangzhou.aliyuncs.com/img/20220716230704.png)

## 方法二从官网下载并处理成COCO格式

```shell
python tools/misc/download_dataset.py --dataset-name voc2007 --save-dir data/voc2007 --unzip
```

### PASCAL 转换为 COCO格式数据集

```shell
python tools/dataset_converters/pascal_voc.py -o data/voc2007 --out-format coco data/voc2007/VOCdevkit
```

同样经过一些操作整理成上图的形式。
