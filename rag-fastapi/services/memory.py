class ChatMemory:
    def __init__(self):
        self.session = {}

    def add_message(
            self,
            session_id,
            role,
            content
    ):
        if session_id not in self.session:
            self.session[session_id] = []

        self.session[session_id].append({
            'role': role,
            'content': content
        })

    def get_history(self, session_id):
        return self.session.get(session_id, []).copy()#如果不加copy则返回的是原list的引用，如果后面进行add_message，则history列表会跟着变，所以添加copy
