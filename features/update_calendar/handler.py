from config.calendar import xac_thuc_calendar
from utils import *

def update_event_api(function_args: dict, timeZone:str = "Asia/Ho_Chi_Minh") -> dict:
    """
    Tìm kiếm sự kiện trong khoảng thời gian, nếu chỉ có 1 sự kiện thì tiến hành cập nhật, nếu có nhiều sự kiện thì trả về danh sách các sự kiện đó.

    Parameters:
    time_min (str): Thời gian bắt đầu (ISO 8601).
    time_max (str): Thời gian kết thúc (ISO 8601).
    updated_event (dict): Thông tin cập nhật sự kiện.

    Returns:
    dict: Thông tin của sự kiện đã được cập nhật hoặc danh sách sự kiện trong khoảng thời gian.
    """
    service, calendar_id = xac_thuc_calendar()
    print("function_args", function_args)
    if function_args['incorrect_datetime']:
        return invalid_time
    try:
        st_datetime_str = convert_to_iso_format(function_args['datetime_ranges'][0]['start_datetime'])
        ed_datetime_str = convert_to_iso_format(function_args['datetime_ranges'][0]['end_datetime'])
        st_new_str = convert_to_iso_format(function_args['datetime_ranges'][0]['start_new'])
        ed_new_str = convert_to_iso_format(function_args['datetime_ranges'][0]['end_new'])
    except Exception as e:
        print(e) 
    # Lấy danh sách sự kiện trong khoảng thời gian
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=st_datetime_str,
        timeMax=ed_datetime_str,
        singleEvents=True,
        orderBy='startTime',
        timeZone=timeZone,
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return {"error":message_no_get_calendar}
    
    if len(events) == 1:
        # Cập nhật sự kiện nếu chỉ có 1 sự kiện
        event_id = events[0]['id']
        event = events[0]
        
        # Cập nhật các thông tin sự kiện
        event['summary'] = function_args['title']
        event['location'] = function_args['location']
        event['start'] = {
            'dateTime': st_new_str,
            'timeZone': timeZone,
        }
        event['end'] = {
            'dateTime': ed_new_str,
            'timeZone': timeZone,
        }

        # Cập nhật sự kiện
        updated_event_response = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event,
            timeZone=timeZone,
        ).execute()

        return updated_event_response
    
    # Nếu có nhiều hơn 1 sự kiện, trả về danh sách sự kiện
    event_list = []
    for event in events:
        event_list.append({
            'id': event['id'],
            'summary': event.get('summary', ''),
            'start': event.get('start', {}).get('dateTime', ''),
            'end': event.get('end', {}).get('dateTime', '')
        })

    return event_list