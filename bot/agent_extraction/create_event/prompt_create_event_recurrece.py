def create_event_recurrece():
    return """
Hãy tuân theo các hướng dẫn sau để trích xuất thông tin lịch định kỳ:
- Trích xuất tất cả các khoảng ngày giờ được đề cập trong văn bản.
- Chuyển đổi sang định dạng ISO (YYYY-MM-DD HH:mm:ss).
- Xử lý các mốc thời gian tương đối (hôm nay, ngày mai, tuần sau, v.v.) dựa vào ngày hiện tại.
- Nếu chỉ có ngày mà không có giờ, sử dụng 00:00:00 cho thời điểm bắt đầu và 23:59:59 cho thời điểm kết thúc.
- Nếu chỉ có một mốc thời gian duy nhất, đặt nó làm cả thời điểm bắt đầu và kết thúc (thời gian bắt đầu bằng thời gian kết thúc).
- Trích xuất quy tắc lặp lại (RRULE) từ yêu cầu của người dùng, đảm bảo tuân theo định dạng iCalendar:
  + FREQ: tần suất (DAILY, WEEKLY, MONTHLY, YEARLY)
  + INTERVAL: khoảng cách (mặc định là 1)
  + BYMONTHDAY: ngày trong tháng (1-31)
  + BYMONTH: tháng trong năm (1-12)
  + BYDAY: ngày trong tuần (MO, TU, WE, TH, FR, SA, SU)
  + COUNT: số lần lặp lại
  + UNTIL: ngày kết thúc lặp lại (YYYYMMDD)
- Trong các trường hợp không rõ ràng, đưa ra giả định hợp lý dựa trên ngữ cảnh.
- Trả về một mảng rỗng nếu không tìm thấy thông tin ngày giờ nào.

Ví dụ 1: 
Input: "Tôi có một cuộc họp vào mỗi thứ Hai từ 10 giờ sáng đến 11 giờ sáng."
Output:
{
  'datetime_ranges': [
    {
      'start_datetime': '2025-04-14 10:00:00', 
      'end_datetime': '2025-04-14 11:00:00',
      'rrules': 'RRULE:FREQ=WEEKLY;BYDAY=MO'
    }
  ], 
  'location': ''
}

Ví dụ 2:
Input: "Tạo sự kiện hàng tháng vào ngày 15 từ 2 giờ đến 3 giờ chiều tại Văn phòng công ty"
Output:
{
  'datetime_ranges': [
    {
      'start_datetime': '2025-04-15 14:00:00',
      'end_datetime': '2025-04-15 15:00:00',
      'rrules': 'RRULE:FREQ=MONTHLY;BYMONTHDAY=15'
    }
  ],
  'location': 'Văn phòng công ty'
}

Ví dụ 3:
Input: "Tạo lịch họp hằng năm vào ngày 30/04 lúc 8 giờ sáng"
Output:
{
  'datetime_ranges': [
    {
      'start_datetime': '2025-04-30 08:00:00',
      'end_datetime': '2025-04-30 08:00:00',
      'rrules': 'RRULE:FREQ=YEARLY;BYMONTHDAY=30;BYMONTH=4'
    }
  ],
  'location': ''
}
"""

