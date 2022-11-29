import os
import re
import json
import ast
import csv
base_route=os.path.abspath('.')
csv_output=[["picture_id","download_url","label","transcription","points","label_id"]]
f = open("Label.txt",encoding="utf-8")           # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line:
    # print (line)             # 后面跟 ',' 将忽略换行符
    # print(line, end = '')　　　# 在 Python 3中使用
    picture_route=line.split('\t')[0]
    content=line.split('\t')[1]
    picture_name=picture_route.split('.')[0].split('/')[1]
    url=base_route+'/'+picture_route
    result = re.findall(r'{(.*?)}',content)   #正则提取
    for i in range (len(result)):
        trans1='{'+result[i]+'}'
        try:
            trans2 = json.loads(trans1)
        except:
            print(trans1,":格式错误")
        else:
            one_row_output=[]
            one_row_output.append(picture_name)
            one_row_output.append(url)
            one_row_output.append(str(trans2["difficult"]))
            one_row_output.append(str(trans2["transcription"]))
            one_row_output.append(str(trans2["points"]))
            one_row_output.append(i)
            csv_output.append(one_row_output)
    line = f.readline()
f.close()
output_root="license.csv"
with open(output_root, 'w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_output)
