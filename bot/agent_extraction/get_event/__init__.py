from .datetime_extraction import extract_datetime_get_event
from .validate import agent_validate_get

def get_event_extraction(user_message: str, intent: str):
    """
    Extracts the event details from the user message and agent response.
    """
    valid = agent_validate_get(user_message)
    
    datetime = extract_datetime_get_event(user_message,intent)
    # Return the extracted information
    return {
        **valid,
        **datetime,
    }
    