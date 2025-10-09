# config.py
from typing import Dict, Union

class WaterQualityConfig:
    """水质参数配置类"""
    # 温度变化阈值
    TEMP_RISE_THRESHOLD = 1.0  # 最大升温阈值(℃)
    TEMP_DROP_THRESHOLD = 2.0  # 最大降温阈值(℃)

    # pH范围
    MIN_PH = 6.0
    MAX_PH = 9.0

    # 各类水质参数阈值标准 [Ⅰ类, Ⅱ类, Ⅲ类, Ⅳ类, Ⅴ类]
    # None 表示该类别无此指标或该类别未规定此指标
    PARAMETER_STANDARDS = {
        "DO": [7.5, 6.0, 5.0, 3.0, 2.0],  # 溶解氧 (mg/L) - 数值越高越好
        "CODMn": [2, 4, 6, 10, 15],  # 高锰酸盐指数 (mg/L)
        "COD": [15, 15, 20, 30, 40],  # 化学需氧量 (mg/L) - Ⅰ、Ⅱ类取Ⅱ类标准
        "BOD5": [3, 3, 4, 6, 10],  # 五日生化需氧量 (mg/L) - Ⅰ、Ⅱ类取Ⅱ类标准
        "NH4_N": [0.15, 0.5, 1.0, 1.5, 2.0],  # 氨氮 (mg/L)
        "TN": [0.2, 0.5, 1.0, 1.5, 2.0],  # 总氮 (mg/L)
        "TP": { # 总磷标准（河流/湖库不同） (mg/L)
            "river": [0.02, 0.1, 0.2, 0.3, 0.4],
            "lake": [0.01, 0.025, 0.05, 0.1, 0.2]
        },
        "CU": [0.01, 1.0],  # 铜 (mg/L) - 仅Ⅰ、Ⅱ类标准
        "ZN": [0.05, 1.0, 1.0, 2.0],  # 锌 (mg/L) - Ⅱ、Ⅲ类取Ⅱ类标准
        "F": [1.0, 1.0, 1.0, 1.5],  # 氟化物 (mg/L) - Ⅰ、Ⅱ、Ⅲ类取Ⅰ类标准
        "SE": [0.01, 0.01, 0.01, 0.02],  # 硒 (mg/L) - Ⅰ、Ⅱ、Ⅲ类取Ⅰ类标准
        "AS": [0.05, 0.05, 0.05, 0.1],  # 砷 (mg/L) - Ⅰ、Ⅱ、Ⅲ类取Ⅰ类标准
        "HG": [0.00005, 0.0001, 0.001, 0.001],  # 汞 (mg/L) - Ⅱ、Ⅲ类取Ⅱ类标准
        "CD": [0.001, 0.005, 0.005, 0.01],  # 镉 (mg/L) - Ⅱ、Ⅲ类取Ⅱ类标准
        "CR_VI": [0.01, 0.05, 0.05, 0.1],  # 六价铬 (mg/L) - Ⅱ、Ⅲ类取Ⅱ类标准
        "PB": [0.01, 0.01, 0.05, 0.05, 0.1], # 铅 (mg/L) - Ⅱ、Ⅳ类取Ⅰ、Ⅲ类标准
        "CN": [0.005, 0.05, 0.2],  # 氰化物 (mg/L) - 仅Ⅰ、Ⅱ、Ⅲ类标准
        "C6H5OH": [0.002, 0.002, 0.005, 0.01, 0.1],  # 挥发酚 (mg/L) - Ⅰ、Ⅱ类取Ⅰ类标准
        "PHC": [0.05, 0.05, 0.05, 0.5, 1.0],  # 石油类 (mg/L) - Ⅰ、Ⅱ、Ⅲ类取Ⅰ类标准
        "LAS_AS": [0.2, 0.2, 0.2, 0.3],  # 阴离子表面活性剂 (mg/L) - Ⅰ、Ⅱ、Ⅲ类取Ⅰ类标准
        "S2_H2S": [0.05, 0.1, 0.2, 0.5, 1.0],  # 硫化物 (mg/L)
        "FC": [200, 2000, 10000, 20000, 40000],  # 粪大肠杆菌 (个/L)
    }

def temperature_check(current_temp: float, last_temp: float) -> Dict[str, Union[float, str]]:
    """
    温度变化检查
    若不合格直接判定为劣Ⅴ类水质
    """
    try:
        max_rise = max(0, current_temp - last_temp)
        max_drop = max(0, last_temp - current_temp)
        if max_rise <= WaterQualityConfig.TEMP_RISE_THRESHOLD and max_drop <= WaterQualityConfig.TEMP_DROP_THRESHOLD:
            result = "水温合格"
        else:
            result = "水温不合格"
        return {
            "current_temp": current_temp,
            "last_temp": last_temp,
            "max_rise": max_rise,
            "max_drop": max_drop,
            "result": result
        }
    except (TypeError, ValueError) as e:
        return {"error": f"温度数据错误: {str(e)}", "result": "水温不合格"}

