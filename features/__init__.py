from .create_calendar.event.handler import *
# from .create_calendar.task.handler import *
from .get_calendar.first_calendar.handler import *
from .get_calendar.free_time.handler import *
from .get_calendar.multi_calendar.handler import *
from .update_calendar.handler import *
from .delete_calendar.handler import *
from .normal_message.handler import *

from .create_calendar.event.example import *
# from .create_calendar.task.example import *
from .get_calendar.first_calendar.example import*
from .get_calendar.free_time.example import *
from .get_calendar.multi_calendar.example import *

from .update_calendar.example import *
from .delete_calendar.example import *
from .normal_message.example import *

calendar_features_map = {
    "normal_message": {
    # "handler_message": chitchat,
    "example": None,
    "tools": None,
    "system_message": "",
    "intent_system_message":""
    },
    
    "create_normal_event": {
        "handler_message": create_event_api,
        "example": create_event_example,
        # "tools": tool_create_event_with_title,
        "system_message": "",
        "intent_system_message":""
    },

    "create_task": {
        # "handler_message": process_message_create_task,
        # "example": create_task_example,
        # "tools": tool_create_task,
        "system_message": "",
        "intent_system_message":""
    },
    "get_first_calendar": {
        "handler_message": get_first_calendar_api,
        "example": get_first_calendar_example,
        # "tools": tool_get_first_calendar,
        "system_message": "",
        "intent_system_message":""
    },
    "get_freetime": {
        "handler_message": get_free_time_api,
        "example": get_free_time_example,
        # "tools": tool_get_freetime,
        "system_message": "",
        "intent_system_message":""
    },
    "get_multi_calendar": {
        "handler_message": get_multi_calendar_api,
        "example": get_multi_calendar_example,
        # "tools": tool_get_calendar,
        "system_message": "",
        "intent_system_message":""
    },
    
    "update_event": {
      "handler_message": update_event_api,
      "example": update_example,
      
      "system_message": "",
      "intent_system_message": ""
    },
    "delete_event": {
      "handler_message": delete_event_api,
      "example": delete_event_example,
      
      "system_message": "",
      "intent_system_message": ""
    },

}


def intent_example_dict():
    intent_example = {}
    for key, feature in calendar_features_map.items():
        # Check if intent_system_message is not None or empty
        intent_system_message = feature.get("intent_system_message")
        if intent_system_message:
            intent_example[intent_system_message] = key
        elif feature.get("example"):
            for example in feature["example"]:
                intent_example[example] = key
    return intent_example
