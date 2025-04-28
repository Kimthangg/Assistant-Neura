from services.llm.llm_config import LLM
from typing import Optional, Dict, List
from datetime import datetime, timedelta

from .prompt_create_normal_event import create_event_normal
from .prompt_create_event_recurrece import create_event_recurrece
from utils import get_context_date

def create_datetime_extractor(is_recurring: bool):
    non_recurrence_tool = {
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
                "location": {
                    "type": "string",
                    "description": "Location of the event"
                },
            },
            "required": ["location","datetime_ranges"]
        }
    }
    recurrence_tool = {
        "name": "extract_datetime",
        "description": "Extract title, datetime ranges and recurrence rules from text",
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
                            },
                            "rrules": {
                                "type": "string",
                                "description": "Recurrence rules"
                            }
                        },
                        "required": ["start_datetime", "end_datetime", "rrules"]
                    },
                    "description": "List of datetime ranges extracted from the text"
                },               
                "location": {
                    "type": "string",
                    "description": "Location of the event"
                },
            },
            "required": ["location","datetime_ranges"]
        }
    }
    if is_recurring:
        return recurrence_tool
    else:
        return non_recurrence_tool
    
def extract_datetime_from_text(text: str, is_recurring: bool) -> Dict[str, List[Dict[str, str]]]:

    # Choose appropriate rules based on input type
    if is_recurring:
        rules = create_event_recurrece()
    else:
        rules = create_event_normal()
    
    system_prompt = f"""Extract datetime ranges from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Tìm ngày giờ chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss) không được sử dụng ngày trong quá khứ.
        2. Xác định địa điểm diễn ra sự kiện nếu không có đưa ra rỗng.
        3. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
    - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
    - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {rules}
    """
    llm = LLM(system_prompt, create_datetime_extractor(is_recurring), temperature=0.1)

    response = llm(text)
    return response
    # print(response)
