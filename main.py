# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QStatusBar # 移除了 QMenuBar, QToolBar
from modules.monitoring_tab import MonitoringTab
from modules.batch_import_tab import BatchImportTab
from modules.data_query_tab import DataQueryTab
from modules.analysis_report_tab import AnalysisReportTab
from modules.database import DatabaseManager

class WaterQualityMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("水质监测分析系统")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        # 添加标签页
        self.monitoring_tab = MonitoringTab(self.db_manager)
        self.batch_import_tab = BatchImportTab(self.db_manager)
        self.data_query_tab = DataQueryTab(self.db_manager)
        self.analysis_report_tab = AnalysisReportTab(self.db_manager)

        self.tab_widget.addTab(self.monitoring_tab, "单次监测")
        self.tab_widget.addTab(self.batch_import_tab, "批量导入")
        self.tab_widget.addTab(self.data_query_tab, "数据查询")
        self.tab_widget.addTab(self.analysis_report_tab, "分析报告")

        # 布局
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.tab_widget)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")


def main():
    app = QApplication(sys.argv)
    window = WaterQualityMonitorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
