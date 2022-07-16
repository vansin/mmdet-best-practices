# MMDetection最佳实践

<div align="center">

[English](README.md) | 简体中文

</div>

本仓库将介绍①包含无侵入式自定义模型、数据集、Hook的最佳实践②提供参加目标检测比赛的模板③组织MMDetection源码共读活动

## 1.环境配置

```shell
git clone https://github.com/vansin/mmdet-best-practices.git
```

### 创建虚拟环境

```shell
conda create --name mmdet-bp python=3.9 -y

# 进入虚拟环境，后续所有操作都需要在mmdet-bp虚拟环境中操作
conda activate mmdet-bp
```

### 安装PyTorch

```shell
conda activate mmdet-bp
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
```

### 安装mmcv

```shell
# 安装mim
pip install -U openmim
# 使用mim安装mmcv-full
mim install mmcv-full
```

### 安装submodule

<!-- （不需要执行）
```shell
git submodule add https://github.com/open-mmlab/mmdetection.git
git submodule add https://www.github.com/open-mmlab/mmclassification.git
``` -->

以下命令用户把MMDetection和MMClassification同步到本地。

```shell
git submodule init
git submodule update
```

#### 安装MMDetection

```shell
pip install -r mmdetection/requirements/build.txt
pip install -v -e mmdetection
```

#### 安装MMClassification(可选)

```shell
pip install -v -e mmclassification
```

### 安装本工具MMDetBP

```shell
pip install -v -e .
```

### 代码规范相关(可选)

```shell
pip install pre-commit
pre-commit install
```

## 2. 数据集

### 重命名config

```shell
find . -type f -name "*coco*" -print0 | while read -r -d '' file; do
    mv "$file" "${file//coco/xray}"
done
```

## 3. 比赛

### 3.1 [X光安检图像检测挑战赛3.0](https://challenge.xfyun.cn/topic/info?type=Xray-2022)

<!-- 已经整理好的数据集链接: https://pan.baidu.com/s/1C0luFgCyv_uxVAk3g1ruow 提取码: xray -->

![](https://moonstarimg.oss-cn-hangzhou.aliyuncs.com/000008.jpg)

![](https://moonstarimg.oss-cn-hangzhou.aliyuncs.com/000080.jpg)
