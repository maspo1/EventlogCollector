import win32evtlog
import win32security
import win32evtlogutil

def read_event_log(server, log_type):
    handler = win32evtlog.OpenEventLog(server, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(handler)
    events = win32evtlog.ReadEventLog(handler, flags, 0, total)
    win32evtlog.CloseEventLog(handler)
    return events

def get_event_message(event):
    message = win32evtlogutil.SafeFormatMessage(event,"Application")
    return message

server = None # Leave as None to access local machine event logs
log_types = ["Application", "Security", "System"]
for log_type in log_types:
    events = read_event_log(server, log_type)
    for event in events:
        event_message = get_event_message(event)
        print("Event Type: ", log_type)
        print("Event ID: ", event.EventID)
        print("Event Time: ", event.TimeGenerated)
        print("Event Message: ", event_message)
        print("\n")