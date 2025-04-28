from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from services.llm.llm_config import llm_gen
from bot.handler.message import call_api, full_flow

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import *

# System prompt for normal messages and context-based responses
system_prompt = """Bạn là một trợ lý ảo hữu ích có tên Neura. Bạn là một trợ lý ảo có thể giúp người dùng quản lý các sự kiện trong lịch của họ và có khả năng nhớ thông tin từ các cuộc trò chuyện trước.
Bây giờ, dựa vào lịch sử hội thoại trên, hãy trả lời câu hỏi của tôi theo cách tự nhiên và chính xác nhất với các chỉ dẫn sau:
- Bạn có thể giúp người dùng tạo, sửa, xóa sự kiện trong lịch của họ.
- Bạn có thể tạo, cập nhật, xóa sự kiện trong lịch.
- Bạn cũng có thể giúp người dùng tìm khoảng thời gian trống trong lịch.
- Bạn có thể giúp người dùng tìm nhiều sự kiện trong một ngày.
- Bạn cũng có thể giúp người dùng tìm sự kiện đầu tiên trong ngày.
Ngoài ra, bạn có thể trả lời các câu hỏi thông thường của người dùng.
- Nếu người dùng yêu cầu Create, update, delete thì ngữ cảnh nhận được là thời gian, địa điểm, tiêu đề để Create, update, delete.
freetime là thời gian rảnh trong lịch của người dùng.
multi_calendar là nhiều sự kiện trong ngày của người dùng.
first_calendar là sự kiện đầu tiên trong ngày của người dùng.
Hãy đưa ra thông tin dưới dạng json để người dùng xác nhận thông tin nếu đó là tạo, sửa, xóa sự kiện trong lịch,
nếu là lấy sự kiện(freetime, multi_calendar, first_calendar) thì dựa vào ngữ cảnh trả lời câu hỏi của người dùng 1 cách tự nhiên như có kiến thức về ngữ cảnh
yêu cầu thông tin cụ thể tương ứng với các trường hợp:
- Nếu là tạo sự kiện thì yêu cầu tiêu đề, thời gian bắt đầu, thời gian kết thúc, địa điểm(có thể có hoặc không).
- Nếu là sửa sự kiện thì yêu cầu tiêu đề, thời gian bắt đầu, thời gian kết thúc, địa điểm(có thể có hoặc không).
- Nếu là xóa sự kiện thì yêu cầu thời gian bắt đầu, thời gian kết thúc.

- Nếu là lấy sự kiện thì yêu cầu thời gian bắt đầu, thời gian kết thúc.
- Nếu là lấy thời gian rảnh thì yêu cầu thời gian bắt đầu, thời gian kết thúc.
- Nếu là lấy nhiều sự kiện thì yêu cầu thời gian bắt đầu, thời gian kết thúc.
- Nếu là lấy sự kiện đầu tiên thì yêu cầu thời gian bắt đầu, thời gian kết thúc.
"""
# Tạo llm để sinh nội dung
llm = llm_gen()
def chain_gen_normal_message(history=None):
    """
    Tạo chain sinh nội dung trả lời các câu hỏi bình thường
    
    Returns:
        Chain: Chain kết hợp prompt và LLM để trả lời các câu hỏi bình thường
    """
    # Tạo prompt cho các câu hỏi bình thường
    prompt_normal = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("""Thông tin về thời gian hiện tại: {datetime_current}
                                                     Câu hỏi của người dùng: {query}"""),
        ]
    )
    chain =  prompt_normal | llm 
    return RunnableWithMessageHistory(
        chain,
        get_session_history= lambda:history,
        input_messages_key="query",
        history_messages_key="history",
    )
    
llm_zero = llm_gen(temperature=0.1)
def chain_gen_with_tools():
    """
    Tạo chain sinh nội dung với ngữ cảnh từ tools
    
    Returns:
        Chain: Chain kết hợp prompt và LLM để trả lời với ngữ cảnh
    """
    # Tạo llm sinh nội dung với độ nhiệt phù hợp để hiểu ngữ cảnh từ tools
    template = """Ngữ cảnh {context}. Dựa vào ngữ cảnh trả lời câu hỏi của người dùng 1 cách tự nhiên như có kiến thức về ngữ cảnh đối với lấy lịch(không đưa ra thông tin về htmlLink),
        còn đối với tạo, sửa, xóa sự kiện thì trả lời câu hỏi của người dùng 1 cách tự nhiên để người dùng xác nhận thông tin nếu đó là tạo, sửa, xóa sự kiện trong lịch,
        kèm theo thông tin json . 
        Câu hỏi: {query}:
                ```json
                "Tiêu đề": "Đây là tiêu đề của sự kiện(title)",
                "Thời gian bắt đầu": "Đây là thời gian bắt đầu của sự kiện định dạng tự nhiên(start_datetime)",
                "Thời gian kết thúc": "Đây là thời gian kết thúc của sự kiện định dạng tự nhiên(end_datetime)",
                "Địa điểm": "Đây là địa điểm của sự kiện(location)",
                ```
            """
    prompt_event = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(template, input_variables=["context", "query"]),
        ]
    )
    return prompt_event | llm_zero
    # return RunnableWithMessageHistory(
    #     chain,
    #     get_session_history=lambda:history,
    #     input_messages_key="query",
    #     history_messages_key="history",
    # )



def create_history_from_list(message_list):
    'Chuyển đổi danh sách tin nhắn thành lịch sử hội thoại'
    history = InMemoryChatMessageHistory()
    for msg in message_list:
        if msg["type"] == "user":
            history.add_user_message(msg["content"])
        elif msg["type"] == "assistant":
            history.add_ai_message(msg["content"])
    return history

def gen_llm(query: str, chat_history):
    """
    Hàm chính để sinh nội dung từ LLM dựa trên ý định của người dùng
    
    Parameters:
        query (str): Câu hỏi của người dùng
        
    Returns:
        tuple: (content, context) - nội dung sinh ra và ngữ cảnh liên quan
    """

    function_args = full_flow(query)
    #nếu thời gian không hợp lệ thì trả về thông báo
    if function_args.get('incorrect_datetime'):
        return "Đã có lỗi xảy ra vui lòng kiểm tra lại thời gian!", {}
    
    if function_args.get('intent') in ["normal_message"]:
        # Tạo chain sinh nội dung trả lời bình thường
        print('chạy bình thường')
        history = create_history_from_list(chat_history)
        print("history",history)
        chain = chain_gen_normal_message(history)
        return chain.invoke({"query": query,"datetime_current": get_context_date()}).content, {}
    else:
        print('chạy với ngữ cảnh')
        # Tạo chain sinh nội dung với ngữ cảnh từ tools
        chain = chain_gen_with_tools()
        if function_args.get("intent") in ["get_first_calendar", "get_freetime", "get_multi_calendar"]:
            # Gọi API để lấy thông tin lịch
            context_api = call_api(function_args)
        else:
            # Nếu không lấy lịch thì trả về context là function_args
            context_api = function_args
        # Nếu context_api là list thì lấy phần tử đầu tiên
        final_context = context_api[0] if isinstance(context_api, list) else context_api
        return chain.invoke({"query": query, "context": context_api}).content, final_context