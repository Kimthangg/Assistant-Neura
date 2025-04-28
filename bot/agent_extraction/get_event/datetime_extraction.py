
from services.llm.llm_config import LLM
from typing import Optional, Dict, List

from .prompt_get_first import get_first_event_rules
from .prompt_get_freetime import get_freetime_rules
from .prompt_get_multi_calendar import get_multi_calendar_rules

from utils import get_context_date
def create_datetime_extractor():
    tool = {
        "name": "extract_datetime",
        "description": "Extract datetime ranges from text",
        "parameters": {
            "type": "object",
            "properties": {
                "datetime_ranges": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "start_datetime": {
                                "type": "string",
                                "description": "Start date and time in ISO format (YYYY-MM-DD HH:mm:ss)"
                            },
                            "end_datetime": {
                                "type": "string",
                                "description": "End date and time in ISO format (YYYY-MM-DD HH:mm:ss)"
                            }
                        },
                        "required": ["start_datetime", "end_datetime"]
                    },
                    "description": "List of datetime ranges extracted from the text"
                },
            },
            "required": ["datetime_ranges"]
        }
    }
    return tool
    
def extract_datetime_get_event(text: str, intent: str) -> Dict[str, List[Dict[str, str]]]:
    
    if intent == "get_first_calendar":
        rules = get_first_event_rules()
    elif intent == "get_freetime":
        rules = get_freetime_rules()
    elif intent == "get_multi_calendar":
        rules = get_multi_calendar_rules()    
    else:
        rules = ""
    system_prompt = f"""Extract datetime ranges from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Tìm ngày giờ chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss).
        2. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
    - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
    - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {rules}
    """
    llm = LLM(system_prompt, create_datetime_extractor(), temperature=0.1)

    response = llm(text)
    return response
    # print(response)
