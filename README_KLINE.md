# 股票K线图绘制工具

## 功能介绍

这个工具可以帮助你获取指定股票的行情数据，并使用mplfinance库绘制K线图（Candlestick图）。

## 安装依赖

首先需要安装mplfinance库：

```bash
python3 -m pip install mplfinance --break-system-packages
```

## 使用方法

### 命令行方式

```bash
python3 plot_kline.py <股票代码> <开始日期> <结束日期> [--k_type <k线类型>] [--adjust_type <复权类型>]
```

参数说明：
- `<股票代码>`：股票代码，如000001
- `<开始日期>`：开始日期，格式YYYY-MM-DD
- `<结束日期>`：结束日期，格式YYYY-MM-DD
- `--k_type`：k线类型，可选值：1.日；2.周；3.月,4季度，5.5min，15.15min，30.30min，60.60min，默认1
- `--adjust_type`：复权类型，可选值：0.不复权；1.前复权；2.后复权，默认1

示例：
```bash
python3 plot_kline.py 000001 2024-01-01 2024-07-23
python3 plot_kline.py 002230 2024-05-01 2024-07-23 --k_type 2
python3 plot_kline.py 600000 2024-06-01 2024-07-23 --k_type 3 --adjust_type 0
```

### 函数调用方式

在Python代码中导入plot_kline函数：

```python
from plot_kline import plot_kline

# 绘制000001股票2024年1月1日至2024年7月23日的日K线图
plot_kline('000001', '2024-01-01', '2024-07-23')

# 绘制002230股票2024年5月1日至2024年7月23日的周K线图
plot_kline('002230', '2024-05-01', '2024-07-23', k_type=2)

# 绘制600000股票2024年6月1日至2024年7月23日的月K线图，不复权
plot_kline('600000', '2024-06-01', '2024-07-23', k_type=3, adjust_type=0)
```

## 注意事项

1. 确保你有网络连接，因为数据是从网络获取的
2. 如果系统缺少SimHei字体，中文标签可能显示为方框，这不会影响K线图的生成
3. 支持的股票代码包括A股、港股等（具体取决于底层接口的支持）

## 示例文件

你可以运行example.py文件查看更多示例：

```bash
python3 example.py
```