
descrips = {
    "aqua-rat":"Multiple choice question type question and answer data containing explanations of algebraic principles",
    "gaokao-biology":"高考生物单项选择题",
    "gaokao-chemistry":"高考化学单项选择题",
    "gaokao-chinese":"高考语文的阅读理解题目，采用单项选择的形式",
    "gaokao-english":"高考英语的阅读理解题目，采用单项选择的形式",
    "gaokao-geography":"高考地理单项选择题",
    "gaokao-history":"高考历史单项选择题",
    "gaokao-mathcloze":"高考数学填空题",
    "gaokao-mathqa":"高考数学单项选择题",
    "gaokao-physics":"高考物理单项选择题",
    "jec-qa-ca":"中国国家司法考试中的案例分析题目——多项选择题型",
    "jec-qa-kd":"中国国家司法考试中的多选题题目",
    "logiqa-en":"Logical Reasoning English Multiple Choice Questions",
    "logiqa-zh":"逻辑推理中文选择题",
    "lsat-ar":"Logical reasoning multiple choice questions",
    "lsat-lr":"Logical reasoning multiple choice questions",
    "lsat-rc":"Logical reasoning multiple choice questions",
    "math":"Math Problems",
    "sat-en":"The Scholastic Assessment Test (SAT), an American college entrance exam, includes multiple-choice questions on the passage reading section",
    "sat-en-without-passage":"Multiple-choice questions from the Scholastic Assessment Test (SAT) in the US college entrance exam",
    "sat-math":"Multiple-choice questions from the SAT (Mathematics Assessment Test) in the US college entrance exam."
}

en_prefix = "This is a question about {description}. Please answer it according to the requirements."
zh_prefix = "这是一道关于{description}的题目，请按要求进行作答。"

en_steps = """
1. Analyze and synthesize complex information in texts.
2. Use external knowledge to aid understanding or reasoning when necessary.
3. Provide well-thought-out answers to questions that require multiple levels of thinking.
4. For each question, try to identify all relevant facts and conditions needed to solve the problem.
5. When reasoning, make sure each step is reasonable and well-founded. If the question involves very specialized knowledge, try to make the best guess possible using the information you know.
6. Output the answer in strict accordance with the specified format answer|A"""
zh_steps = """
1. 分析、综合文本中的复杂信息。
2. 必要时借助外部知识帮助理解或推理。
3. 对需要多层次思考的问题提供深思熟虑的答案。
4. 对于每个问题，尽量找出解决问题所需的所有相关事实和条件。
5. 推理时，确保每一步都是合理且有理有据的。如果问题涉及非常专业的知识，尽量利用已知的信息做出最佳猜测。
6. 严格按照指定的格式 answer|A 输出答案
"""
