# modules/batch_import_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QComboBox, QGridLayout, QAbstractItemView
)
import sqlite3 # 导入sqlite3以处理数据库连接
# --- 添加/更新映射字典 ---
# 将英文字段名映射到中文标签 (包含所有数据库字段)
FIELD_NAME_MAP = {
    'location': '监测断面',
    'timestamp': '时间',
    'temperature': '温度',
    'last_temperature': '上次温度',
    'ph': 'pH',
    'do_value': '溶解氧',
    'codmn_value': '高锰酸盐指数',
    'cod_value': '化学需氧量',
    'bod5_value': '五日生化需氧量',
    'nh4_n_value': '氨氮',
    'tp_value': '总磷',
    'tn_value': '总氮',
    'cu_value': '铜',
    'zn_value': '锌',
    'f_value': '氟化物',
    'se_value': '硒',
    'as_value': '砷',
    'hg_value': '汞',
    'cd_value': '镉',
    'cr_vi_value': '六价铬',
    'pb_value': '铅',
    'cn_value': '氰化物',
    'c6h5oh_value': '挥发酚',
    'phc_value': '石油类',
    'las_as_value': '阴离子表面活性剂',
    's2_h2s_value': '硫化物',
    'fc_value': '粪大肠杆菌',
    'water_type': '水体类型',
    'temp_result': '温度检查结果', # 通常不从Excel导入
    'ph_result': 'pH检查结果',     # 通常不从Excel导入
    'overall_category': '总体类别', # 通常不从Excel导入
    'notes': '备注'
}
# 反向映射：中文标签 -> 英文字段名
REVERSE_FIELD_NAME_MAP = {v: k for k, v in FIELD_NAME_MAP.items()}
# --- 添加/更新映射字典 ---
from modules.database import DatabaseManager

class BatchImportTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.data = None
        self.column_mapping = {} # 存储英文字段名 -> Excel列名
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 文件选择区域
        file_group = QGroupBox("Excel文件导入")
        file_layout = QHBoxLayout(file_group)
        self.file_label = QLabel("请选择Excel文件...")
        file_layout.addWidget(self.file_label)
        self.select_file_btn = QPushButton("选择文件")
        self.select_file_btn.clicked.connect(self.select_excel_file)
        file_layout.addWidget(self.select_file_btn)
        self.load_file_btn = QPushButton("加载数据")
        self.load_file_btn.clicked.connect(self.load_excel_data)
        file_layout.addWidget(self.load_file_btn)
        # --- 添加关闭文件按钮 ---
        self.close_file_btn = QPushButton("关闭文件")
        self.close_file_btn.clicked.connect(self.close_file)
        self.close_file_btn.setEnabled(False) # 初始禁用
        file_layout.addWidget(self.close_file_btn)
        # --- 添加关闭文件按钮 ---
        layout.addWidget(file_group)

        # 列映射区域
        mapping_group = QGroupBox("列映射设置")
        self.mapping_layout = QGridLayout(mapping_group)
        layout.addWidget(mapping_group)

        # 数据预览区域
        preview_group = QGroupBox("数据预览")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_table = QTableWidget()
        self.preview_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        preview_layout.addWidget(self.preview_table)
        layout.addWidget(preview_group)

        # 操作按钮
        action_layout = QHBoxLayout()
        self.import_btn = QPushButton("开始导入")
        self.import_btn.clicked.connect(self.import_data)
        action_layout.addWidget(self.import_btn)
        self.download_template_btn = QPushButton("下载模板")
        self.download_template_btn.clicked.connect(self.download_template)
        action_layout.addWidget(self.download_template_btn)
        action_layout.addStretch()
        layout.addLayout(action_layout)

    def select_excel_file(self):
        """选择Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"已选择: {file_path}")

    def load_excel_data(self):
        """加载Excel数据"""
        if not hasattr(self, 'file_path'):
            return
        try:
            self.data = pd.read_excel(self.file_path)
            self.update_preview_table()
            self.create_column_mapping_ui()
            # --- 启用关闭文件按钮 ---
            self.close_file_btn.setEnabled(True)
            # --- 启用关闭文件按钮 ---
        except Exception as e:
            print(f"加载Excel文件失败: {str(e)}")

    def close_file(self):
        """关闭已加载的文件"""
        self.data = None
        self.column_mapping = {}
        self.preview_table.setRowCount(0)
        self.preview_table.setColumnCount(0)
        self.file_label.setText("请选择Excel文件...")
        # 清空映射UI
        for i in reversed(range(self.mapping_layout.count())):
            widget = self.mapping_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # --- 禁用关闭文件按钮 ---
        self.close_file_btn.setEnabled(False)
        # --- 禁用关闭文件按钮 ---
        print("文件已关闭。")

    def update_preview_table(self):
        """更新数据预览表"""
        if self.data is None:
            return

        self.preview_table.setRowCount(min(100, len(self.data)))  # 最多显示100行
        self.preview_table.setColumnCount(len(self.data.columns))

        # 设置列标题
        self.preview_table.setHorizontalHeaderLabels(self.data.columns.tolist())

        # 填充数据
        for row in range(self.preview_table.rowCount()):
            for col in range(self.preview_table.columnCount()):
                value = self.data.iloc[row, col]
                item = QTableWidgetItem(str(value) if not pd.isna(value) else "")
                self.preview_table.setItem(row, col, item)

        # 调整列宽
        header = self.preview_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def create_column_mapping_ui(self):
        """创建列映射界面"""
        # 清空现有布局
        for i in reversed(range(self.mapping_layout.count())):
            widget = self.mapping_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if self.data is None:
            return

        # 水质参数列表 (使用中文，包含所有字段)
        water_params_chinese = list(FIELD_NAME_MAP.values())

        # 为每个参数创建映射选择
        for i, param_chinese in enumerate(water_params_chinese):
            label = QLabel(param_chinese + ":")
            combo = QComboBox()
            combo.addItems([''] + self.data.columns.tolist())
            # 使用闭包确保lambda捕获正确的参数
            combo.currentTextChanged.connect(lambda text, p=param_chinese: self.update_column_mapping(p, text))
            self.mapping_layout.addWidget(label, i // 2, (i % 2) * 2)
            self.mapping_layout.addWidget(combo, i // 2, (i % 2) * 2 + 1)

    def update_column_mapping(self, param_chinese, column):
        """更新列映射 (使用中文标签作为键)"""
        if column:
            # 通过中文标签获取英文字段名
            param_english = REVERSE_FIELD_NAME_MAP.get(param_chinese)
            if param_english:
                self.column_mapping[param_english] = column
        else:
            # 通过中文标签获取英文字段名，然后从映射中删除
            param_english = REVERSE_FIELD_NAME_MAP.get(param_chinese)
            if param_english and param_english in self.column_mapping:
                del self.column_mapping[param_english]

    def import_data(self):
        """导入数据到数据库"""
        if self.data is None or not self.column_mapping:
            print("没有数据或未设置列映射，无法导入。")
            return

        # 修复：在循环外打开数据库连接
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        successful_records = 0
        try:
            for index, row in self.data.iterrows():
                data_record = {}
                for param_english, column in self.column_mapping.items():
                    if column in row:
                        value = row[column]
                        if pd.isna(value): # 修复：处理NaN
                            # 修复：为location设置默认值
                            if param_english == 'location':
                                data_record[param_english] = '未知断面'
                            else:
                                data_record[param_english] = None
                        else:
                            # 对于location等字符串字段，不转换为float
                            if param_english in ['location', 'water_type', 'overall_category', 'temp_result', 'ph_result', 'notes']:
                                data_record[param_english] = str(value)
                            elif param_english == 'timestamp': # 特殊处理时间
                                try:
                                    # 尝试解析时间，支持多种常见格式
                                    parsed_time = pd.to_datetime(value, errors='coerce') # errors='coerce' 会将无法解析的设为NaT
                                    if pd.notna(parsed_time):
                                        data_record[param_english] = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
                                    else:
                                        print(f"警告: 行 {index}, 列 '{column}' 的时间值 '{value}' 无法解析，已跳过。")
                                        data_record[param_english] = None
                                except Exception as parse_error:
                                    print(f"警告: 行 {index}, 列 '{column}' 的时间值 '{value}' 解析时出错 ({parse_error})，已跳过。")
                                    data_record[param_english] = None
                            else:
                                try:
                                    data_record[param_english] = float(value)
                                except (ValueError, TypeError):
                                    print(f"警告: 行 {index}, 列 '{column}' 的值 '{value}' 无法转换为浮点数，已跳过或设置为None。")
                                    data_record[param_english] = None # 无法转换则设为None

                # 添加默认值 (如果映射中没有提供)
                if 'water_type' not in data_record:
                    data_record['water_type'] = 'river'
                if 'notes' not in data_record:
                    data_record['notes'] = ''

                # 注意：temp_result, ph_result, overall_category 通常不由导入决定，这里不设默认值
                # 检查是否必须字段有值
                if data_record.get('location') is None:
                     print(f"警告: 行 {index} 的location为空或无效，跳过此记录。")
                     continue # 跳过此记录

                # 插入数据库
                try:
                    # 构建插入语句和参数
                    valid_columns = {'location', 'timestamp', 'temperature', 'last_temperature', 'ph', 'do_value',
                                     'codmn_value', 'cod_value', 'bod5_value', 'nh4_n_value', 'tp_value',
                                     'tn_value', 'cu_value', 'zn_value', 'f_value', 'se_value', 'as_value',
                                     'hg_value', 'cd_value', 'cr_vi_value', 'pb_value', 'cn_value',
                                     'c6h5oh_value', 'phc_value', 'las_as_value', 's2_h2s_value', 'fc_value',
                                     'water_type', 'temp_result', 'ph_result', 'overall_category', 'notes'}
                    columns = [c for c in data_record.keys() if c in valid_columns]
                    placeholders = ', '.join(['?' for _ in columns])
                    column_str = ', '.join(columns)
                    sql = f"INSERT INTO monitoring_data ({column_str}) VALUES ({placeholders})"
                    cursor.execute(sql, list(data_record.values()))
                    successful_records += 1
                except sqlite3.Error as e: # 修复：捕获更具体的错误
                    print(f"插入记录 {index} 失败: {str(e)}")
                    # conn.rollback() # 可选：如果需要，可以回滚失败的事务
                except Exception as e:
                    print(f"插入记录 {index} 时发生未知错误: {str(e)}")

            # 修复：在循环结束后提交事务并关闭连接
            conn.commit()
            print(f"成功导入 {successful_records}/{len(self.data)} 条记录")
        except Exception as e:
            print(f"导入数据过程中发生错误: {str(e)}")
            conn.rollback() # 发生错误时回滚
        finally:
            conn.close() # 确保连接关闭

    def download_template(self):
        """下载Excel模板"""
        import os
        template_path = "water_quality_template.xlsx"
        # 创建模板数据 (包含更多字段)
        template_data = {
            'location': ['监测断面A', '监测断面B'],
            'timestamp': ['2023-10-01 10:00:00', '2023-10-01 11:00:00'],
            'temperature': [25.0, 24.5],
            'last_temperature': [24.8, 24.0],
            'ph': [7.2, 6.8],
            'do_value': [8.5, 7.2],
            'codmn_value': [2.1, 3.5],
            'cod_value': [18, 25],
            'bod5_value': [3.2, 4.1],
            'nh4_n_value': [0.2, 0.8],
            'tp_value': [0.05, 0.12],
            'tn_value': [0.8, 1.2],
            'water_type': ['river', 'lake'],
            'notes': ['第一次采样', '第二次采样']
        }
        df = pd.DataFrame(template_data)
        df.to_excel(template_path, index=False)
        print(f"模板已保存到: {template_path}")
