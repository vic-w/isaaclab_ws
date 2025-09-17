# Isaac Lab 购物车杆摄像头任务

本仓库提供了一个 Isaac Lab 强化学习任务，在默认的购物车-杆示例基础上增加了 RGB 摄像头。该任务配置将摄像头固定在小车上，把像素观测添加到策略输入中，并提供了一个使用卷积编码器处理图像流的 ``rl-games`` 训练方案。

## 仓库结构

- ``source/omni/isaac/lab_tasks/cartpole/cartpole_camera_cfg.py`` —— 使用 Isaac Lab 配置数据类定义带摄像头的任务配置的 Python 模块。
- ``config/task/rl/cartpole_camera.yaml`` —— Hydra/``rl-games`` 配置文件，在现有的购物车-杆训练流程中接入新任务，并为 RGB 观测启用基于 CNN 的编码器。
- ``scripts`` —— 预留的启动/训练脚本目录。安装好本仓库后，通常可通过 Isaac Lab 的 ``python scripts/rlgames_train.py --task=cartpole_camera`` 命令启动训练。

## 使用方法

1. 按照官方文档安装 Isaac Lab 及其依赖。
2. 将此工作区加入 Python 路径，例如执行 ``pip install -e .``。
3. 在 Isaac Lab 工作目录下运行 ``python scripts/rlgames_train.py --task cartpole_camera`` 启动训练。此时 ``rl-games`` 策略除原有的本体感知信号外，还会收到名为 ``pole_camera_rgb`` 的摄像头图像张量。

有关摄像头位置和观测连线的详细信息，请参阅配置模块中的行内注释。
