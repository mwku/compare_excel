import pandas as pd
import numpy as np

import ui

def compare_same(data_a:pd.DataFrame,data_b:pd.DataFrame) -> pd.DataFrame:
    """
    Compare two dataframes and return the differences.
    """
    # 成品長度 && 素材規格 直到 成品數量 0
    try:
        result:list[str] = []
        data_a_list = [] # 規格 長度(float) 數量(int)
        title_now = ""
        for i in range(len(data_a)):
            if data_a["素材規格"].iloc[i] != "":
                title_now = data_a["素材規格"].iloc[i]
            data_a_list.append((str(title_now), float(data_a["成品長度"].iloc[i]), int(data_a["成品數量"].iloc[i])))

        data_b_dict = {} # 規格：[長度(float),數量(int),構件編號(str)]
        for i in range(len(data_b)):
            if data_b["素材規格"].iloc[i] != "":
                title_now = data_b["素材規格"].iloc[i]
            if data_b_dict.get(title_now) is None:
                data_b_dict[title_now] = []
            data_b_dict[title_now].append([float(data_b["成品長度"].iloc[i]), int(data_b["成品數量"].iloc[i]), str(data_b["構件編號"].iloc[i])])

        for i in range(len(data_a_list)):
            used:list[str] = []
            leave = data_a_list[i][2]
            for j in range(len(data_b_dict.get(data_a_list[i][0]))):
                if data_a_list[i][1]  == data_b_dict.get(data_a_list[i][0])[j][0]:
                    if data_b_dict.get(data_a_list[i][0])[j][1] >= leave:
                        result.append([data_b_dict.get(data_a_list[i][0])[j][2]])
                        data_b_dict.get(data_a_list[i][0])[j][1] -= data_a_list[i][2]
                        break
                    else:
                        used.append(data_b_dict.get(data_a_list[i][0])[j][2])
                        leave -= data_b_dict.get(data_a_list[i][0])[j][1]
                        data_b_dict.get(data_a_list[i][0])[j][1] = 0
        r = data_a
        r["構件編號"] = ""
        for i in range(len(result)):
            r.at[r.index[i], "構件編號"] = ",".join(result[i])
        # print(r)
        return r
    
    except KeyError as e:
        raise KeyError(f"請確認關鍵字{e}是否存在或檔名是否正確")
    
    except Exception as e:
        raise Exception(f"比較過程中發生錯誤: {e}")

def compare_diff(data_a:pd.DataFrame,data_b:pd.DataFrame,keyword:tuple[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    result_a = data_a
    result_b = data_b
    return (result_a,result_b)



def to_excel(data:pd.DataFrame,path:str) -> bool:
    try:
        data.to_excel(path, index=False)
        return True
    except Exception as e:
        return False

def read_file(file_path:str) -> pd.DataFrame:
    """
    Read a file and return a dataframe.
    """
    return pd.read_excel(file_path,dtype=str,keep_default_na=False, na_filter=False)

app = ui.App(read_file,compare_same,to_excel,compare_diff)
app.mainloop()