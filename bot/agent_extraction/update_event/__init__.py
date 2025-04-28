from .datetime_extraction import extract_datetime_update_event
from .validate import agent_validate_update

def update_event_extraction(user_message: str):
    """
    Extracts the event details from the user message and agent response.
    """
    valid = agent_validate_update(user_message)
    
    datetime = extract_datetime_update_event(user_message)
    # Return the extracted information
    return {
        **valid,
        **datetime,
    }
    