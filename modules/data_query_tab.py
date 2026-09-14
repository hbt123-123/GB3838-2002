# modules/data_query_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QDateEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel
)
from PyQt6.QtCore import QDate
from modules.database import DatabaseManager

class DataQueryTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        # 查询条件区域
        query_group = QGroupBox("查询条件")
        query_layout = QFormLayout(query_group)
        # 日期范围
        date_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(QLabel("开始日期:"))
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(QLabel("结束日期:"))
        date_layout.addWidget(self.end_date_edit)
        query_layout.addRow("日期范围:", date_layout)

        # 监测断面
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("可选，模糊匹配")
        query_layout.addRow("监测断面:", self.location_edit)

        # 水质类别
        self.category_combo = QComboBox()
        self.category_combo.addItems(["全部", "Ⅰ类", "Ⅱ类", "Ⅲ类", "Ⅳ类", "Ⅴ类", "劣Ⅴ类"])
        query_layout.addRow("水质类别:", self.category_combo)

        # 查询按钮
        self.query_btn = QPushButton("查询")
        self.query_btn.clicked.connect(self.query_data)
        query_layout.addRow(self.query_btn)
        layout.addWidget(query_group)

        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.result_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.result_table)

        # 操作按钮区域
        action_group = QGroupBox("操作")
        action_layout = QHBoxLayout(action_group)
        self.delete_btn = QPushButton("删除选中行")
        self.delete_btn.clicked.connect(self.delete_selected_rows)
        action_layout.addWidget(self.delete_btn)
        action_layout.addStretch()
        layout.addWidget(action_group)

        # 初始化表格
        self.init_table()
        # 初始查询
        self.query_data()

    def init_table(self):
        """初始化表格"""
        headers = [
            "ID", "时间", "监测断面", "温度", "pH", "DO", "CODMn",
            "BOD5", "NH₄-N", "TP", "总体类别"
        ]
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)
        # 设置列宽
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def query_data(self):
        """查询数据"""
        filters = {}
        # 日期范围
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        filters['date_range'] = (start_date, end_date)
        # 监测断面
        location = self.location_edit.text().strip()
        if location:
            filters['location'] = location
        # 水质类别
        category = self.category_combo.currentText()
        if category != "全部":
            filters['category'] = category

        try:
            results = self.db_manager.get_monitoring_data(filters)
            # 更新表格
            self.result_table.setRowCount(len(results))
            self.query_results = results # 存储查询结果以便删除时使用
            for row, record in enumerate(results):
                self.result_table.setItem(row, 0, QTableWidgetItem(str(record['id'])))
                self.result_table.setItem(row, 1, QTableWidgetItem(str(record['timestamp'])))
                self.result_table.setItem(row, 2, QTableWidgetItem(str(record['location'] or '')))
                self.result_table.setItem(row, 3, QTableWidgetItem(str(record['temperature'] or '')))
                self.result_table.setItem(row, 4, QTableWidgetItem(str(record['ph'] or '')))
                self.result_table.setItem(row, 5, QTableWidgetItem(str(record['do_value'] or '')))
                self.result_table.setItem(row, 6, QTableWidgetItem(str(record['codmn_value'] or '')))
                self.result_table.setItem(row, 7, QTableWidgetItem(str(record['bod5_value'] or '')))
                self.result_table.setItem(row, 8, QTableWidgetItem(str(record['nh4_n_value'] or '')))
                self.result_table.setItem(row, 9, QTableWidgetItem(str(record['tp_value'] or '')))
                self.result_table.setItem(row, 10, QTableWidgetItem(str(record['overall_category'] or '')))
            print(f"查询到 {len(results)} 条记录。")
        except Exception as e:
            print(f"查询数据失败: {str(e)}")

    def delete_selected_rows(self):
        """删除选中的行"""
        selected_rows = self.result_table.selectionModel().selectedRows()
        if not selected_rows:
            print("未选择任何行。")
            return

        # 获取选中行的ID
        ids_to_delete = []
        for row_index in selected_rows:
            row = row_index.row()
            # 从存储的查询结果中获取对应的ID
            if row < len(self.query_results):
                record_id = self.query_results[row]['id']
                ids_to_delete.append(record_id)

        if not ids_to_delete:
            print("无法获取选中行的ID。")
            return

        # 从数据库删除
        self.db_manager.delete_monitoring_data(ids_to_delete)
        print(f"已删除 {len(ids_to_delete)} 条记录。")
        # 重新查询以更新表格
        self.query_data()