def ph_check(ph_value: float) -> Dict[str, Union[float, str]]:
    """
    pH值检查
    若不合格直接判定为劣Ⅴ类水质
    """
    try:
        if WaterQualityConfig.MIN_PH <= ph_value <= WaterQualityConfig.MAX_PH:
            category = "pH正常"
        else:
            category = "pH不正常"
        return {
            "pH": ph_value,
            "min_pH": WaterQualityConfig.MIN_PH,
            "max_pH": WaterQualityConfig.MAX_PH,
            "result": category
        }
    except (TypeError, ValueError) as e:
        return {"error": f"pH数据错误: {str(e)}", "result": "pH不正常"}

def parameter_check(param_name: str, value: float, water_type: str = "river") -> Dict[str, Union[float, str, int]]:
    """
    通用参数检查函数
    water_type: "river"河流或"lake"湖库（仅对总磷有效）
    """
    try:
        # 特殊处理溶解氧（DO）：数值越高越好
        if param_name == "DO":
            standards = WaterQualityConfig.PARAMETER_STANDARDS["DO"]
            category = 5  # 默认劣Ⅴ类
            for i, threshold in enumerate(standards):
                if threshold is not None and value >= threshold: # 使用 >= 对于DO
                    category = i  # 找到满足的最高标准
                    break # 找到最高满足的类别后退出循环

        # 特殊处理总磷（TP）：根据水体类型
        elif param_name == "TP":
            standards = WaterQualityConfig.PARAMETER_STANDARDS["TP"].get(water_type, WaterQualityConfig.PARAMETER_STANDARDS["TP"]["river"])
            # TP 依然是数值越低越好
            category = 5  # 默认劣Ⅴ类
            for i, threshold in enumerate(standards):
                if threshold is not None and value <= threshold:
                    category = i
                    break

        # 特殊处理化学需氧量（COD）：Ⅰ、Ⅱ类标准相同 (15)，应对应Ⅱ类
        elif param_name == "COD":
            standards = WaterQualityConfig.PARAMETER_STANDARDS["COD"] # [15, 15, 20, 30, 40]
            category = 5  # 默认劣Ⅴ类
            # 找到满足的最小类别索引 (最好的类别)
            best_category = 5 # 初始化为劣Ⅴ类
            for i, threshold in enumerate(standards):
                 if threshold is not None and value <= threshold:
                     best_category = i
                     break # 找到第一个满足的 (最好的) 就停止

            # 检查是否是 COD 的特殊情况 (满足Ⅰ类标准，且Ⅰ、Ⅱ类标准相同)
            if best_category == 0 and len(standards) > 1 and standards[0] == standards[1]:
                # 根据“取Ⅱ类标准”，将类别调整为Ⅱ类
                category = 1
            else:
                category = best_category

        # 特殊处理五日生化需氧量（BOD5）：Ⅰ、Ⅱ类标准相同 (3)，应对应Ⅱ类
        elif param_name == "BOD5":
            standards = WaterQualityConfig.PARAMETER_STANDARDS["BOD5"] # [3, 3, 4, 6, 10]
            category = 5  # 默认劣Ⅴ类
            # 找到满足的最小类别索引 (最好的类别)
            best_category = 5 # 初始化为劣Ⅴ类
            for i, threshold in enumerate(standards):
                 if threshold is not None and value <= threshold:
                     best_category = i
                     break # 找到第一个满足的 (最好的) 就停止

            # 检查是否是 BOD5 的特殊情况 (满足Ⅰ类标准，且Ⅰ、Ⅱ类标准相同)
            if best_category == 0 and len(standards) > 1 and standards[0] == standards[1]:
                # 根据“取Ⅱ类标准”，将类别调整为Ⅱ类
                category = 1
            else:
                category = best_category

        else: # 处理其他参数（数值越低越好）的统一逻辑
            standards = WaterQualityConfig.PARAMETER_STANDARDS.get(param_name, [])
            if not standards:
                return {"error": f"未知参数: {param_name}", "result": "参数错误", "category": -1}
            # 其他参数（数值越低越好）的统一分类逻辑
            category = 5  # 默认劣Ⅴ类
            for i, threshold in enumerate(standards):
                if threshold is not None and value <= threshold:
                    category = i
                    break

        category_map = {0: "Ⅰ类", 1: "Ⅱ类", 2: "Ⅲ类", 3: "Ⅳ类", 4: "Ⅴ类", 5: "劣Ⅴ类"}
        return {
            param_name: value,
            "result": category_map[category],
            "category": category
        }
    except (TypeError, ValueError, IndexError) as e:
        return {"error": f"{param_name}数据错误: {str(e)}", "result": "劣Ⅴ类", "category": 5}


