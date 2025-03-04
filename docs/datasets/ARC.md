# ARC

| 序号 | 数据集                          | 描述                               | 准确率 | 指令服从性 |
| ---- | ------------------------------- | ---------------------------------- | ------ | ---------- |
| 01   | [ARC-Challenge](#ARC-Challenge) | 小学水平多项选择科学问题（挑战集） | 0.9326 | 0.9812     |
| 02   | [ARC-Easy](#ARC-Easy)           | 小学水平多项选择科学问题（简单集） | 0.9465 | 0.9592     |

### ARC-Challenge

数据样式

```python
{
    "answerKey": "B",
    "choices": {
        "label": ["A", "B", "C", "D"],
        "text": ["Shady areas increased.", "Food sources increased.", "Oxygen levels increased.", "Available water increased."]
    },
    "id": "Mercury_SC_405487",
    "question": "One year, the oak trees in a park began producing more acorns than usual. The next year, the population of chipmunks in the park also increased. Which best explains why there were more chipmunks the next year?"
}
```

### ARC-Easy

数据样式

```python
{
    "answerKey": "B",
    "choices": {
        "label": ["A", "B", "C", "D"],
        "text": ["Shady areas increased.", "Food sources increased.", "Oxygen levels increased.", "Available water increased."]
    },
    "id": "Mercury_SC_405487",
    "question": "One year, the oak trees in a park began producing more acorns than usual. The next year, the population of chipmunks in the park also increased. Which best explains why there were more chipmunks the next year?"
}
```

