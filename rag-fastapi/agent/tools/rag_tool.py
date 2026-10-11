
class RagTool:


    def __init__(
        self,
        rag_service
    ):
        self.rag_service = rag_service


    def run(
        self,
        query,
        session_id = "01",
    ):

        result = self.rag_service.chat(
            session_id,
            query
        )

        return result

    def run_pass(
        self
    ):
        pass
