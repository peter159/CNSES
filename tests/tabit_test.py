# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from CNSES.tables import taball
from CNSES.utils import make_safe_path

import pandas as pd
data = pd.read_spss('./data/1220data.sav')
#删除开放题及”以上均无“选项 及全为0的['D2a__22']
open_col = data.filter(like='open').columns.tolist()
none_of_above = data.filter(like='500').columns.tolist()
# Refused_to_answer = data.filter(like='99').columns.tolist()
# others = data.filter(like='98').columns.tolist()
data = data.drop(open_col+none_of_above,axis=1)
#ALL_var
Region = ['Region']
city_tier = ['City']
phone_type = ['G3']
mobile_type1 = ['G1','G2']
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

data = pd.read_spss('./data/1222datadelsomecases.sav')

con_vars = ['video', 'music', 'reading', 'education', 
                'socialmedia', 'photo', 'health', 'shopping', 
                'Parenting', 'convenient', 'tools', 'efficiency', 
                'finance', 'travel', 'working', 'mobie_game', 'BYOA',
                'B2__1', 'B2__2', 'B2__3', 'B2__4', 'B2__5', 'B2__6', 
                'B2__7', 'B2__8', 'B2__9', 'B2__10', 'B2__11', 'B2__12', 
                'B2__13', 'B2__14']+fre_byday
cat_vars = city_tier+age+phone_type+['S2','S3','S4','S8']+gender+['fclust_12','f17']+['S8_reco']

taball(
    data=data,
    con_vars=con_vars,
    cat_vars=cat_vars,
    clu_vars=data['re_membership'], 
    outfile=make_safe_path("./output/1222/1222tabit16-17edu_shopV2recona.xlsx"),
)
