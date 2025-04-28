def create_event_normal():
    return """
Hãy tuân theo các hướng dẫn sau để trích xuất thông tin sự kiện thông thường:
- Trích xuất tất cả các khoảng ngày giờ được đề cập trong văn bản một cách chính xác.
- Chuyển đổi sang định dạng ISO chuẩn (YYYY-MM-DD HH:mm:ss).
- Xử lý các mốc thời gian tương đối (hôm nay, ngày mai, tuần sau, v.v.) dựa vào các mốc thời gian đã đề cập, nếu thời gian đã qua thì lấy tuần sau.
- Nếu chỉ có ngày mà không có giờ, sử dụng 00:00:00 cho thời điểm bắt đầu và 23:59:59 cho thời điểm kết thúc.
- Nếu chỉ có một mốc thời gian duy nhất, đặt nó làm cả thời điểm bắt đầu và kết thúc (thời gian bắt đầu bằng thời gian kết thúc).
- Trích xuất địa điểm sự kiện nếu được đề cập, nếu không có thì để trống ('').
- Trong các trường hợp không rõ ràng, đưa ra giả định hợp lý dựa trên ngữ cảnh.
- Trả về một mảng rỗng nếu không tìm thấy thông tin ngày giờ nào.
IMPORTANT: KHÔNG SỬ DỤNG THỜI GIAN TRONG QUÁ KHỨ
Ví dụ 1: 
Input: "Ngày 15/05 tôi có buổi thi trên trường vào lúc 10 giờ sáng hãy tạo lịch."
Output:
{
  'datetime_ranges': [
    {
      'start_datetime': '2025-05-15 10:00:00', 
      'end_datetime': '2025-05-15 10:00:00'
    }
  ], 
  'location': 'trường'
}

Ví dụ 2:
Input: "Tạo lịch họp ngày mai từ 14h đến 16h tại phòng A1-501"
Output:
{
  'datetime_ranges': [
    {
      'start_datetime': '2025-04-13 14:00:00',
      'end_datetime': '2025-04-13 16:00:00'
    }
  ],
  'location': 'phòng A1-501'
}

Ví dụ 3:
Input: "Đặt lịch hẹn với bác sĩ vào 9h sáng thứ Sáu tuần này"
Output:
{
  'datetime_ranges': [
    {
      'start_datetime': '2025-04-18 09:00:00',
      'end_datetime': '2025-04-18 09:00:00'
    }
  ],
  'location': ''
}
"""
