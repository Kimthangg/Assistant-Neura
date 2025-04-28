from config.calendar import xac_thuc_calendar
from utils import *

def create_event_api(event_data, timeZone:str = "Asia/Ho_Chi_Minh"):
    # Tạo sự kiện theo định dạng của Google Calendar API
    event = {
        'summary': event_data['title'],
        'location': event_data['location'],
        'start': {
            'dateTime': convert_to_iso_format(event_data['datetime_ranges'][0]['start_datetime']),
            'timeZone': timeZone,
        },
        'end': {
            'dateTime': convert_to_iso_format(event_data['datetime_ranges'][0]['end_datetime']),
            'timeZone': timeZone,
        }
    }
    # Kiểm tra và thêm phần RRULE nếu có
    if 'rrules' in event_data['datetime_ranges'][0]:
        event['recurrence'] = [
            event_data['datetime_ranges'][0]['rrules']  # Thêm RRULE vào trong phần recurrence
        ]
    print(event)
    # Tạo đối tượng dịch vụ Google Calendar API
    service, CALENDAR_ID = xac_thuc_calendar()
    try:
        # Kiểm tra xem sự kiện đã tồn tại hay chưa
        created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Sự kiện đã được tạo: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"Lỗi khi kiểm tra sự kiện: {e}")
        return {"error": str(e)}
    return event