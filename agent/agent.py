from tools import (
    search_knowledge,
    get_time
)


class Agent:

    def __init__(self):
        pass


    def run(self, question):

        # 模拟 LLM 判断

        if "年假" in question or "病假" in question:

            result = search_knowledge(
                question
            )

            return result


        elif "时间" in question:

            result = get_time()

            return result


        else:

            return "不知道"



if __name__ == "__main__":

    agent = Agent()


    question = "病假需要多久申请"

    answer = agent.run(
        question
    )

    print(answer)