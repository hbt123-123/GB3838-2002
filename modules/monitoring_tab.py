# modules/monitoring_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit,
    QScrollArea, QFrame, QGridLayout, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPalette, QDoubleValidator  # 修复：添加验证器导入
from config import (
    WaterQualityConfig, temperature_check, ph_check,
    do_check, codmn_check, cod_check, bod5_check, nh4_n_check,
    tp_check, parameter_check, evaluate_water_quality  # 修复：添加缺失的导入
)
from modules.database import DatabaseManager

class MonitoringTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout(self)
        # 主滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        # --- 添加时间输入 ---
        time_group = QGroupBox("时间信息")
        time_layout = QFormLayout(time_group)
        self.timestamp_edit = QDateTimeEdit()
        self.timestamp_edit.setDateTime(QDateTime.currentDateTime())
        self.timestamp_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        time_layout.addRow("监测时间:", self.timestamp_edit)
        scroll_layout.addWidget(time_group)
        # --- 添加时间输入 ---
        # 监测断面信息
        self.create_location_section(scroll_layout)
        # 水温处理（特殊处理）
        self.create_temperature_section(scroll_layout)
        # 基本参数
        self.create_basic_params_section(scroll_layout)
        # 有机污染物
        self.create_organic_params_section(scroll_layout)
        # 重金属参数
        self.create_heavy_metal_section(scroll_layout)
        # 其他参数
        self.create_other_params_section(scroll_layout)
        # 水质类型选择
        self.create_water_type_section(scroll_layout)
        # 评价结果
        self.create_evaluation_section(scroll_layout)
        # 操作按钮
        self.create_action_buttons(scroll_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def create_location_section(self, parent_layout):
        group = QGroupBox("监测断面信息")
        layout = QFormLayout(group)
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("请输入监测断面名称")
        layout.addRow("监测断面:", self.location_edit)
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        self.notes_edit.setPlaceholderText("备注信息...")
        layout.addRow("备注:", self.notes_edit)
        parent_layout.addWidget(group)

    def create_temperature_section(self, parent_layout):
        group = QGroupBox("水温监测（特殊处理）")
        layout = QFormLayout(group)
        temp_layout = QHBoxLayout()
        self.current_temp_edit = QLineEdit()
        self.current_temp_edit.setPlaceholderText("当前温度")
        # 设置浮点数验证器
        validator = QDoubleValidator()
        self.current_temp_edit.setValidator(validator)
        temp_layout.addWidget(QLabel("当前温度:"))
        temp_layout.addWidget(self.current_temp_edit)
        self.last_temp_edit = QLineEdit()
        self.last_temp_edit.setPlaceholderText("上次温度")
        self.last_temp_edit.setValidator(validator)
        temp_layout.addWidget(QLabel("上次温度:"))
        temp_layout.addWidget(self.last_temp_edit)
        layout.addRow(temp_layout)
        # 温度变化结果显示
        self.temp_result_label = QLabel("等待输入...")
        self.temp_result_label.setStyleSheet("color: blue;")
        layout.addRow("温度检查结果:", self.temp_result_label)
        parent_layout.addWidget(group)

    def create_basic_params_section(self, parent_layout):
        group = QGroupBox("基本水质参数")
        layout = QGridLayout(group)
        # pH值
        self.ph_edit = QLineEdit()
        self.ph_edit.setPlaceholderText("6.0-9.0")
        self.ph_edit.setValidator(QDoubleValidator(0.0, 14.0, 2))  # pH范围0-14
        layout.addWidget(QLabel("pH值:"), 0, 0)
        layout.addWidget(self.ph_edit, 0, 1)
        self.ph_result_label = QLabel("未检测")
        layout.addWidget(self.ph_result_label, 0, 2)
        # 溶解氧
        self.do_edit = QLineEdit()
        self.do_edit.setPlaceholderText("mg/L")
        self.do_edit.setValidator(QDoubleValidator(0.0, 20.0, 2))
        layout.addWidget(QLabel("溶解氧(DO):"), 1, 0)
        layout.addWidget(self.do_edit, 1, 1)
        self.do_result_label = QLabel("未检测")
        layout.addWidget(self.do_result_label, 1, 2)
        parent_layout.addWidget(group)

    def create_organic_params_section(self, parent_layout):
        group = QGroupBox("有机污染物参数")
        layout = QGridLayout(group)
        # 高锰酸盐指数
        self.codmn_edit = QLineEdit()
        self.codmn_edit.setPlaceholderText("mg/L")
        self.codmn_edit.setValidator(QDoubleValidator(0.0, 100.0, 2))
        layout.addWidget(QLabel("高锰酸盐指数(CODMn):"), 0, 0)
        layout.addWidget(self.codmn_edit, 0, 1)
        self.codmn_result_label = QLabel("未检测")
        layout.addWidget(self.codmn_result_label, 0, 2)
        # 化学需氧量
        self.cod_edit = QLineEdit()
        self.cod_edit.setPlaceholderText("mg/L")
        self.cod_edit.setValidator(QDoubleValidator(0.0, 500.0, 2))
        layout.addWidget(QLabel("化学需氧量(COD):"), 1, 0)
        layout.addWidget(self.cod_edit, 1, 1)
        self.cod_result_label = QLabel("未检测")
        layout.addWidget(self.cod_result_label, 1, 2)
        # BOD5
        self.bod5_edit = QLineEdit()
        self.bod5_edit.setPlaceholderText("mg/L")
        self.bod5_edit.setValidator(QDoubleValidator(0.0, 100.0, 2))
        layout.addWidget(QLabel("五日生化需氧量(BOD5):"), 2, 0)
        layout.addWidget(self.bod5_edit, 2, 1)
        self.bod5_result_label = QLabel("未检测")
        layout.addWidget(self.bod5_result_label, 2, 2)
        parent_layout.addWidget(group)

    def create_heavy_metal_section(self, parent_layout):
        group = QGroupBox("重金属参数")
        layout = QGridLayout(group)
        # 氨氮
        self.nh4_n_edit = QLineEdit()
        self.nh4_n_edit.setPlaceholderText("mg/L")
        self.nh4_n_edit.setValidator(QDoubleValidator(0.0, 10.0, 3))
        layout.addWidget(QLabel("氨氮(NH₄-N):"), 0, 0)
        layout.addWidget(self.nh4_n_edit, 0, 1)
        self.nh4_n_result_label = QLabel("未检测")
        layout.addWidget(self.nh4_n_result_label, 0, 2)
        # 总磷
        self.tp_edit = QLineEdit()
        self.tp_edit.setPlaceholderText("mg/L")
        self.tp_edit.setValidator(QDoubleValidator(0.0, 5.0, 3))
        layout.addWidget(QLabel("总磷(TP):"), 1, 0)
        layout.addWidget(self.tp_edit, 1, 1)
        self.tp_result_label = QLabel("未检测")
        layout.addWidget(self.tp_result_label, 1, 2)
        # 总氮
        self.tn_edit = QLineEdit()
        self.tn_edit.setPlaceholderText("mg/L")
        self.tn_edit.setValidator(QDoubleValidator(0.0, 10.0, 3))
        layout.addWidget(QLabel("总氮(TN):"), 2, 0)
        layout.addWidget(self.tn_edit, 2, 1)
        self.tn_result_label = QLabel("未检测")
        layout.addWidget(self.tn_result_label, 2, 2)
        parent_layout.addWidget(group)

    def create_other_params_section(self, parent_layout):
        group = QGroupBox("其他参数")
        layout = QGridLayout(group)
        # 铜
        self.cu_edit = QLineEdit()
        self.cu_edit.setPlaceholderText("mg/L")
        self.cu_edit.setValidator(QDoubleValidator(0.0, 1.0, 4))
        layout.addWidget(QLabel("铜(Cu):"), 0, 0)
        layout.addWidget(self.cu_edit, 0, 1)
        self.cu_result_label = QLabel("未检测")
        layout.addWidget(self.cu_result_label, 0, 2)
        # 锌
        self.zn_edit = QLineEdit()
        self.zn_edit.setPlaceholderText("mg/L")
        self.zn_edit.setValidator(QDoubleValidator(0.0, 2.0, 4))
        layout.addWidget(QLabel("锌(Zn):"), 1, 0)
        layout.addWidget(self.zn_edit, 1, 1)
        self.zn_result_label = QLabel("未检测")
        layout.addWidget(self.zn_result_label, 1, 2)
        # 汞
        self.hg_edit = QLineEdit()
        self.hg_edit.setPlaceholderText("mg/L")
        self.hg_edit.setValidator(QDoubleValidator(0.0, 0.01, 6))
        layout.addWidget(QLabel("汞(Hg):"), 2, 0)
        layout.addWidget(self.hg_edit, 2, 1)
        self.hg_result_label = QLabel("未检测")
        layout.addWidget(self.hg_result_label, 2, 2)
        parent_layout.addWidget(group)

    def create_water_type_section(self, parent_layout):
        group = QGroupBox("水体类型")
        layout = QHBoxLayout(group)
        self.water_type_combo = QComboBox()
        self.water_type_combo.addItems(["河流", "湖库"])
        layout.addWidget(QLabel("水体类型:"))
        layout.addWidget(self.water_type_combo)
        parent_layout.addWidget(group)

    def create_evaluation_section(self, parent_layout):
        group = QGroupBox("水质评价结果")
        layout = QVBoxLayout(group)
        self.overall_result_label = QLabel("等待评价...")
        self.overall_result_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.overall_result_label)
        parent_layout.addWidget(group)

    def create_action_buttons(self, parent_layout):
        button_layout = QHBoxLayout()
        self.evaluate_btn = QPushButton("实时评价")
        self.evaluate_btn.clicked.connect(self.evaluate_water_quality)
        self.save_btn = QPushButton("保存结果")
        self.save_btn.clicked.connect(self.save_monitoring_data)
        button_layout.addWidget(self.evaluate_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addStretch()
        parent_layout.addLayout(button_layout)

    def setup_connections(self):
        # 连接输入框变化信号到评价函数
        self.current_temp_edit.textChanged.connect(self.update_evaluation)
        self.last_temp_edit.textChanged.connect(self.update_evaluation)
        self.ph_edit.textChanged.connect(self.update_evaluation)
        self.do_edit.textChanged.connect(self.update_evaluation)
        self.codmn_edit.textChanged.connect(self.update_evaluation)
        self.cod_edit.textChanged.connect(self.update_evaluation)
        self.bod5_edit.textChanged.connect(self.update_evaluation)
        self.nh4_n_edit.textChanged.connect(self.update_evaluation)
        self.tp_edit.textChanged.connect(self.update_evaluation)
        self.tn_edit.textChanged.connect(self.update_evaluation)
        self.cu_edit.textChanged.connect(self.update_evaluation)
        self.zn_edit.textChanged.connect(self.update_evaluation)
        self.hg_edit.textChanged.connect(self.update_evaluation)

    def update_evaluation(self):
        """更新评价结果（实时）"""
        QTimer.singleShot(100, self.evaluate_water_quality)  # 防抖

    def evaluate_water_quality(self):
        """评价水质"""
        try:
            # 获取水体类型
            water_type = "river" if self.water_type_combo.currentText() == "河流" else "lake"
            parameters = {}
            # 检查温度
            current_temp_text = self.current_temp_edit.text()
            last_temp_text = self.last_temp_edit.text()
            if current_temp_text and last_temp_text:
                current_temp = float(current_temp_text)
                last_temp = float(last_temp_text)
                temp_result = temperature_check(current_temp, last_temp)
                self.temp_result_label.setText(temp_result["result"])
                parameters["current_temp"] = current_temp
                parameters["last_temp"] = last_temp
                # 如果温度不合格，直接判定为劣Ⅴ类
                if temp_result["result"] == "水温不合格":
                    self.overall_result_label.setText("劣Ⅴ类（水温不合格）")
                    self.overall_result_label.setStyleSheet("color: red; font-weight: bold;")
                    return
            # 检查pH
            ph_text = self.ph_edit.text()
            if ph_text:
                ph_value = float(ph_text)
                ph_result = ph_check(ph_value)
                self.ph_result_label.setText(ph_result["result"])
                parameters["pH"] = ph_value
                # 如果pH不合格，直接判定为劣Ⅴ类
                if ph_result["result"] == "pH不正常":
                    self.overall_result_label.setText("劣Ⅴ类（pH不合格）")
                    self.overall_result_label.setStyleSheet("color: red; font-weight: bold;")
                    return
            # 检查各参数
            param_checks = [
                ('do_edit', 'DO', self.do_edit, self.do_result_label),
                ('codmn_edit', 'CODMn', self.codmn_edit, self.codmn_result_label),
                ('cod_edit', 'COD', self.cod_edit, self.cod_result_label),
                ('bod5_edit', 'BOD5', self.bod5_edit, self.bod5_result_label),
                ('nh4_n_edit', 'NH4_N', self.nh4_n_edit, self.nh4_n_result_label),
                ('tp_edit', 'TP', self.tp_edit, self.tp_result_label),
                ('tn_edit', 'TN', self.tn_edit, self.tn_result_label),
                ('cu_edit', 'CU', self.cu_edit, self.cu_result_label),
                ('zn_edit', 'ZN', self.zn_edit, self.zn_result_label),
                ('hg_edit', 'HG', self.hg_edit, self.hg_result_label),
            ]
            for edit_name, param_name, edit_widget, result_label in param_checks:
                text = edit_widget.text()
                if text:
                    try:
                        value = float(text)
                        if param_name == 'TP':
                            result = parameter_check(param_name, value, water_type)
                        else:
                            result = parameter_check(param_name, value)
                        result_label.setText(result["result"])
                        parameters[param_name] = value
                    except ValueError:
                        result_label.setText("输入错误")
            # 使用综合评价函数
            if parameters:
                evaluation = evaluate_water_quality(parameters, water_type)
                self.overall_result_label.setText(evaluation["overall_result"])
                # 设置颜色
                color_map = {
                    "劣Ⅴ类": "red", "Ⅴ类": "orange", "Ⅳ类": "yellow",
                    "Ⅲ类": "green", "Ⅱ类": "blue", "Ⅰ类": "darkgreen"
                }
                color = color_map.get(evaluation["overall_result"], "black")
                self.overall_result_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            else:
                self.overall_result_label.setText("等待输入...")
                self.overall_result_label.setStyleSheet("color: black; font-weight: normal;")
        except ValueError:
            self.overall_result_label.setText("输入数据格式错误")
            self.overall_result_label.setStyleSheet("color: red; font-weight: bold;")
        except Exception as e:
            self.overall_result_label.setText(f"评价错误: {str(e)}")
            self.overall_result_label.setStyleSheet("color: red; font-weight: bold;")

    def save_monitoring_data(self):
        """保存监测数据"""
        try:
            data = {
                'timestamp': self.timestamp_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"), # --- 添加时间 ---
                'location': self.location_edit.text() or '未知断面',
                'temperature': float(self.current_temp_edit.text()) if self.current_temp_edit.text() else None,
                'last_temperature': float(self.last_temp_edit.text()) if self.last_temp_edit.text() else None,
                'ph': float(self.ph_edit.text()) if self.ph_edit.text() else None,
                'do_value': float(self.do_edit.text()) if self.do_edit.text() else None,
                'codmn_value': float(self.codmn_edit.text()) if self.codmn_edit.text() else None,
                'cod_value': float(self.cod_edit.text()) if self.cod_edit.text() else None,
                'bod5_value': float(self.bod5_edit.text()) if self.bod5_edit.text() else None,
                'nh4_n_value': float(self.nh4_n_edit.text()) if self.nh4_n_edit.text() else None,
                'tp_value': float(self.tp_edit.text()) if self.tp_edit.text() else None,
                'tn_value': float(self.tn_edit.text()) if self.tn_edit.text() else None,
                'cu_value': float(self.cu_edit.text()) if self.cu_edit.text() else None,
                'zn_value': float(self.zn_edit.text()) if self.zn_edit.text() else None,
                'hg_value': float(self.hg_edit.text()) if self.hg_edit.text() else None,
                'water_type': "river" if self.water_type_combo.currentText() == "河流" else "lake",
                'overall_category': self.overall_result_label.text(),
                'notes': self.notes_edit.toPlainText()
            }
            self.db_manager.insert_monitoring_data(data)
            print("数据保存成功！")
        except Exception as e:
            print(f"保存数据失败: {str(e)}")