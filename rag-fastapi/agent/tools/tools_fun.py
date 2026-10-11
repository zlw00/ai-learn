rag_tool = None


def init_tools(tool):

    global rag_tool

    rag_tool = tool



def search_knowledge(query):

    return rag_tool.run(query)

def get_time():
    return rag_tool.run()

def calculator(query):
    return rag_tool.run(query)
