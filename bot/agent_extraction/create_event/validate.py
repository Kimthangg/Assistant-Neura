prompt_validate_system = """Bạn là trợ lý ảo thông minh có chức năng kiểm tra câu lệnh của người dùng có hợp lệ hay không về thời gian.
1. Xác định tiêu đề của sự kiện(title):
 - Trích xuất thông tin về sự kiện từ câu lệnh của người dùng.
 - Example: 
    * "Họp nhóm" từ "Tạo sự kiện họp nhóm vào ngày mai lúc 15h"
    * "Đi chơi" từ "Tạo sự kiện đi chơi vào cuối tuần"
    * "Học Toeic" từ "Tạo sự kiện học Toeic vào tối thứ 7"
    
2. Kiểm tra xem thời gian có thỏa mãn điều kiện(incorrect_datetime):
    - Kiểm tra ngày không hợp lệ: ví dụ 30/2, 31/4, 31/6, 31/9, 31/11,...
    - Kiểm tra thời gian không hợp lệ: ví dụ 24:00:00, 25:00:00,..
    - Kiểm tra tháng không hợp lệ: ví dụ Tháng 13, tháng 0,...
    - Kiểm tra năm không hợp lệ: < năm hiện tại
    - Mặc định là False chỉ trả về True nếu tìm thấy bất kỳ mẫu không hợp lệ nào
    
3. Kiểm tra xem sự kiện có lặp lại không(is_recurring):
    - Trả về True nếu sự kiện lặp lại (mỗi, hàng tuần, hàng tháng, hàng năm, v.v.)
    - Ví dụ: "Họp nhóm hàng tuần", "Học Toeic mỗi tối thứ 7",...

Suy luận theo từng bước:
1. Trích xuất tiêu đề sự kiện từ yêu cầu
2. Xác thực tất cả thông tin ngày giờ trong yêu cầu:
- Kiểm tra tất cả các số để biết ngày/giờ hợp lệ
3. Đối với incorrect_datetime: Kiểm tra tất cả các mẫu ngày/giờ để biết tính hợp lệ
4. Đối với is_recurring: Kiểm tra các mẫu lặp lại trong yêu cầu

LƯU Ý QUAN TRỌNG:
- Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
- Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
- Luôn trả về giá trị cho tất cả các trường bắt buộc, ngay cả khi không tìm thấy thông tin trong câu lệnh của người dùng
- Nếu không chắc chắn, hãy đưa ra giá trị mặc định: title là chuỗi rỗng (""), incorrect_datetime là False, is_recurring là False

Vui lòng phân tích văn bản cẩn thận và trả về tất cả thông tin bắt buộc.

"""
tool_create_event_validate ={
        "name": "validate_create_event",
        "description": "Validate booking event requests and extract event information",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title/name of the event (e.g., khám bệnh, cuộc họp, hội thảo, đi chơi, học Toeic, etc.)"
                },
                "incorrect_datetime": {
                    "type": "boolean",
                    "description": "True if there are invalid datetime patterns"
                },
                "is_recurring": {
                    "type": "boolean",
                    "description": "True if this is a recurring event (e.g., mỗi, hàng tuần, hàng tháng, etc.)"
                },
            },
            "required": ["title", "incorrect_datetime", "is_recurring"]
        }
    }

from services.llm.llm_config import LLM

agent_validate_create = LLM(prompt_validate_system, tool_create_event_validate, temperature=0.0)