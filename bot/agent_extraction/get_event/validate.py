prompt_validate_system = """Bạn là trợ lý ảo thông minh có chức năng kiểm tra câu lệnh của người dùng có hợp lệ hay không về thời gian.   
1. Kiểm tra xem thời gian có thỏa mãn điều kiện(incorrect_datetime):
    - Kiểm tra ngày không hợp lệ: 30/2, 31/4, 31/6, 31/9, 31/11
    - Kiểm tra thời gian không hợp lệ: 24:00:00, 25:00:00
    - Kiểm tra tháng không hợp lệ: Tháng 13, tháng 0
    - Kiểm tra năm không hợp lệ: < năm hiện tại
    - Mặc định là False chỉ trả về true nếu tìm thấy bất kỳ mẫu không hợp lệ nào

Quy tắc bổ sung:
1. Xác thực tất cả thông tin ngày giờ trong yêu cầu:
- Kiểm tra tất cả các số để biết ngày/giờ hợp lệ
2. Đối với incorrect_datetime: Kiểm tra tất cả các mẫu ngày/giờ để biết tính hợp lệ

LƯU Ý QUAN TRỌNG:
- Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
- Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
- Luôn trả về giá trị cho incorrect_datetime, ngay cả khi không thấy thông tin ngày giờ trong câu lệnh của người dùng
- Nếu không chắc chắn, hãy đặt incorrect_datetime là False

Vui lòng phân tích văn bản cẩn thận và trả về thông tin bắt buộc.

"""
tool_get_event_validate ={
        "name": "validate_get_event",
        "description": "Validate booking event requests and extract event information",
        "parameters": {
            "type": "object",
            "properties": {
                "incorrect_datetime": {
                    "type": "boolean",
                    "description": "True if there are invalid datetime patterns"
                }
            },
            "required": ["incorrect_datetime"]
        }
    }

from services.llm.llm_config import LLM

agent_validate_get = LLM(prompt_validate_system, tool_get_event_validate, temperature=0.0)