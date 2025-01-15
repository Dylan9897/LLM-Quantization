# AGIEval

| 序号 | 数据集                 | 描述                                                         |
| ---- | ---------------------- | ------------------------------------------------------------ |
| 01   | [aqua-rat](# Aqua-Rat) | 带原理的代数问答数据集（单选题）                             |
| 02   | gaokao-biology         | 高考生物题（单选题）                                         |
| 03   | gaokao-chemistry       | 高考化学题（单选题）                                         |
| 04   | gaokao-chinese         | 高考语文题（阅读理解）（单选题）                             |
| 05   | gaokao-english         | 高考英语题（阅读理解）（单选题）                             |
| 06   | gaokao-geography       | 高考地理题（单选题）                                         |
| 07   | gaokao-history         | 高考历史题（单选题）                                         |
| 08   | gaokao-mathcloze       | 高考数学填空题                                               |
| 09   | gaokao-mathqa          | 高考数学选择题（单选题）                                     |
| 10   | gaokao-physics         | 高考物理题（单选题）                                         |
| 11   | Jec-Qa-Ca              | 中国国家司法考试的题目-案例分析（多选题）                    |
| 12   | jec-qa-kd              | 中国国家司法考试的题目（多选题）                             |
| 13   | logiqa-en              | 逻辑推理英文题（单选题）                                     |
| 14   | logiqa-zh              | 逻辑推理中文题（单选题）                                     |
| 15   | lsat-ar                | 逻辑推理题（单选题）                                         |
| 16   | lsat-lr                | 逻辑推理题（单选题）                                         |
| 17   | lsat-rc                | 逻辑推理题（单选题）                                         |
| 18   | math                   | 数学题                                                       |
| 19   | sat-en                 | 美国大学入学考试（Scholastic Assessment Test, SAT）带有篇章阅读部分的问题（单选题） |
| 20   | sat-en-without-passage | 美国大学入学考试（Scholastic Assessment Test, SAT）不带有篇章阅读部分的问题（评估模型在不涉及大量上下文的情况下处理特定类型问题的能力）（单选题） |
| 21   | sat-math               | 美国大学入学考试（Scholastic Assessment Test, SAT）数学题    |

### Aqua-Rat

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

###   Jec-qa-ca

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

### Lsat-Rc

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

