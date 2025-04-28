from bot.agent_intent import intent_model
from bot.agent_extraction import *
from features import *

def full_flow(user_message: str):
    intent = intent_model(user_message)
    
    if not intent or intent.get('intent') == "normal_message":
        # extraction = {'content':get_llm(user_message)}
        extraction = {'intent': 'normal_message'}
        
    #Create event
    elif intent.get('intent') == "create_normal_event":
        extraction = create_event_extraction(user_message)
        
    #get event    
    elif intent.get('intent') == "get_first_calendar":
        # Extract datetime from text
        extraction = get_event_extraction(user_message,"get_first_calendar")
    elif intent.get('intent') == "get_freetime":
        # Extract datetime from text
        extraction = get_event_extraction(user_message,"get_freetime")
    elif intent.get('intent') == "get_multi_calendar":
        extraction = get_event_extraction(user_message,"get_multi_calendar")
        
    #Update event
    elif intent.get('intent') == "update_event":
        extraction = update_event_extraction(user_message)
        
    #Delete event
    elif intent.get('intent') == "delete_event":
        extraction = delete_event_extraction(user_message)
    print("intent", intent)
    print("extraction", extraction)    
    return {
            **intent,
            **extraction
        }
    
def call_api(event):
    print("Đang gọi api")
    try:
        if event.get('intent') == "create_normal_event":
            event = create_event_api(event)
        elif event.get('intent') == "get_first_calendar":
            event = get_first_calendar_api(event)
        elif event.get('intent') == "get_freetime":
            event = get_free_time_api(event)
        elif event.get('intent') == "get_multi_calendar":
            event = get_multi_calendar_api(event)
        elif event.get('intent') == "update_event":
            event = update_event_api(event)
        elif event.get('intent') == "delete_event":
            event = delete_event_api(event)
        else:
            event = {"error": "Đã xảy ra lỗi khi gọi API"}
        print("event", event)        
        return event
    except Exception as e:
        print("Lỗi khi gọi API:", e)
        return {"error": "Đã xảy ra lỗi khi gọi API"}