from datetime import datetime


def search_knowledge(query):

    # 这里暂时模拟RAG

    knowledge = {
        "病假":
            "病假需要提前1天申请",

        "年假":
            "年假需要提前3个工作日申请"
    }


    for key,value in knowledge.items():

        if key in query:
            return value


    return "知识库没有相关信息"



def get_time():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



def calculator(expression):

    try:

        result = eval(expression)

        return str(result)

    except:

        return "计算错误"