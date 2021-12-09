# -*- coding: utf-8 -*-

from CNSES.data_process import (
    Reader,
    ZipfProcess,
    PcaProcess,
    ExponProcess,
    FaProcess,
    OnehotProcess,
)
from CNSES.algorithms.clustering import (
    KMeansCluster,
    HcCluster,
    FactorCluster,
    KprotoCluster,
    SubpaceCluster,
)
from CNSES.visualize import TsneVisual
from CNSES.algorithms.typing import RandomforestTyping
from CNSES.tables import taball
from CNSES.utils import make_safe_path, ClusterReassign


def main(filepath: str) -> None:
    """
    perform segmentation evaluation
    """
    global con_vars
    global cat_vars
    global factor_vars
    global add_tab_cat_vars
    global add_tab_con_vars

    # preprocess stage
    reader = Reader(filepath)
    reader = FaProcess(
        reader, vars=factor_vars, nfactors="auto", loading_save=make_safe_path("./raws/output/factor_loadings.xlsx")
    )

    # cluster stage
    vars_to_cluster = reader.columns["fac"]
    cluster = FactorCluster(reader, vars=vars_to_cluster)
    cluster = KprotoCluster(
        reader,
        convars=factor_vars,
        catvars=cluster.columns["fclust_labels"] + cat_vars,
        nclusters=[11],
    )

    typing = RandomforestTyping(
    cluster,
    vars=cat_vars + factor_vars,
    labels=cluster.columns["kproto_labels"],
    clu_name="kproto",
    )

#     # visualization stage
#     visual = TsneVisual(
#         cluster,
#         # vars=cluster.columns["zipf"],
#         vars=vars_to_process,  # + cluster.columns["onehot"],
#         # vars=["tq423r14","tq423r15","tq423r16"],
#         # labels=cluster.columns["kmeans_labels"],
#         labels=cluster.columns["kproto_labels"],
#     )
#     visual.show()
    
    # tabulation stage
    con_vars = factor_vars + reader.columns["fac"] + add_tab_con_vars
    cat_vars = cat_vars + add_tab_cat_vars
    taball(
        data=cluster.data,
        con_vars=con_vars,
        cat_vars=cat_vars,
        clu_vars=cluster.columns["kproto_labels"],
        outfile=make_safe_path("./raws/output/upg_solu_tabs.xlsx"),
    )
    return cluster.data

if __name__ == "__main__":
    import pandas as pd
    data = pd.read_spss('./1206vivo_data_drop_del.sav')
    #删除开放题及”以上均无“选项 及全为0的['D2a__22']
    open_col = data.filter(like='open').columns.tolist()
    none_of_above = data.filter(like='500').columns.tolist()
    Refused_to_answer = data.filter(like='99').columns.tolist()
    others = data.filter(like='98').columns.tolist()
    data = data.drop(open_col+none_of_above+Refused_to_answer+others,axis=1)
    #ALL_var
    Region = ['Region']
    city_tier = ['City']
    mobile_type = ['G1','G2','G3']
    Commonly_used = data.filter(like='G4').columns.tolist()
    reason_buy = data.filter(like='G5').columns.tolist()
    hobby = data.filter(like='A1').columns.tolist()
    Everyday_experience = data.filter(like='A2').columns.tolist()
    Everyweek_experience = data.filter(like='A3').columns.tolist()
    Everymonth_experience = data.filter(like='A4').columns.tolist()
    Last_year = data.filter(like='B1').columns.tolist()
    Life_attitude = data.filter(like='B2').columns.tolist()
    Elec_owned = data.filter(like='C1').columns.tolist()
    Mobile_connected = data.filter(like='C2').columns.tolist()
    Install = data.filter(like='D1').columns.tolist()
    fre_byday = data.filter(like='D2').columns.tolist()
    fre_byweek = data.filter(like='D3').columns.tolist()
    Dissatisfied_app = data.filter(like='D4').columns.tolist()
    Purchased_last_month = data.filter(like='D5').columns.tolist()
    Mobile_satisfaction = data.filter(like='D6').columns.tolist()
    Dissatisfied_mobile = data.filter(like='D7').columns.tolist()
    gender = data.filter(like='S1').columns.tolist()
    age = data.filter(like='S2').columns.tolist()
    eduction = data.filter(like='S3').columns.tolist()
    Working_status = data.filter(like='S4').columns.tolist()
    Living_family = data.filter(like='S5').columns.tolist()
    number_Living_family = data.filter(like='S6').columns.tolist() #cati
    child_age = data.filter(like='S7').columns.tolist()
    revenue = data.filter(like='S8').columns.tolist()
    Commodity_brand = data.filter(like='S9').columns.tolist()

    con_vars = Life_attitude
    cat_vars = gender+age
#     cat_vars = gender
    factor_vars = ['video', 'music', 'reading', 'education', 'socialmedia', 'photo', 
                   'health', 'shopping', 'Parenting', 'convenient', 'tools', 'efficiency', 
                   'finance', 'travel', 'working', 'mobie_game', 'BYOA']
    
    add_tab_con_vars = (reason_buy+hobby+Everyday_experience+
                        Everyweek_experience+Everymonth_experience+
                        Last_year+Life_attitude+Elec_owned+Mobile_connected+
                        Install+Dissatisfied_app+
                        Purchased_last_month+Mobile_satisfaction+Dissatisfied_mobile+
                        Commodity_brand)
    
    add_tab_cat_vars = (Region+city_tier+Commonly_used+eduction+Working_status+Living_family+
                        number_Living_family+child_age+revenue)

#     data = main(filepath="maxdiff_data_enlarge_save.sav")
    data = main(filepath="./1206vivo_data_drop_del.sav")
    data.to_excel("./raws/output/1209V1.xlsx")
