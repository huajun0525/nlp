# 尚硅谷 AI 大模型之 NLP 教程项目运行指南

本项目包含多个独立的 NLP 经典任务子项目（情感分析、机器翻译、RNN输入法、词向量表达等）。为了便于管理，已对项目的运行路径和 Python 虚拟环境进行了全方位的优化。

---

## 🛠️ 1. 项目环境与多模块设计说明

为了防止不同任务间（例如基于 BERT 的情感分析与基础 RNN 情感分析）的库版本和依赖发生冲突，我们采用了**多模块独立解释器设计**：
1. **独立虚拟环境 (`.venv`)**：每个子项目目录下均创建了一个独立的 `.venv` 虚拟环境。
2. **定制依赖清单 (`requirements.txt`)**：根据各子项目中的 `import` 语句，自动在对应子目录下提取并生成了专有的依赖清单，体积更小，更加纯净。
3. **PyCharm / IDEA 多模块配置**：自动为 12 个子文件夹注册了独立的 `.iml` 模块，并更新了 `.idea/modules.xml`。现在当您使用 PyCharm 打开父级“代码”目录时，PyCharm 会自动将其识别为 12 个平行的子项目，您可以分别为每个子文件夹指派和管理各自的 Python 解释器。

---

## 🚀 2. 如何运行项目（以 `review-analyze-rnn` 情感分析为例）

所有的子项目均遵循高内聚的模块化开发，运行步骤极其简单、规范：

### 第一步：进入子项目并激活其独立虚拟环境
在终端中打开项目根目录，进入指定的子项目文件夹：
```powershell
# 1. 进入子项目
cd review-analyze-rnn

# 2. 激活该子项目的虚拟环境 (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

### 第二步：一键安装该子项目所需的第三方依赖
使用刚刚生成并归类好的依赖清单进行安装：
```bash
pip install -r requirements.txt
```
*(注：如果需要使用 GPU 训练，请确保按照 PyTorch 官网命令安装对应的 CUDA 版本。)*

### 第三步：按顺序运行核心脚本

根据 NLP 标准流程，运行顺序如下：

1. **数据预处理 (`process.py`)**
   * **命令**：`python src/process.py`
   * **作用**：读取 `data/raw/` 目录下的原始数据集（在线购物评论），自动构建 `JiebaTokenizer` 词表，生成 `vocab.txt` 并保存到 `models/` 文件夹下；同时将文本数据编码、对齐后，保存为 `data/processed/` 下的训练集 `train.jsonl` 和测试集 `test.jsonl`。
   
2. **模型训练 (`train.py`)**
   * **命令**：`python src/train.py`
   * **作用**：读取处理后的 jsonl 训练集，构建模型开展时序训练。每个 Epoch 自动打印 Loss，并自动在 TensorBoard 日志中记录训练状态。最终，会在 `models/` 下生成最佳模型参数文件（`best.pt` 或 `best.pth`）。

3. **启动 TensorBoard 可视化训练监控 (`http://localhost:6006/`)**
   * **说明**：`train.py` 仅负责把标量指标写入 `logs/` 磁盘目录，它本身不启动 Web 服务。若需在浏览器查看 Loss 变化折线图，需单独启动 TensorBoard 服务进程。
   * **启动命令**（在子项目终端执行）：
     ```powershell
     .\.venv\Scripts\python.exe -m tensorboard.main --logdir logs
     ```
   * **浏览器访问**：
     终端提示启动成功后，直接打开浏览器访问 👉 **`http://localhost:6006/`**
     *(注：训练期间保持该终端运行，按 `Ctrl + C` 可退出 Web 服务)*。

4. **模型评估 (`evaluate.py`)**
   * **命令**：`python src/evaluate.py`
   * **作用**：加载训练好的权重文件，在测试集上验证模型的 Accuracy (准确率) 或 BLEU 分数。
   
5. **交互式预测推理 (`predict.py`)**
   * **命令**：`python src/predict.py`
   * **作用**：开启一个实时互动的终端预测器。您可以在控制台输入文本，模型将当场输出预测分类、候选词或翻译结果。输入 `q` 或 `quit` 即可退出。

---

## 🔄 3. 统一修复的 Python 导入和路径问题

原项目在不同的执行上下文（从总目录运行 vs 进入子目录运行 vs 在 IDE 里运行）中可能会频繁抛出 `ModuleNotFoundError`。为此，已为您完成了以下优化修复：

1. **统一导入机制**：去除了 `predict.py`、`evaluate.py` 等脚本中混杂的 `from src.tokenizer import ...`，将其统一为了优雅的平级导入（`from tokenizer import ...`）。
2. **动态 `sys.path` 自动配置**：在各子项目（`review-analyze-rnn`、`review-analyze-gru`、`review-analyze-bert`、`input-method-rnn`）的 `src/config.py` 顶部，动态注入了搜索路径配置：
   ```python
   import sys
   from pathlib import Path
   ROOT_DIR = Path(__file__).parent.parent
   src_dir = str(ROOT_DIR / "src")
   if src_dir not in sys.path:
       sys.path.append(src_dir)
   ```
   **效果**：现在，无论您在终端中是从哪一个文件夹启动 Python（在总目录下运行 `python review-analyze-rnn/src/predict.py`，或进入子目录运行 `python src/predict.py`），脚本都能百分之百精准定位依赖，再也不会报路径找不到的错误。

---

## 📂 4. 12个子项目清单一览

本教程涵盖了 NLP 核心技术栈的演进脉络，您可以采用相同的步骤运行以下任意项目：

1. `text_rep`：词嵌入表示（Word2Vec, Jieba 分词初探，Jupyter Notebook 实验）。
2. `review-analyze-rnn`：经典循环神经网络 (RNN) 情感极性分析。
3. `review-analyze-gru`：门控循环单元 (GRU) 情感极性分析。
4. `review-analyze-lstm`：长短期记忆网络 (LSTM) 情感极性分析。
5. `review-analyze-bert`：预训练大模型 (BERT) 情感分析微调。
6. `input-method-rnn`：利用 RNN 构建中文拼音输入法的首选候选词预测。
7. `transformer` / `test-scaled-attention`：Transformer 底层基础模块（点积自注意力等）构建与测试。
8. `translation-seq2seq`：基于 Sequence-to-Sequence (Seq2Seq) 的机器翻译（中英）。
9. `translation-attention`：引入 Attention 机制的 Seq2Seq 机器翻译（中英）。
10. `translation-transformer`：基于纯 Transformer 架构的机器翻译（中英）。
11. `hugging-face`：Hugging Face 框架基础 API 实验（数据集加载、Tokenizer 使用等）。
