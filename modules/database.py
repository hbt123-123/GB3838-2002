# modules/database.py
import sqlite3
import os
from datetime import datetime
from config import WaterQualityConfig

class DatabaseManager:
    def __init__(self, db_path="water_quality.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 创建监测数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                location TEXT NOT NULL,
                temperature REAL,
                last_temperature REAL,
                ph REAL,
                do_value REAL,
                codmn_value REAL,
                cod_value REAL,
                bod5_value REAL,
                nh4_n_value REAL,
                tp_value REAL,
                tn_value REAL,
                cu_value REAL,
                zn_value REAL,
                f_value REAL,
                se_value REAL,
                as_value REAL,
                hg_value REAL,
                cd_value REAL,
                cr_vi_value REAL,
                pb_value REAL,
                cn_value REAL,
                c6h5oh_value REAL,
                phc_value REAL,
                las_as_value REAL,
                s2_h2s_value REAL,
                fc_value REAL,
                water_type TEXT DEFAULT 'river',
                temp_result TEXT,
                ph_result TEXT,
                overall_category TEXT,
                notes TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_monitoring_data(self, data):
        """插入监测数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 检查是否包含timestamp，如果没有则使用默认值
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        column_str = ', '.join(columns)
        cursor.execute(f'''
            INSERT INTO monitoring_data ({column_str})
            VALUES ({placeholders})
        ''', list(data.values()))
        conn.commit()
        conn.close()

    def get_monitoring_data(self, filters=None):
        """获取监测数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT * FROM monitoring_data"
        params = []
        if filters:
            conditions = []
            for key, value in filters.items():
                if key == 'date_range':
                    start_date, end_date = value
                    conditions.append("(timestamp >= ? AND timestamp <= ?)")
                    params.extend([start_date, end_date])
                elif key == 'location':
                    conditions.append("location LIKE ?")
                    params.append(f"%{value}%")
                elif key == 'category':
                    conditions.append("overall_category = ?")
                    params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY timestamp DESC"
        cursor.execute(query, params)
        results = cursor.fetchall()
        # 获取列名
        columns = [description[0] for description in cursor.description]
        conn.close()
        # 转换为字典列表
        return [dict(zip(columns, row)) for row in results]

    def get_water_category_stats(self):
        """获取水质类别统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT overall_category, COUNT(*) FROM monitoring_data GROUP BY overall_category")
        results = cursor.fetchall()
        conn.close()
        return dict(results)

    # --- 添加删除功能 ---
    def delete_monitoring_data(self, ids):
        """根据ID列表删除监测数据"""
        if not ids:
            return
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 使用 ? 占位符防止SQL注入
        placeholders = ','.join('?' * len(ids))
        cursor.execute(f"DELETE FROM monitoring_data WHERE id IN ({placeholders})", ids)
        conn.commit()
        conn.close()
        print(f"已从数据库删除 {len(ids)} 条记录 (ID: {ids})")
    # --- 添加删除功能 ---