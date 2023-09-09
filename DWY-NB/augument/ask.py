import SparkApi
import sys
import pandas as pd
#以下密钥信息从控制台获取
appid = "d1145251"     #填写控制台中获取的 APPID 信息
api_secret = "MTJjNTEzN2ExNTcwOGI1YjY4NTY2YWE0"   #填写控制台中获取的 APISecret 信息
api_key ="762e42b4710b28a6bbb1e14a27affb00"    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
# domain = "general"   # v1.5版本
domain = "generalv2"    # v2.0版本
#云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    

# conversation_module.py

def get_xinghuo_answers(input_str, log_filename, answer_filename):
    text.clear()
    input_lines = input_str.strip().split('\n')
    #output_list = []

    line_index = 0  # 用于跟踪读取的行索引
    #log_file = open(log_filename, "a")  # Open the log file in append mode
    #data_file = open(answer_filename, "a")

    try:
        while line_index < len(input_lines):
            Input = input_lines[line_index].strip()


            with open(answer_filename, "r", encoding="utf-8") as file:
        # 逐行读取文件，并计数行数
                    line_count = sum(1 for line in file)

            log_file = open(log_filename, "a")
            data_file = open(answer_filename, "a")
            #Input = input_str
            if not Input:
                break      
            #data_file.write(Input + "\n")
            #Input = "列出与"+Input+"最相关的十个关键词"
            Input = "List the top ten relevant keywords related to " + Input + ", without explanation."        
            print("我: " + Input)

            log_file.write("我: " + Input + "\n")
            question = checklen(getText("user", Input))
            SparkApi.answer = ""
            print("星火:", end="")
           
            
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
            getText("assistant", SparkApi.answer)
            assistant_response = str(text[-1]["content"])
            
            
            log_file.write("星火: " + assistant_response + "\n")

            Input="Extract the ten keywords mentioned in the following statement and separate them with commas, without explanation."+assistant_response
            log_file.write("我: " + Input + "\n")
            question = checklen(getText("user", Input))
            SparkApi.answer = ""
            print('总结:', end="")  
            SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
            getText("assistant",SparkApi.answer)
            assistant_response = str(text[-1]["content"])
            log_file.write("星火: " + assistant_response + "\n")

            data_file.write(assistant_response + "\n")
            data_file.flush()

            line_index += 1  # 读取下一行
            log_file.flush()  
            data_file.close()
            log_file.close()

            #data_file = pd.read_csv(answer_filename, delimiter=',', header=None)
            #keywordss = data_file.iloc[:, :]
            #keywords = keywordss.iloc[line_count]
            #judge = keywordss.iloc[i]
            #while len(judge[0])!=0:
                #i+=1
            with open(answer_filename, "r", encoding="utf-8") as file:
                lines=file.readlines()
                if 0<len(lines):
                    keywords=lines[-1]
                    keywords=keywords.strip()
                    keywords=keywords.split(",")

            
            print('以下为提取出的文字:'+str(keywords)+'\n')

    except KeyboardInterrupt:
        pass
    return keywords





