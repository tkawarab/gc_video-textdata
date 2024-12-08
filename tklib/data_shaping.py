import pandas as pd
import datetime
from tklib import data_shaping_check_similar
from tklib import gc_upload
import os


def tbl_2_sbv_format_2(bucket_name,array_tbl,file_name):
    df = pd.DataFrame(array_tbl,columns=["start_time","end_time","text","confidence","first_frame_tme","x1","y1","x2","y2","x3","y3","x4","y4"])
    df_s = df.sort_values(["start_time","y1","x1"],ascending=[True,True,True])
    save_csv_path = "./temp/" + file_name[:-4] + "_tmp.csv"
    df_s.to_csv(save_csv_path, index=False)

    ret = csv_2_sbv_format(save_csv_path,file_name)
    os.remove(save_csv_path)
    return ret

def csv_2_sbv_format(csv_path,file_name):
    df = pd.read_csv(csv_path)
    save_csv_path = "./temp/" + file_name[:-4] + "_tmp.csv"

    ret = ""
    df_s = df['text']
    df_i = df.index    

    similar_list = data_shaping_check_similar.check_similar(df_s)
    df_list = pd.DataFrame(similar_list)

    done_list = []
    new_list = []
    for index,df_row in df.iterrows():
        confidence = df_row['confidence']
        if confidence<0.9: continue
        if (int(df_row['end_time']) - int(df_row['start_time'])) < 1 \
            and confidence < 0.95:           
            continue        
        x1 = df_row['x1']
        x2 = df_row['x2']
        x3 = df_row['x3']
        x4 = df_row['x4']
        y1 = df_row['y1']
        y2 = df_row['y2']
        y3 = df_row['y3']
        y4 = df_row['y4']
        valid_list = check_similar(similar_list,df,index,df_row,done_list)
        if len(valid_list) == 0:
            continue
        #start_time = datetime.timedelta(seconds = df_row['start_time'])
        #end_time = datetime.timedelta(seconds = df_row['end_time'])
        #text = df_row['text']
        start_time = datetime.timedelta(seconds = valid_list[0])
        end_time = datetime.timedelta(seconds = valid_list[1])
        text = valid_list[2]
        #new_list.append([start_time,end_time,text,confidence,x1,x2,x3,x4,y1,y2,y3,y4])
        ret = ret + str(start_time) + "," + str(end_time) + "\n" + str(text) + "\n\n"
    #pd.DataFrame(new_list).to_csv(save_csv_path)
    return ret

def check_similar(similar_list,df_origin,index,df_row_origin,done_list):
    df = pd.DataFrame(df_origin)
    df_rows = pd.DataFrame(df_row_origin).transpose()
    similar_df = pd.DataFrame(similar_list)

    for index,df_row in df_rows.iterrows():
        threshold = 0.8
        similars = similar_df[index][similar_df[index] > threshold].index.tolist()
        select_similars = []
        for similar in similars:
            index_start_time = df_row['start_time']
            similar_start_time = df['start_time'][similar]
            test = abs(similar_start_time - index_start_time)
            if test <= 10:
                select_similars.append(similar)
        match = set(select_similars) & set(done_list)
        done_list.extend(select_similars)
        if len(list(match)) > 0:
            return []
        valid_confidence = df_row['confidence']
        valid_start_time = df_row['start_time']
        valid_end_time = df_row['end_time']
        valid_text = df_row['text']
        
        for item in select_similars:
            confidence = df['confidence'][item]
            start_time = df['start_time'][item]
            end_time = df['end_time'][item]
            text = df['text'][item]
            if valid_confidence < confidence:
                valid_text = text
                valid_confidence = confidence
            if valid_end_time < end_time:
                valid_end_time = end_time
    return [valid_start_time,valid_end_time,valid_text]    