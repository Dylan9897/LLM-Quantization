# BBH

| 序号 | 数据集                                  | 描述                   | 类别   |
| ---- | --------------------------------------- | ---------------------- | ------ |
| 01   | Boolean_expressions                     | 布尔表达式             | 判断题 |
| 02   | causal_judgement                        | 因果判断               | 判断题 |
| 03   | date_understanding                      | 日期判断               | 选择题 |
| 04   | disambiguation_qa                       | 指代消解               | 选择题 |
| 05   | dyck_languages                          | 括号匹配               | 解答题 |
| 06   | formal_fallacies                        | 论点判断               | 判断题 |
| 07   | geometric_shapes                        | 几何形状               | 选择题 |
| 08   | hyperbaton                              | 语句语病（形容词用法） | 选择题 |
| 09   | logical_deduction_five_objects          | 逻辑推理               | 选择题 |
| 10   | logical_deduction_seven_objects         | 逻辑推理               | 选择题 |
| 11   | logical_deduction_three_objects         | 逻辑推理               | 选择题 |
| 12   | movie_recommendation                    | 电影推荐               | 选择题 |
| 13   | multistep_arithmetic_two                | 算数题                 | 解答题 |
| 14   | navigate                                | 导航推理               | 判断题 |
| 15   | object_counting                         | 算术题                 | 解答题 |
| 16   | penguins_in_a_table                     | 算术题                 | 选择题 |
| 17   | reasoning_about_colored_objects         | 算术题                 | 选择题 |
| 18   | ruin_names                              | 电影问达               | 选择题 |
| 19   | salient_translation_error_detection     | 翻译错误               | 选择题 |
| 20   | snarks                                  | 讽刺性判断             | 选择题 |
| 21   | sports_understanding                    | 句子合理性判断         | 判断题 |
| 22   | temporal_sequences                      | 时间序列推理           | 选择题 |
| 23   | tracking_shuffled_objects_five_objects  | 逻辑推理               | 选择题 |
| 24   | tracking_shuffled_objects_seven_objects | 逻辑推理               | 选择题 |
| 25   | tracking_shuffled_objects_three_objects | 逻辑推理               | 选择题 |
| 26   | web_of_lies                             | 逻辑推理               | 判断题 |
| 27   | word_sorting                            | 排序问题               | 解答题 |

### 数据样式

```python
{
  "canary": 相关描述,
  "examples": [
    {
      "input": 问题,
      "target": 答案
    },
  ...
  ] 
}
```

