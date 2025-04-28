from .datetime_extraction import extract_datetime_from_text
from .validate import agent_validate_create

def create_event_extraction(user_message: str):
    """
    Extracts the event details from the user message and agent response.
    """
    valid = agent_validate_create(user_message)
    
    datetime = extract_datetime_from_text(user_message,valid['is_recurring'])
    # Return the extracted information
    return {
        **valid,
        **datetime,
    }
    