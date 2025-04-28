from google.oauth2 import service_account
from googleapiclient.discovery import build
from .environment import SCOPES, SERVICE_ACCOUNT_FILE, CALENDAR_ID

def xac_thuc_calendar():
    """
    Hàm xác thực và kết nối với Google Calendar API.
    Trả về đối tượng dịch vụ để tương tác với Google Calendar.
    """
    # Tạo đối tượng credentials từ tệp JSON của Service Account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Kết nối với Google Calendar API
    service = build('calendar', 'v3', credentials=credentials)
    
    return service,CALENDAR_ID

