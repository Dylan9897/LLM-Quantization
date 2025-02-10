# AGIEval

| 序号 | 数据集                                             | 描述                                                         |
| ---- | -------------------------------------------------- | ------------------------------------------------------------ |
| 01   | [aqua-rat](#Aqua-Rat)                              | 带原理的代数问答数据集（单选题）                             |
| 02   | [gaokao-biology](#Gaokao-Biology)                  | 高考生物题（单选题）                                         |
| 03   | [gaokao-chemistry](#Gaokao-Chemistry)              | 高考化学题（单选题）                                         |
| 04   | [gaokao-chinese](#Gaokao-Chinese)                  | 高考语文题（阅读理解）（单选题）                             |
| 05   | [gaokao-english](#Gaokao-English)                  | 高考英语题（阅读理解）（单选题）                             |
| 06   | [gaokao-geography](#Gaokao-Geography)              | 高考地理题（单选题）                                         |
| 07   | [gaokao-history](#Gaokao-History)                  | 高考历史题（单选题）                                         |
| 08   | [gaokao-mathcloze](#Gaokao-Mathcloze)              | 高考数学填空题                                               |
| 09   | [gaokao-mathqa](#Gaokao-Mathqa)                    | 高考数学选择题（单选题）                                     |
| 10   | [gaokao-physics](#Gaokao-Physics)                  | 高考物理题（单选题）                                         |
| 11   | [jec-qa-ca](#Jec-qa-ca)                            | 中国国家司法考试的题目-案例分析（多选题）                    |
| 12   | [jec-qa-kd](#Jec-qa-kd)                            | 中国国家司法考试的题目（多选题）                             |
| 13   | [logiqa-en](#Logiqa-en)                            | 逻辑推理英文题（单选题）                                     |
| 14   | [logiqa-zh](#Logiqa-zh)                            | 逻辑推理中文题（单选题）                                     |
| 15   | [lsat-ar](#Lsat-ar)                                | 逻辑推理题（单选题）                                         |
| 16   | [lsat-lr](#Lsat-lr)                                | 逻辑推理题（单选题）                                         |
| 17   | [lsat-rc](#Lsat-rc)                                | 逻辑推理题（单选题）                                         |
| 18   | [math](#Math)                                      | 数学题                                                       |
| 19   | [sat-en](#Set-en)                                  | 美国大学入学考试（Scholastic Assessment Test, SAT）带有篇章阅读部分的问题（单选题） |
| 20   | [sat-en-without-passage](#Sat-en-Without-Passage ) | 美国大学入学考试（Scholastic Assessment Test, SAT）不带有篇章阅读部分的问题（评估模型在不涉及大量上下文的情况下处理特定类型问题的能力）（单选题） |
| 21   | [sat-math](#Sat-Math)                              | 美国大学入学考试（Scholastic Assessment Test, SAT）数学题    |

### Aqua-Rat

数据样式

```python
{        
    "passage": null,        
    "question": "代数问题",        
    "options": [            
        "选项一",           
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "solution": "推理过程"        
    }    
}
```

### Gaokao-Biology

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-Chemistry

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",           
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {           
        "source": "来源"        
    }    
}
```

### Gaokao-Chinese

数据样式

```python
{        
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-English

数据样式

```python
{        
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-Geography

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-History

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-Mathcloze

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": null,        
    "label": null,        
    "answer": "答案（填空的内容）",        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-Mathqa

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Gaokao-Physics

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Jec-qa-ca

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
} 
```

### Jec-qa-kd

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": {            
        "source": "来源"        
    }    
}
```

### Logiqa-en

数据样式

```python
{        
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": null    
}
```

### Logiqa-zh

数据样式

```python
{        
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": null    
}
```

### Lsat-ar

数据样式

```python
{        
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": null    
}
```

### Lsat-lr

数据样式

```python
{        
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": null    
}
```

### Lsat-rc

数据样式

```python
{       
    "passage": "阅读材料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "answer": null,        
    "other": null    
}
```

### Math

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": null,        
    "label": null,        
    "answer": "计算结果",        
    "other": {            
        "solution": "推理过程"        
    }    
}
```

### Sat-en

数据样式

```python
{        
    "passage": "背景资料",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "other": {            
        "solution": "推理过程"        
    }    
}
```

### Sat-en-Without-Passage 

数据样式

```python
{        
    "passage": null,        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "other": {            
        "solution": "推理过程"        
    }    
}
```

### Sat-Math

数据样式

```python
{        
    "passage": "",        
    "question": "问题",        
    "options": [            
        "选项一",            
        "选项二",            
        ......        
    ],        
    "label": "正确答案的选项",        
    "other": {            
        "solution": "推理过程"        
    }    
}
```

