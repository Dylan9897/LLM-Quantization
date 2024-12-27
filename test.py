def process_in_batches(data, batch_size, process_function):
    """
    将输入数据按批次处理。

    参数:
    - data: 可迭代对象，包含要处理的所有元素。
    - batch_size: int, 每个批次的大小。
    - process_function: function, 用来处理每个批次数据的函数，接受一个批次作为参数。

    返回:
    - None, 处理结果依赖于process_function的行为。
    """
    # 创建一个迭代器
    data_iterator = iter(data)
    while True:
        # 获取批次数据
        batch = list()
        try:
            for _ in range(batch_size):
                batch.append(next(data_iterator))
        except StopIteration:
            # 如果数据不足一个批次，则只处理剩余的数据
            if len(batch) == 0:
                break
            pass

        # 使用提供的函数处理当前批次的数据
        process_function(batch)

        # 如果最后一批次小于设定的batch_size，则跳出循环
        if len(batch) < batch_size:
            break


# 示例：定义一个简单的处理函数，这里只是打印出批次
def example_process_function(batch):
    print(f"Processing batch of size {len(batch)}: {batch}")


# 示例调用
data = [i for i in range(1, 15)]  # 假设我们有1到14的数据点
batch_size = 5
process_in_batches(data, batch_size, example_process_function)