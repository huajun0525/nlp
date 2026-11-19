# review-analyze-lstm 运维与运行指南

本项目基于 **长短期记忆网络（LSTM）** 实现中文电商评论的情感二分类任务（判断评论为正面好评或负面差评）。本文档整理了本地开发、调试、日常运行与维护的实用操作指南。

---

## 📌 1. 项目定位与核心指标

* **任务类型**：文本二分类（0：负向差评，1：正向好评）
* **数据集**：`data/raw/online_shopping_10_cats.csv`（涵盖 10 类电商产品评论）
* **核心指标**：当前模型在测试集上的准确率（Accuracy）达到 **91.72%**
* **模型文件**：`models/best.pt`（已固化训练好的模型权重）
* **词表规模**：`models/vocab.txt`（包含 61,032 个词条）

---

## 🚀 2. IDE 极简操作（IDEA / PyCharm）

在日常开发调试中，推荐直接在 IDE 中可视化操作：

### ① 确认解释器与源码目录（首次打开检查）
1. **解释器绑定**：
   * 点击窗口右下角状态栏，确认当前模块绑定的解释器为本目录下的虚拟环境：
     `Python 3.12 (review-analyze-lstm)`（对应路径：`review-analyze-lstm/.venv/Scripts/python.exe`）。
2. **源码目录标识**：
   * 项目左侧目录树中，`src` 文件夹图标应为**浅蓝色**。
   * 若为普通黄色文件夹，鼠标右键点击 `src` 目录 $\rightarrow$ **Mark Directory as** $\rightarrow$ **Sources Root**（消除所有同级导包红线）。

### ② 脚本一键运行方式（直接右键即可）

| 运维操作 | 目标脚本 | 执行方法 | 说明 |
|---|---|---|---|
| **交互式情感预测** | `src/predict.py` | 在编辑器中**直接鼠标右键 $\rightarrow$ Run 'predict'** | 启动交互式控制台，输入任意评论即时输出预测情感与置信度；输入 `q` 退出 |
| **模型效果评估** | `src/evaluate.py` | 在编辑器中**直接鼠标右键 $\rightarrow$ Run 'evaluate'** | 自动读取测试集进行批量推理，控制台输出当前的准确率 `acc` |
| **模型训练重跑** | `src/train.py` | 在编辑器中**直接鼠标右键 $\rightarrow$ Run 'train'** | 从头开始训练 LSTM，每个 Epoch 打印 Loss 并自动将更优权重保存到 `models/best.pt` |
| **数据重新处理** | `src/process.py` | 在编辑器中**直接鼠标右键 $\rightarrow$ Run 'process'** | 重新划分训练/测试集并更新词表（注意：更新词表后必须重新跑 `train.py`） |
| **分词与词表自检** | `src/tokenizer.py` | 在编辑器中**直接鼠标右键 $\rightarrow$ Run 'tokenizer'** | 打印当前词表规模并测试样例文本编码结果 |

> **提示**：选中脚本后也可以直接使用快捷键 `Ctrl + Shift + F10` 快速启动当前文件。

---

## 💻 3. 终端命令行运行方式

若脱离 IDE 或在服务器/终端环境下运行，可进入本项目目录执行：

### ① 激活虚拟环境
```powershell
# 进入当前子项目目录
cd review-analyze-lstm

# 激活专属虚拟环境 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
```

### ② 核心命令速查
```bash
# 1. 运行交互式预测推理
python src/predict.py

# 2. 评估当前模型在测试集上的表现
python src/evaluate.py

# 3. 启动模型训练
python src/train.py
```

---

## 📊 4. TensorBoard 监控看板运维

训练过程中（`train.py`）会将损失曲线实时打点记录到 `logs/` 目录下。

### ① 启动 Web 服务
在当前目录终端中执行：
```powershell
.\.venv\Scripts\python.exe -m tensorboard.main --logdir logs
```

### ② 查看指标
* 终端输出类似 `TensorBoard 2.21.0 at http://localhost:6006/`；
* 打开浏览器访问：👉 **`http://localhost:6006/`**；
* 可在网页中实时观察每轮 Epoch 的 `Loss` 训练下降曲线。
* **退出服务**：在终端按 `Ctrl + C` 即可中止服务。

> **端口冲突排障**：若 6006 端口被占用，可指定其他端口启动：
> ```powershell
> .\.venv\Scripts\python.exe -m tensorboard.main --logdir logs --port 6007
> ```

---

## 🔧 5. 运维与常见排障速查（FAQ）

### Q1：编辑器里 `from dataset import ...` 飘红线，但能跑？
* **原因**：IDE 没有识别到 `src` 为根目录。
* **解决**：在左侧工程导航树上，右键点击 `src` $\rightarrow$ **Mark Directory as** $\rightarrow$ **Sources Root**。

### Q2：报错 `AttributeError: module 'jieba' has no attribute 'lcut'`？
* **原因**：误装了十年前已废弃的古老包 `jieba3k`，破坏了现代 jieba 文件。
* **解决**：严禁安装 `jieba3k`。在终端执行：
  ```powershell
  .\.venv\Scripts\python.exe -m pip uninstall -y jieba3k
  .\.venv\Scripts\python.exe -m pip install --force-reinstall jieba
  ```

### Q3：纯 CPU 机器上加载权重报错 `Attempting to deserialize object on a CUDA device`？
* **原因**：PyTorch 默认尝试将 GPU 上导出的模型载入 GPU。
* **解决**：代码中加载模型时统一补充了 `map_location=device` 参数，已内置支持无缝自适应 CPU/CUDA：
  ```python
  model.load_state_dict(torch.load(config.MODELS_DIR / 'best.pt', map_location=device))
  ```

### Q4：超参数如何调整？
所有关键模型配置均集中于 **`src/config.py`**：
* `SEQ_LEN = 128`：文本截断/填充的序列最大长度；
* `BATCH_SIZE = 64`：每批次样本数；
* `EMBEDDING_DIM = 128`：词向量维度；
* `HIDDEN_SIZE = 256`：LSTM 隐藏层节点数；
* `LEARNING_RATE = 1e-3`：Adam 优化器学习率；
* `EPOCHS = 20`：完整训练轮数。
