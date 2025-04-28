import os
CREDENTIALS_FILE = "credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE

# Scope cho quyền truy cập vào Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
# Đường dẫn đến tệp JSON chứa thông tin xác thực của tài khoản dịch vụ
SERVICE_ACCOUNT_FILE = 'credentials.json'
# Chọn lịch cần thêm sự kiện (mặc định là "primary")
CALENDAR_ID = "THAY THẾ BẰNG ID LỊCH CỦA BẠN NÓ CÓ DẠNG @group.calendar.google.com"  # Email tài khoản Google có lịch cần truy cập