# 为每个参数创建专用函数
def do_check(do_value: float) -> Dict:
    """溶解氧检查"""
    return parameter_check("DO", do_value)

def codmn_check(codmn_value: float) -> Dict:
    """高锰酸盐指数检查"""
    return parameter_check("CODMn", codmn_value)

def cod_check(cod_value: float) -> Dict:
    """化学需氧量检查"""
    return parameter_check("COD", cod_value)

def bod5_check(bod_value: float) -> Dict:
    """五日生化需氧量检查"""
    return parameter_check("BOD5", bod_value)

def nh4_n_check(nh4_value: float) -> Dict:
    """氨氮检查"""
    return parameter_check("NH4_N", nh4_value)

def tn_check(tn_value: float) -> Dict:
    """总氮检查"""
    return parameter_check("TN", tn_value)

def tp_check(tp_value: float, water_type: str = "river") -> Dict:
    """总磷检查"""
    return parameter_check("TP", tp_value, water_type)

def cu_check(cu_value: float) -> Dict:
    """铜检查"""
    return parameter_check("CU", cu_value)

def zn_check(zn_value: float) -> Dict:
    """锌检查"""
    return parameter_check("ZN", zn_value)

def f_check(f_value: float) -> Dict:
    """氟化物检查"""
    return parameter_check("F", f_value)

def se_check(se_value: float) -> Dict:
    """硒检查"""
    return parameter_check("SE", se_value)

def as_check(as_value: float) -> Dict:
    """砷检查"""
    return parameter_check("AS", as_value)

def hg_check(hg_value: float) -> Dict:
    """汞检查"""
    return parameter_check("HG", hg_value)

def cd_check(cd_value: float) -> Dict:
    """镉检查"""
    return parameter_check("CD", cd_value)

def cr_vi_check(cr_vi_value: float) -> Dict:
    """六价铬检查"""
    return parameter_check("CR_VI", cr_vi_value)

def pb_check(pb_value: float) -> Dict:
    """铅检查"""
    return parameter_check("PB", pb_value)

def cn_check(cn_value: float) -> Dict:
    """氰化物检查"""
    return parameter_check("CN", cn_value)

def c6h5oh_check(c6h5oh_value: float) -> Dict:
    """挥发酚检查"""
    return parameter_check("C6H5OH", c6h5oh_value)

def phc_check(phc_value: float) -> Dict:
    """石油类检查"""
    return parameter_check("PHC", phc_value)

def las_as_check(las_as_value: float) -> Dict:
    """阴离子表面活性剂检查"""
    return parameter_check("LAS_AS", las_as_value)

def s2_h2s_check(s2_h2s_value: float) -> Dict:
    """硫化物检查"""
    return parameter_check("S2_H2S", s2_h2s_value)

def fc_check(fc_value: float) -> Dict:
    """粪大肠杆菌检查"""
    return parameter_check("FC", fc_value)


# 水质综合评价函数
def evaluate_water_quality(parameters: Dict[str, Union[float, Dict]], water_type: str = "river") -> Dict[str, Union[str, int, Dict]]:
    # 首先检查温度和pH，这两个超标直接为劣Ⅴ类
    current_temp = parameters.get("current_temp")
    last_temp = parameters.get("last_temp")
    if current_temp is not None and last_temp is not None:
        temp_result = temperature_check(current_temp, last_temp)
        if temp_result["result"] != "水温合格":
            return {"overall_result": "劣Ⅴ类", "reason": "水温不合格", "category": 5}

    ph_value = parameters.get("pH")
    if ph_value is not None:
        ph_result = ph_check(ph_value)
        if ph_result["result"] != "pH正常":
            return {"overall_result": "劣Ⅴ类", "reason": "pH不合格", "category": 5}

    worst_category = 0  # 修改初始值为0 (Ⅰ类)，寻找最差类别 (最大数字)
    worst_param = "N/A"
    detailed_results = {}

    for param_name, value in parameters.items():
        if param_name in ["current_temp", "last_temp", "pH"]:
            continue
        if isinstance(value, dict) and "category" in value:
            param_result = value
        else:
            if param_name == "TP":
                param_result = parameter_check(param_name, value, water_type)
            else:
                param_result = parameter_check(param_name, value, water_type)

        detailed_results[param_name] = param_result
        param_category = param_result.get("category", 5)
        # 修改比较逻辑：寻找最大的category (最差水质)
        if param_category > worst_category:
            worst_category = param_category
            worst_param = param_name

    category_map = {0: "Ⅰ类", 1: "Ⅱ类", 2: "Ⅲ类", 3: "Ⅳ类", 4: "Ⅴ类", 5: "劣Ⅴ类"}
    overall_result = category_map[worst_category]

    return {
        "overall_result": overall_result,
        "category": worst_category,
        "worst_param": worst_param,
        "details": detailed_results
    }


