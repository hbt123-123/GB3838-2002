# GB3838-2002
地表水环境质量标准

# 水质监测分析系统 (Water Quality Monitoring System)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)
## 🌟 项目特色

- **国家标准合规**：严格遵循GB3838-2002地表水环境质量标准
- **智能水质评价**：自动进行水质分类和综合评价
- **多维度分析**：趋势分析、分布统计、参数对比等丰富图表
- **便捷数据管理**：支持单次录入、批量导入、灵活查询
- **用户友好界面**：直观的图形界面，操作简单易用

## 📋 功能模块

### 🔍 单次监测
- 实时水质参数录入与评价
- 温度变化监控和pH值检查
- 自动水质类别判定（Ⅰ类至劣Ⅴ类）

### 📊 批量导入
- Excel模板数据批量导入
- 智能列映射配置
- 数据格式自动验证

### 🔎 数据查询
- 多条件组合查询（时间范围、监测断面、水质类别）
- 数据编辑与删除功能
- 查询结果导出

### 📈 分析报告
- 水质参数趋势分析
- 水质类别分布统计
- 多断面参数对比
- 交互式图表展示

## 🚀 快速开始

### 系统要求
- Windows 7/10/11
- Python 3.8+ (如使用源码运行)

### 安装使用

#### 方法一：直接运行可执行文件（推荐）
1. 下载 `main.exe` 文件
2. 双击运行即可使用

#### 方法二：从源码运行
```bash
# 克隆项目
git clone https://github.com/hbt123-123/GB3838-2002.git

# 进入项目目录
cd GB3838-2002

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```


## 📁 项目结构

```
GB3838-2002/
├── main.py                 # 主程序入口
├── config.py              # 水质参数配置
├── requirements.txt       # 依赖包列表
├── main.exe              # 可执行文件
├── modules/              # 功能模块
│   ├── monitoring_tab.py     # 单次监测模块
│   ├── batch_import_tab.py   # 批量导入模块
│   ├── data_query_tab.py     # 数据查询模块
│   ├── analysis_report_tab.py # 分析报告模块
│   └── database.py          # 数据库管理
└── water_quality.db       # 数据库文件（运行时生成）
```
## 🔧 config.py 模块接口说明

`config.py` 是水质评价的核心模块，可以独立集成到其他项目中。该模块基于GB3838-2002标准实现完整的水质参数评价功能。

### 类与方法接口

#### WaterQualityConfig 配置类

| 类属性 | 类型 | 描述 |
|--------|------|------|
| `TEMP_RISE_THRESHOLD` | float | 最大升温阈值(℃)，默认1.0℃ |
| `TEMP_DROP_THRESHOLD` | float | 最大降温阈值(℃)，默认2.0℃ |
| `MIN_PH` | float | pH最小值，默认6.0 |
| `MAX_PH` | float | pH最大值，默认9.0 |
| `PARAMETER_STANDARDS` | Dict | 所有水质参数的标准阈值 |

#### 核心评价函数

| 函数名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| `temperature_check(current_temp, last_temp)` | `current_temp`: float, `last_temp`: float | Dict[str, Union[float, str]] | 温度变化检查，不合格直接判定为劣Ⅴ类 |
| `ph_check(ph_value)` | `ph_value`: float | Dict[str, Union[float, str]] | pH值检查，不合格直接判定为劣Ⅴ类 |
| `parameter_check(param_name, value, water_type)` | `param_name`: str, `value`: float, `water_type`: str = "river" | Dict[str, Union[float, str, int]] | 通用参数检查函数，支持河流/湖库类型 |
| `evaluate_water_quality(parameters, water_type)` | `parameters`: Dict[str, Union[float, Dict]], `water_type`: str = "river" | Dict[str, Union[str, int, Dict]] | 水质综合评价函数，返回总体结果和详细信息 |

#### 专用参数检查函数

