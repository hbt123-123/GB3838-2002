# modules/analysis_report_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTabWidget,
    QPushButton, QLabel, QScrollArea, QComboBox
)
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
except Exception:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans'] # 优先使用黑体，备选DejaVu Sans
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


from modules.database import DatabaseManager

class AnalysisReportTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # --- 添加监测断面选择 ---
        filter_group = QGroupBox("筛选条件")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.addWidget(QLabel("监测断面:"))
        self.location_combo = QComboBox()
        self.location_combo.addItems(["全部"]) # 默认添加“全部”
        self.location_combo.currentTextChanged.connect(self.on_location_changed)
        filter_layout.addWidget(self.location_combo)
        filter_layout.addStretch()
        layout.addWidget(filter_group)
        # --- 添加监测断面选择 ---

        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 趋势分析页
        self.trend_widget = self.create_trend_analysis()
        self.tab_widget.addTab(self.trend_widget, "趋势分析")
        
        # 类别分布页
        self.distribution_widget = self.create_distribution_analysis()
        self.tab_widget.addTab(self.distribution_widget, "类别分布")
        
        # 参数对比页
        self.comparison_widget = self.create_comparison_analysis()
        self.tab_widget.addTab(self.comparison_widget, "参数对比")
        
        layout.addWidget(self.tab_widget)

        # --- 移除生成报告按钮 ---
        # report_layout = QHBoxLayout()
        # self.generate_report_btn = QPushButton("生成PDF报告")
        # self.generate_report_btn.clicked.connect(self.generate_pdf_report)
        # report_layout.addWidget(self.generate_report_btn)
        # report_layout.addStretch()
        # layout.addLayout(report_layout)
        # --- 移除生成报告按钮 ---

    def create_trend_analysis(self):
        """创建趋势分析页面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.trend_fig = Figure(figsize=(12, 6), dpi=100)
        self.trend_canvas = FigureCanvas(self.trend_fig)
        layout.addWidget(self.trend_canvas)
        return widget

    def create_distribution_analysis(self):
        """创建分布分析页面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.dist_fig = Figure(figsize=(10, 6), dpi=100)
        self.dist_canvas = FigureCanvas(self.dist_fig)
        layout.addWidget(self.dist_canvas)
        return widget

    def create_comparison_analysis(self):
        """创建对比分析页面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.comp_fig = Figure(figsize=(12, 8), dpi=100)
        self.comp_canvas = FigureCanvas(self.comp_fig)
        layout.addWidget(self.comp_canvas)
        return widget

    def load_data(self):
        """加载数据并绘制图表"""
        try:
            # 获取所有数据
            all_data = self.db_manager.get_monitoring_data()
            if not all_data:
                print("数据库中没有数据，无法生成分析图表。")
                self._show_no_data_message(self.trend_fig, "趋势分析")
                self._show_no_data_message(self.dist_fig, "类别分布")
                self._show_no_data_message(self.comp_fig, "参数对比")
                self.update_location_combo(all_data) # 更新下拉框选项
                return

            # 更新监测断面下拉框
            self.update_location_combo(all_data)

            # 绘制图表（使用全部数据）
            self.plot_trend_analysis(all_data)
            self.plot_distribution_analysis()
            self.plot_comparison_analysis(all_data)
        except Exception as e:
            print(f"加载数据或绘制图表失败: {str(e)}")

    def update_location_combo(self, data):
        """更新监测断面下拉框"""
        locations = set(item.get('location', '未知断面') or '未知断面' for item in data)
        self.location_combo.clear()
        self.location_combo.addItem("全部")
        self.location_combo.addItems(sorted(locations))

    def on_location_changed(self):
        """当监测断面选择改变时，重新加载数据"""
        selected_location = self.location_combo.currentText()
        try:
            all_data = self.db_manager.get_monitoring_data()
            if selected_location == "全部":
                data_to_plot = all_data
            else:
                data_to_plot = [item for item in all_data if item.get('location', '未知断面') == selected_location]

            if not data_to_plot:
                print(f"监测断面 '{selected_location}' 没有数据。")
                self._show_no_data_message(self.trend_fig, "趋势分析")
                self._show_no_data_message(self.dist_fig, "类别分布")
                self._show_no_data_message(self.comp_fig, "参数对比")
            else:
                # 重新绘制图表
                self.plot_trend_analysis(data_to_plot)
                self.plot_distribution_analysis(data_to_plot)
                self.plot_comparison_analysis(data_to_plot)

        except Exception as e:
            print(f"根据监测断面筛选数据失败: {str(e)}")


    def _show_no_data_message(self, fig, title):
        """在图表上显示无数据消息"""
        fig.clear()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, '无数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=14)
        ax.set_title(title)
        ax.axis('off') # 关闭坐标轴
        # 需要手动调用draw，但注意传入的是对应的canvas
        # 这个函数只负责清理和设置提示，实际draw在调用它的函数里完成
        # 因为这里不知道具体是哪个canvas，所以不直接draw

    def plot_trend_analysis(self, data):
        """绘制趋势分析图"""
        self.trend_fig.clear()
        ax = self.trend_fig.add_subplot(111)
        
        # 准备数据
        timestamps = [item['timestamp'] for item in data]
        do_values = [item['do_value'] for item in data if item['do_value'] is not None]
        ph_values = [item['ph'] for item in data if item['ph'] is not None]
        codmn_values = [item['codmn_value'] for item in data if item['codmn_value'] is not None]

        # 绘制多条线（确保时间戳和值长度一致）
        if len(do_values) > 0:
            ax.plot(timestamps[:len(do_values)], do_values, label='DO (mg/L)', marker='o', linestyle='-')
        if len(ph_values) > 0:
            ax.plot(timestamps[:len(ph_values)], ph_values, label='pH', marker='s', linestyle='--')
        if len(codmn_values) > 0:
            ax.plot(timestamps[:len(codmn_values)], codmn_values, label='CODMn (mg/L)', marker='^', linestyle='-.')
            
        ax.set_xlabel('时间')
        ax.set_ylabel('数值')
        ax.set_title('水质参数趋势分析')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        self.trend_fig.autofmt_xdate() # 自动格式化x轴日期
        self.trend_canvas.draw()

    def plot_distribution_analysis(self, data):
        """绘制类别分布饼图 (根据筛选后的数据)"""
        self.dist_fig.clear()
        ax = self.dist_fig.add_subplot(111)

        # 统计筛选后数据的类别分布
        category_counts = {}
        for item in data:
            cat = item.get('overall_category')
            if cat is not None:
                category_counts[cat] = category_counts.get(cat, 0) + 1

        if category_counts:
            categories = list(category_counts.keys())
            counts = list(category_counts.values())
            ax.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90)
            ax.set_title('水质类别分布')
        else:
            ax.text(0.5, 0.5, '无有效数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.set_title('水质类别分布')
        
        self.dist_canvas.draw()

    def plot_comparison_analysis(self, data):
        """绘制参数对比柱状图 (根据筛选后的数据)"""
        self.comp_fig.clear()
        ax = self.comp_fig.add_subplot(111)
        
        # 统计各监测断面的平均值 (这里显示的是筛选后的数据，如果筛选为特定断面，则只显示该断面)
        # 为了更有意义，我们只在未筛选（全部）时显示对比
        selected_location = self.location_combo.currentText()
        if selected_location == "全部":
            locations = {}
            for item in data:
                loc = item.get('location', '未知断面') or '未知断面' # 处理None值
                if loc not in locations:
                    locations[loc] = {'do': [], 'ph': [], 'codmn': []}
                if item.get('do_value') is not None:
                    locations[loc]['do'].append(item['do_value'])
                if item.get('ph') is not None:
                    locations[loc]['ph'].append(item['ph'])
                if item.get('codmn_value') is not None:
                    locations[loc]['codmn'].append(item['codmn_value'])

            # 计算平均值
            avg_data = {}
            for loc, values in locations.items():
                avg_data[loc] = {
                    'do': sum(values['do']) / len(values['do']) if values['do'] else 0,
                    'ph': sum(values['ph']) / len(values['ph']) if values['ph'] else 0,
                    'codmn': sum(values['codmn']) / len(values['codmn']) if values['codmn'] else 0,
                }

            if avg_data:
                locations_list = list(avg_data.keys())
                do_values = [avg_data[loc]['do'] for loc in locations_list]
                ph_values = [avg_data[loc]['ph'] for loc in locations_list]
                codmn_values = [avg_data[loc]['codmn'] for loc in locations_list]

                x = range(len(locations_list))
                width = 0.25

                ax.bar([i - width for i in x], do_values, width, label='DO (mg/L)', alpha=0.8)
                ax.bar([i for i in x], ph_values, width, label='pH', alpha=0.8)
                ax.bar([i + width for i in x], codmn_values, width, label='CODMn (mg/L)', alpha=0.8)

                ax.set_xlabel('监测断面')
                ax.set_ylabel('平均值')
                ax.set_title('各监测断面参数对比')
                ax.set_xticks(x)
                ax.set_xticklabels(locations_list, rotation=45, ha="right") # ha="right" 使旋转的标签靠右对齐
                ax.legend()
                ax.grid(True, axis='y', linestyle='--', alpha=0.6) # 只在y轴方向显示网格
            else:
                ax.text(0.5, 0.5, '无有效数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                ax.set_title('各监测断面参数对比')
        else:
            # 如果选择了特定断面，显示该断面各参数的平均值
            avg_data = {'selected': {'do': 0, 'ph': 0, 'codmn': 0}}
            total_do, total_ph, total_codmn = 0, 0, 0
            count_do, count_ph, count_codmn = 0, 0, 0
            for item in data:
                if item.get('do_value') is not None:
                    total_do += item['do_value']
                    count_do += 1
                if item.get('ph') is not None:
                    total_ph += item['ph']
                    count_ph += 1
                if item.get('codmn_value') is not None:
                    total_codmn += item['codmn_value']
                    count_codmn += 1
            avg_data['selected']['do'] = total_do / count_do if count_do > 0 else 0
            avg_data['selected']['ph'] = total_ph / count_ph if count_ph > 0 else 0
            avg_data['selected']['codmn'] = total_codmn / count_codmn if count_codmn > 0 else 0

            if any(v > 0 for v in avg_data['selected'].values()):
                params = list(avg_data['selected'].keys())
                values = list(avg_data['selected'].values())

                ax.bar(params, values, alpha=0.8)
                ax.set_ylabel('平均值')
                ax.set_title(f'监测断面 "{selected_location}" 参数分析')
                ax.grid(True, axis='y', linestyle='--', alpha=0.6)
            else:
                ax.text(0.5, 0.5, '无有效数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                ax.set_title(f'监测断面 "{selected_location}" 参数分析')

        self.comp_canvas.draw()

