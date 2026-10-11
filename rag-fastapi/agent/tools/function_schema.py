tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description":
            "查询企业知识库，适用于公司制度、流程、假期等问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户的问题"
                    }
                },
                "required":[
                    "query"
                ]
            }
        }
    }
]