| 函数名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| `do_check(do_value)` | `do_value`: float | Dict | 溶解氧检查 |
| `codmn_check(codmn_value)` | `codmn_value`: float | Dict | 高锰酸盐指数检查 |
| `cod_check(cod_value)` | `cod_value`: float | Dict | 化学需氧量检查 |
| `bod5_check(bod_value)` | `bod_value`: float | Dict | 五日生化需氧量检查 |
| `nh4_n_check(nh4_value)` | `nh4_value`: float | Dict | 氨氮检查 |
| `tn_check(tn_value)` | `tn_value`: float | Dict | 总氮检查 |
| `tp_check(tp_value, water_type)` | `tp_value`: float, `water_type`: str = "river" | Dict | 总磷检查，区分河流/湖库 |
| `cu_check(cu_value)` | `cu_value`: float | Dict | 铜检查 |
| `zn_check(zn_value)` | `zn_value`: float | Dict | 锌检查 |
| `f_check(f_value)` | `f_value`: float | Dict | 氟化物检查 |
| `se_check(se_value)` | `se_value`: float | Dict | 硒检查 |
| `as_check(as_value)` | `as_value`: float | Dict | 砷检查 |
| `hg_check(hg_value)` | `hg_value`: float | Dict | 汞检查 |
| `cd_check(cd_value)` | `cd_value`: float | Dict | 镉检查 |
| `cr_vi_check(cr_vi_value)` | `cr_vi_value`: float | Dict | 六价铬检查 |
| `pb_check(pb_value)` | `pb_value`: float | Dict | 铅检查 |
| `cn_check(cn_value)` | `cn_value`: float | Dict | 氰化物检查 |
| `c6h5oh_check(c6h5oh_value)` | `c6h5oh_value`: float | Dict | 挥发酚检查 |
| `phc_check(phc_value)` | `phc_value`: float | Dict | 石油类检查 |
| `las_as_check(las_as_value)` | `las_as_value`: float | Dict | 阴离子表面活性剂检查 |
| `s2_h2s_check(s2_h2s_value)` | `s2_h2s_value`: float | Dict | 硫化物检查 |
| `fc_check(fc_value)` | `fc_value`: float | Dict | 粪大肠杆菌检查 |

### 使用示例

```python
from config import WaterQualityConfig, evaluate_water_quality, do_check, ph_check

# 单个参数检查
do_result = do_check(8.0)  # 返回: {"DO": 8.0, "result": "Ⅰ类", "category": 0}
ph_result = ph_check(7.5)  # 返回: {"pH": 7.5, "result": "pH正常", ...}

# 综合评价
sample_data = {
    "current_temp": 25.0,
    "last_temp": 24.5,
    "pH": 7.5,
    "DO": 8.0,
    "CODMn": 3.0,
    "TP": 0.15
}
result = evaluate_water_quality(sample_data, "river")
# 返回: {
#   "overall_result": "Ⅲ类",
#   "category": 2,
#   "worst_param": "TP",
#   "details": {...}
# }

# 访问配置参数
print(f"pH允许范围: {WaterQualityConfig.MIN_PH} - {WaterQualityConfig.MAX_PH}")
```

### 集成到其他项目

1. **单独使用评价功能**：
```python
from config import evaluate_water_quality

def your_water_quality_function(data):
    result = evaluate_water_quality(data, "river")
    return result["overall_result"]
```

2. **自定义配置**：
```python
from config import WaterQualityConfig

# 修改阈值
WaterQualityConfig.TEMP_RISE_THRESHOLD = 1.5  # 调整升温阈值
```

## 🎯 使用指南

### 首次使用
1. 启动程序后，系统自动创建数据库
2. 在"单次监测"页面录入监测数据
3. 系统自动进行水质评价并保存结果

### 数据录入
- **单次录入**：在"单次监测"页面逐项填写参数
- **批量导入**：下载Excel模板，填写数据后批量导入

### 数据分析
- 在"分析报告"页面查看各类图表分析
- 支持按监测断面筛选数据
- 图表支持缩放和保存

## 🔧 技术特点

### 核心算法
- 基于GB3838-2002的多参数综合评价
- 温度变化阈值监控
- pH值范围验证
- 最差参数决定原则

### 数据处理
- SQLite本地数据库存储
- 数据完整性验证
- 异常数据处理机制

### 用户界面
- PyQt6现代化界面
- 响应式布局设计
- 实时数据验证
- 直观的状态反馈

## 📊 水质标准

系统支持以下水质参数的监测与评价：

| 参数类别 | 包含参数 |
|---------|---------|
| 基本参数 | pH、溶解氧(DO)、水温 |
| 有机污染物 | 高锰酸盐指数(CODMn)、化学需氧量(COD)、五日生化需氧量(BOD5) |
| 营养盐 | 氨氮(NH₄-N)、总氮(TN)、总磷(TP) |
| 重金属 | 铜(Cu)、锌(Zn)、汞(Hg)、镉(Cd)等 |
| 其他参数 | 氟化物、挥发酚、石油类等 |

## 🐛 问题反馈

如果您在使用过程中遇到任何问题，请通过以下方式联系：

- 📧 **邮箱**: [3478584509@qq.com]
- 🐛 **GitHub Issues**: [提交问题](https://github.com/hbt123-123/GB3838-2002/issues)

## 🤝 贡献指南

我们欢迎各种形式的贡献！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request


## 📞 联系方式

- 🌐 **GitHub**: [https://github.com/hbt123-123](https://github.com/hbt123-123)
- 🌐 **HuggingFace**: [https://huggingface.co/firefly123firefly](https://huggingface.co/firefly123firefly)
- 🌐 **ModelScope**: [https://www.modelscope.cn/profile/firefly123123](https://www.modelscope.cn/profile/firefly123123)

---

**注意**: 本软件仅供学习和研究使用，实际水质监测请以官方监测机构的检测结果为准。
