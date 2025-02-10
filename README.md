# - 大模型推理

#### 1. 简介

​		随着大型语言模型（LLM）的发展，其参数规模已达到数十亿乃至更多，这些庞大的模型虽然在自然语言处理任务中表现出卓越性能，但同时也带来了显著的挑战。首先，巨大的参数量导致了高昂的存储成本；其次，进行推理时需要消耗大量的计算资源，使得在普通消费级硬件上直接运行变得不切实际。为了解决这些问题，通常依赖于配备大容量显存的图形处理单元（GPU）以加速推理过程。

​		面对这一挑战，研究界积极探索优化模型部署的方法，其中量化技术成为了关键解决方案之一。通过减少模型权重的精度，量化不仅有效降低了模型大小和运算需求，还提高了模型在资源受限环境中的部署可能性。本项目专注于探索并实现高效的量化策略，旨在确保大型语言模型可以在更广泛的硬件平台上高效运行，从而推动人工智能技术的普及应用。

#### 2. 目录

- [快速开始](#3-快速开始)
- [数据集](#4-数据集)
- [实验设置](#5-实验设置)
- [实验结果](#6-实验结果)
- [文件结构](#7-文件结构)

#### 3. 快速开始

- **安装指南**：

  ```bash
  pip install -r requirments.txt
  ```

- **运行说明**：

  运行

  ```bash
  python run.py --dataset="AGIEval" --setting="GseRo"
  python run.py --dataset="ARC" --setting="GseRo"
  python run.py --dataset="BBH" --setting="GseRo"
  python run.py --dataset="ceval" --setting="GseRo"
  ```

  评估

  ```bash
  python eval.py --dataset="AGIEval" --setting="GseRo"
  python eval.py --dataset="ARC" --setting="GseRo"
  python eval.py --dataset="BBH" --setting="GseRo"
  python eval.py --dataset="ceval" --setting="GseRo"
  ```

#### 4. 数据集

​	本项目采用了一系列与大模型相关的开源评测数据集进行性能评估，详细情况请参见下表：

| **序号** | **数据集**                                                  | **论文**                             | **数据集描述**                         |
| -------- | ----------------------------------------------------------- | ------------------------------------ | -------------------------------------- |
| **1**    | [**AGIEval**](https://github.com/ruixiangcui/AGIEval)       | https://arxiv.org/pdf/2304.06364.pdf | [AGIEval.md](docs/datasets/AGIEval.md) |
| **2**    | [**ARC**](https://opendatalab.com/OpenDataLab/ARC)          | https://arxiv.org/pdf/1803.05457v1   | [ARC.md](docs/datasets/ARC.md)         |
| **3**    | [**BBH**](https://github.com/suzgunmirac/BIG-Bench-Hard)    | https://arxiv.org/pdf/2210.09261v1   | [BBH.md](docs/datasets/BBH.md)         |
| **4**    | [**ceval**](https://github.com/hkust-nlp/ceval/tree/main)   | https://arxiv.org/pdf/2305.08322     | [ceval.md](docs/datasets/ceval.md)     |
| **5**    | [**CLUE**](https://github.com/CLUEbenchmark/CLUE)           | https://arxiv.org/pdf/2004.05986     | ##                                     |
| **6**    | [**SuperGLUE**](https://github.com/CLUEbenchmark/SuperCLUE) | https://arxiv.org/abs/2307.15020     | ##                                     |
| **7**    | **commonsenseqa**                                           | ##                                   | ##                                     |
| **8**    | **drop**                                                    | ##                                   | ##                                     |
| **9**    | **FewCLUE**                                                 | ##                                   | ##                                     |
| **10**   | **flores_first100**                                         | ##                                   | ##                                     |
| **11**   | **GAOKAO-BENCH**                                            | ##                                   | ##                                     |
| **12**   | **gsm8k**                                                   | ##                                   | ##                                     |
| **13**   | **hellaswag**                                               | ##                                   | ##                                     |
| **14**   | **humaneval**                                               | ##                                   | ##                                     |
| **15**   | **lambada**                                                 | ##                                   | ##                                     |
| **16**   | **LCSTS**                                                   | ##                                   | ##                                     |
| **17**   | **math**                                                    | ##                                   | ##                                     |
| **18**   | **mbpp**                                                    | ##                                   | ##                                     |
| **19**   | **mmlu**                                                    | ##                                   | ##                                     |
| **20**   | **nq**                                                      | ##                                   | ##                                     |
| **21**   | **openbookqa**                                              | ##                                   | ##                                     |
| **22**   | **piqa**                                                    | ##                                   | ##                                     |
| **23**   | **race**                                                    | ##                                   | ##                                     |
| **24**   | **siqa**                                                    | ##                                   | ##                                     |
| **25**   | **strategyqa**                                              | ##                                   | ##                                     |
| **26**   | **summedits**                                               | ##                                   | ##                                     |
| **27**   | **cmmlu**                                                   | ##                                   | ##                                     |
| **28**   | **TheoremQA**                                               | ##                                   | ##                                     |
| **29**   | **triviaqa**                                                | ##                                   | ##                                     |
| **30**   | **tydiqa**                                                  | ##                                   | ##                                     |
| **31**   | **winogrande**                                              | ##                                   | ##                                     |
| **32**   | **xstory_cloze**                                            | ##                                   | ##                                     |
| **33**   | **Xsum**                                                    | ##                                   | ##                                     |

#### 5. 实验设置

- **硬件要求**：需配备NVIDIA GeForce RTX 4090显卡以确保最佳性能。
- **软件环境**：请参考项目根目录下的`requirements.txt`文件来安装所有必要的软件依赖项。

#### 6. 实验

- DeepZeek

  - 模型选择：DeepZeek-Chat

  - 实验设置：

    - 使用GseRo方法来设计和调整提示词（prompt engineering），示例如下：

      ```bash
      --Goal--
      这是一道关于注册会计师的题目，请按要求进行作答。
      
      --steps--
      1. 分析、综合文本中的复杂信息。
      2. 必要时借助外部知识帮助理解或推理。
      3. 对需要多层次思考的问题提供深思熟虑的答案。
      4. 对于每个问题，尽量找出解决问题所需的所有相关事实和条件。
      5. 推理时，确保每一步都是合理且有理有据的。如果问题涉及非常专业的知识，尽量利用已知的信息做出最佳猜测。
      6. 严格按照指定的格式 answer|A 输出答案
      
      ######################
      --Examples--
      ######################
          question1: 甲公司是国内一家上市公司。甲公司对其各子公司实行全面预算管理，并通常使用增量预算方式进行战略控制，子公司预算需要经甲公司预算管理委员会批准后执行。2015年10月，甲公司投资了一个新的项目乙(子公司)。2015年11月，甲公司启动2016年度预算编制工作，此时甲公司应要求乙公司编制____。
              options:
              	(A) 增量预算  
              	(B) 零基预算  
              	(C) 固定预算  
              	(D) 弹性预算
              output:
              	answer|B
          question2: 债务人转让全部合同义务的，下列说法不正确的是____。
              options:
              	(A) 须债权人同意方可进行  
              	(B) 新债务人可主张原债务人对债权人的抗辩  
              	(C) 债务人转移债务的，原债务人对债权人享有债权的，新债务人可以向债权人主张抵销
                  (D) 非专属于原债务人自身的从债务，一并转让给新债务人
              output:
              	answer|C
      ######################
      --Real Data--
      ######################
      	question: 下列关于税法基本原则的表述中，不正确的是____。
      	options:
              (A) 税收法定原则包括税收要件法定原则和税务合法性原则  
              (B) 税收公平原则源于法律上的平等性原则  
              (C) 税收效率原则包含经济效率和行政效率两个方面 
              (D) 税务机关按法定程序依法征税，可以自由做出减征、停征或免征税款的决定
      	output:
      
      ```

    - 本次评估聚焦于两个核心指标：对指令的服从性及模型预测能力。

  - 实验结果

    

    


#### 7. 文件结构

- **目录结构**：给出项目的文件夹和文件组织方式。
- **重要文件说明**：对一些核心文件的功能做简要说明。
