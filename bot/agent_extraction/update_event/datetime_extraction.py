from services.llm.llm_config import LLM
from typing import Optional, Dict, List


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
                                "description": "Original start datetime before the update, in ISO format (YYYY-MM-DD HH:mm:ss)"
                            },
                            "end_datetime": {
                                "type": "string",
                                "description": "Original end datetime before the update, in ISO format (YYYY-MM-DD HH:mm:ss)"
                            },
                            "start_new": {
                                "type": "string",
                                "description": "Updated start datetime after the change, in ISO format (YYYY-MM-DD HH:mm:ss)"
                            },
                            "end_new": {
                                "type": "string",
                                "description": "Updated end datetime after the change, in ISO format (YYYY-MM-DD HH:mm:ss)"
                            }
                        },
                        "required": ["start_datetime", "end_datetime", "start_new", "end_new"]
                    },
                    "description": "List of datetime ranges extracted from the text"
                },
            },
            "required": ["datetime_ranges"]
        }
    }
    return tool

update_event_rules = """
    Bạn là một trợ lý giúp người dùng tìm các khoảng thời gian rảnh trong lịch trình của họ.
Nhiệm vụ của bạn là trích xuất các khoảng thời gian từ câu truy vấn của người dùng và trả về chúng dưới dạng có cấu trúc.

Hãy tuân theo các hướng dẫn sau để trích xuất:
- Trích xuất tất cả các khoảng ngày giờ được đề cập trong văn bản một cách chính xác.
- Chuyển đổi sang định dạng ISO chuẩn (YYYY-MM-DD HH:mm:ss).
- Xử lý các mốc thời gian tương đối (hôm nay, ngày mai, tuần sau, v.v.) dựa vào các mốc thời gian đã đề cập, nếu thời gian đã qua thì lấy tuần sau.
- Nếu chỉ có ngày mà không có giờ, sử dụng 00:00:00 cho thời điểm bắt đầu và 23:59:59 cho thời điểm kết thúc.
- Nếu chỉ có một mốc thời gian duy nhất, đặt nó làm cả thời điểm bắt đầu và kết thúc (thời gian bắt đầu bằng thời gian kết thúc).
- Trích xuất địa điểm sự kiện nếu được đề cập, nếu không có thì để trống ('').
- Trong các trường hợp không rõ ràng, đưa ra giả định hợp lý dựa trên ngữ cảnh.
- Trả về một mảng rỗng nếu không tìm thấy thông tin ngày giờ nào.
IMPORTANT: KHÔNG SỬ DỤNG THỜI GIAN TRONG QUÁ KHỨ

Ví dụ: 
1. "Thay đổi cuộc họp từ 9h đến 11h ngày 20/4/2025 thành 14h đến 16h cùng ngày"
   Kết quả: 
   {
     "datetime_ranges": [
       {
         "start_datetime": "2025-04-20 09:00:00",
         "end_datetime": "2025-04-20 11:00:00",
         "start_new": "2025-04-20 14:00:00",
         "end_new": "2025-04-20 16:00:00"
       }
     ]
   }

2. "Dời buổi thuyết trình vào ngày mai từ 8h sáng thành 15h chiều"
   Giả sử ngày hiện tại là 19/4/2025, kết quả:
   {
     "datetime_ranges": [
       {
         "start_datetime": "2025-04-20 08:00:00",
         "end_datetime": "2025-04-20 08:00:00",
         "start_new": "2025-04-20 15:00:00",
         "end_new": "2025-04-20 15:00:00"
       }
     ]
   }

3. "Chuyển sự kiện ngày 25/4 thành ngày 27/4"
   Kết quả:
   {
     "datetime_ranges": [
       {
         "start_datetime": "2025-04-25 00:00:00",
         "end_datetime": "2025-04-25 23:59:59",
         "start_new": "2025-04-27 00:00:00",
         "end_new": "2025-04-27 23:59:59"
       }
     ]
   }

4. "Đổi cuộc hẹn từ 10h-12h thứ 2 tuần sau thành 13h-15h thứ 3 cùng tuần"
   Giả sử ngày hiện tại là 19/4/2025 (thứ 7), kết quả:
   {
     "datetime_ranges": [
       {
         "start_datetime": "2025-04-21 10:00:00",
         "end_datetime": "2025-04-21 12:00:00",
         "start_new": "2025-04-22 13:00:00",
         "end_new": "2025-04-22 15:00:00"
       }
     ]
   }

5. "Cập nhật thời gian họp từ 15h30 đến 17h ngày 22/4/2025 thành từ 16h đến 18h ngày 23/4/2025"
   Kết quả:
   {
     "datetime_ranges": [
       {
         "start_datetime": "2025-04-22 15:30:00",
         "end_datetime": "2025-04-22 17:00:00",
         "start_new": "2025-04-23 16:00:00",
         "end_new": "2025-04-23 18:00:00"
       }
     ]
   }
"""
def extract_datetime_update_event(text: str) -> Dict[str, List[Dict[str, str]]]:
    
    system_prompt = f"""Extract datetime ranges from the user's message.
    {update_event_rules}
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Tìm ngày giờ cũ và mới chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss).
        2. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
        - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
        - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    """
    llm = LLM(system_prompt, create_datetime_extractor(), temperature=0.1)

    response = llm(text)
    return response
    # print(response)
