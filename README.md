# GB3838-2002
地表水环境质量标准

# 水质监测分析系统 (Water Quality Monitoring System)

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
