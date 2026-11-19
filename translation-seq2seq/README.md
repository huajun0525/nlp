# translation-seq2seq 运维与运行指南

本项目基于 **经典序列到序列架构（Sequence-to-Sequence / Seq2Seq）** 与 **门控循环单元（GRU）** 实现中英文机器翻译（中文输入 $\rightarrow$ 英文输出）。本文档整理了本地环境配置、IDE可视化调试、命令行运行与运维排障指南。

---

## 📌 1. 项目定位与核心指标

* **任务类型**：中英机器翻译（Sequence-to-Sequence 生成任务）
* **网络架构**：
  * **Encoder（编码器）**：Embedding(128) + 单向 GRU(256)，提取中文句子的全局语义向量（Context Vector）。
  * **Decoder（解码器）**：Embedding(128) + 单向 GRU(256) + Linear(vocab_size)，接收 Context Vector 作为初始隐状态，以自回归（Auto-regressive）方式逐步生成英文单词。
* **数据集**：`data/raw/cmn.txt`（经典的 Tatoeba 中英平行语料对）
* **词表与模型产物**：
  * 中文词表：`models/zh_vocab.txt`
  * 英文词表：`models/en_vocab.txt`
  * 模型权重：`models/best.pt`
* **评估基准**：当前模型在测试集上的 **Corpus BLEU** 分数达到 **0.1825**。

---

## 🚀 2. IDE 极简操作（IDEA / PyCharm）

在日常开发与演示中，推荐直接在 IDE 中鼠标右键运行：

### ① 确认解释器与源码目录（首次打开检查）
1. **解释器绑定**：
   * 确保当前模块绑定的解释器为本目录下的虚拟环境：
     `Python 3.12 (translation-seq2seq)`（对应路径：`translation-seq2seq/.venv/Scripts/python.exe`）。
2. **源码目录标识**：
   * 确认 `src` 文件夹图标为**浅蓝色**。
   * 若为普通黄色，在左侧目录树鼠标右键点击 `src` $\rightarrow$ **Mark Directory as** $\rightarrow$ **Sources Root**。

### ② 脚本一键运行方式（直接右键即可）

| 运维操作 | 目标脚本 | 执行方法 | 说明 |
|---|---|---|---|
| **中英交互式翻译** | `src/predict.py` | 在编辑器中**直接右键 $\rightarrow$ Run 'predict'** | 启动终端输入中文，即时输出翻译后的英文句子；输入 `q` 退出 |
| **测试集 BLEU 评估** | `src/evaluate.py` | 在编辑器中**直接右键 $\rightarrow$ Run 'evaluate'** | 自动对整个测试集进行批量推理并计算语料级 BLEU 得分 |
| **模型训练重跑** | `src/train.py` | 在编辑器中**直接右键 $\rightarrow$ Run 'train'** | 运行 50 轮 Seq2Seq 训练，自动记录 Loss 并更新保存 `models/best.pt` |
| **数据重新预处理** | `src/process.py` | 在编辑器中**直接右键 $\rightarrow$ Run 'process'** | 重新切分数据集并重新生成中英双语词表 |
| **BLEU 算法自检** | `test/test-bleu.py` | 在编辑器中**直接右键 $\rightarrow$ Run 'test-bleu'** | 样例演示 NLTK 的 `corpus_bleu` 分数计算过程 |
| **分词器效果自检** | `src/tokenizer.py` | 在编辑器中**直接右键 $\rightarrow$ Run 'tokenizer'** | 测试英文 Treebank 分词与还原逻辑 |

> **快捷键提示**：打开对应脚本文件后，直接按快捷键 `Ctrl + Shift + F10` 即可快速启动。

---

## 💻 3. 终端命令行运行方式

若脱离 IDE 在 PowerShell 终端环境下运行：

### ① 激活虚拟环境
```powershell
# 进入当前子项目目录
cd translation-seq2seq

# 激活专属虚拟环境 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
```

### ② 常用命令速查
```bash
# 1. 运行交互式翻译控制台
python src/predict.py

# 2. 计算测试集 BLEU 评分
python src/evaluate.py

# 3. 启动模型训练流程
python src/train.py
```

---

## 📊 4. TensorBoard 训练可视化监控

训练过程（`train.py`）会自动把损失曲线写入 `logs/` 目录。

### ① 启动 Web 服务
在当前目录下执行：
```powershell
.\.venv\Scripts\python.exe -m tensorboard.main --logdir logs
```

### ② 浏览器查看
* 启动成功后，浏览器打开 👉 **`http://localhost:6006/`**；
* 可在网页中实时查看训练 Loss 下降趋势。
* **退出服务**：在终端按 `Ctrl + C` 即可中止 Web 服务。

> **端口冲突排障**：若 6006 端口被占用，可指定其他端口启动：
> ```powershell
> .\.venv\Scripts\python.exe -m tensorboard.main --logdir logs --port 6008
> ```

---

## 🔧 5. 运维与常见排障速查（FAQ）

### Q1：解码生成时如何防止死循环？
* **机制**：在 `predict.py` 的自回归解码中，设置了最大步长阈值 `config.MAX_SEQ_LENGTH = 128`。当模型生成了 `<eos>` 结束符，或者达到 128 个单词时，循环会自动终止，并切掉 `<eos>` 之后的多余字符。

### Q2：CPU 环境加载 GPU 保存的权重报 `RuntimeError`？
* **机制**：原作者在 CUDA 上训练了模型，代码中加载模型时已统一补充 `map_location=device`：
  ```python
  model.load_state_dict(torch.load(config.MODELS_DIR / 'best.pt', map_location=device))
  ```
  无需手动修改，可在纯 CPU 或 GPU 环境下自动无缝运行。

### Q3：超参数如何调整？
所有关键参数统一在 **`src/config.py`** 中配置：
* `MAX_SEQ_LENGTH = 128`：自回归生成的最大句子长度；
* `BATCH_SIZE = 64`：每批训练样本数；
* `EMBEDDING_DIM = 128`：词向量维度；
* `HIDDEN_SIZE = 256`：GRU 隐藏状态维度；
* `LEARNING_RATE = 1e-3`：Adam 优化器学习率；
* `EPOCHS = 50`：完整训练轮数。
