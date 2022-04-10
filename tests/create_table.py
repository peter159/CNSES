# -*- coding: utf-8 -*-

import pandas as pd


def covert_excel(input_path, output_path):
    data = pd.read_excel(input_path)

    new_data = pd.DataFrame()  # 新建一个表
    need_columns = data.columns[1:]  # 获取需要的列，去掉第一列

    max_target = 0  # 这个循环为了计算target的最大值
    for column in need_columns:
        for i, j in data["target"].value_counts().items():
            if i > max_target:
                max_target = i

    target_dict = {columns: {} for columns in need_columns}
    for col in need_columns:
        for p in range(1, max_target + 1):
            target_dict[col].update({p: 0})
    # dict format: {'G5__1': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    for x, y in data["target"].items():
        for column in target_dict.keys():
            target_dict[column][y] += data[column][x]

    for q, g in data["target"].items():
        for c in target_dict.keys():
            target_dict[c][g] /= (
                target_dict["target"][g] / g
            )  # 每个数的总和再除以target = n时的数量得到平均数

    for columns in target_dict.keys():
        if columns != "target":
            subdict = target_dict[columns]  # 除去target一行
            new_data[columns] = pd.Series(subdict)
            new_data.T.to_excel(output_path)  # 保存表格
    __import__("ipdb").set_trace()  # FIXME BREAKPOINT


if __name__ == "__main__":
    input_path = "tablet_data.xlsx"
    output_path = "tablet.xlsx"
    covert_excel(input_path, output_path)
