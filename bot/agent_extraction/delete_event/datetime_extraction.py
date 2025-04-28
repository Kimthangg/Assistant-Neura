from langchain_core.messages import HumanMessage
from services.llm.llm_config import LLM
from typing import Optional, Dict, List
from datetime import datetime, timedelta
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

delete_event_rules = """
    You are an assistant that helps users find free time slots in their schedule.
Your task is to extract the free time slots from the user's schedule and return them in a structured format."""
def extract_datetime_delete_event(text: str) -> Dict[str, List[Dict[str, str]]]:
    
    system_prompt = f"""Extract datetime ranges from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Tìm ngày giờ chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss).
        2. Sau đó hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
        - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
        - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {delete_event_rules}
    """
    llm = LLM(system_prompt, create_datetime_extractor(), temperature=0.1)

    response = llm(text)
    return response
    # print(response)
