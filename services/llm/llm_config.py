from langchain_openai import ChatOpenAI

#AI Studio
API_KEY = "THAY BẰNG API CỦA BẠN"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME = "gemini-2.0-flash"

# Format lịch sử trò chuyện để đưa vào prompt
def format_chat_history(chat_history):
    """
    Chuyển đổi lịch sử trò chuyện thành chuỗi văn bản có định dạng.
    
    Parameters:
        chat_history (list): Danh sách các tin nhắn trong lịch sử trò chuyện
    
    Returns:
        str: Chuỗi văn bản chứa lịch sử trò chuyện đã định dạng
    """
    if not chat_history:
        return ""
    
    formatted_history = ""
    for msg in chat_history:
        role = "Người dùng" if msg["type"] == "user" else "Trợ lý"
        formatted_history += f"{role}: {msg['content']}\n\n"
    
    return formatted_history

class LLM:
    def __init__(self, system_message: str, tool: dict, model_name: str = MODEL_NAME, temperature: float = 0.):
        """
        Initializes the LLM class with a specified system message, tool, model name, and temperature.

        Parameters:
        system_message (str): The system message to be used by the language model.
        tool (dict): A dictionary representing the tool to be bound to the model.
        model_name (str): The name of the model to be used. Defaults to MODEL_NAME.
        temperature (float): The temperature setting for the model, affecting randomness. Defaults to 0.
        """
        self.model = ChatOpenAI(
            api_key=API_KEY,
            openai_api_base=API_BASE,
            model=MODEL_NAME,
            temperature=temperature,
            # streaming=True,
        )
        # , tool_choice=tool["name"]
        if tool is not None:
            self.model = self.model.bind_tools([tool])
        self.system_message = system_message
    def __call__(self, user_message: str):
        """
        Invokes the language model with a user message and returns the function name and arguments if any tool calls are made.

        Parameters:
        user_message (str): The message from the user to be processed by the language model.

        Returns:
        tuple: A tuple containing the function name and arguments if a tool call is made, otherwise (None, {}).
        """
        response = self.model.invoke([
            ("system", self.system_message),
            ("user", user_message),
        ])
        # print(f"response = {response}")
        # print(f"model = {self.model}")
        # print(f"system message = {self.system_message}")
        if len(response.tool_calls):  # need to get calendar info
            function_name = response.tool_calls[0].get('name', '')
            function_args = response.tool_calls[0].get('args')
            token_used = response.usage_metadata.get('total_tokens', -1)
            # print(f"{function_name} {function_args} {token_used}")
            # return function_name, function_args
            return function_args

        return {}

# system_message_normal = """
# Bạn là một trợ lý ảo thông minh, có khả năng nhớ thông tin từ các cuộc trò chuyện trước.
# Dưới đây là lịch sử hội thoại giữa tôi và bạn:
# {chat_history}

# Bây giờ, dựa vào lịch sử hội thoại trên, hãy trả lời câu hỏi của tôi theo cách tự nhiên và chính xác nhất.

# Người dùng: {user_input}
# Trợ lý:
# """

def llm_gen(model_name: str = MODEL_NAME, temperature: float = 0.5):
    """
    Tạo một đối tượng ChatOpenAI dựa trên các thông số được cung cấp.
    Hàm này tạo và cấu hình một đối tượng ChatOpenAI sử dụng các thông số về model, key API và 
    các cài đặt khác được định nghĩa trước.
    Parameters:
        model_name (str, optional): Tên của model OpenAI sẽ được sử dụng. 
                                   Mặc định là giá trị của hằng số MODEL_NAME.
        temperature (float, optional): Tham số điều chỉnh độ ngẫu nhiên của kết quả sinh ra. 
                                      Mặc định là 1.0.
    Returns:
        ChatOpenAI: Một đối tượng ChatOpenAI đã được cấu hình, sẵn sàng để sử dụng.
    """
    return ChatOpenAI(
            api_key=API_KEY,
            openai_api_base=API_BASE,
            model=model_name,
            temperature=temperature,
        )
