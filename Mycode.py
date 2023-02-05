import win32evtlog
import win32security
import win32evtlogutil
import mariadb
import sys
import socket

hostname = socket.gethostname()
server = None
event_count = 0
log_types = ["application", "security", "system"]

def connect_database(user,password,host,port,database):
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def get_event_message(event, log_type):
    message = win32evtlogutil.SafeFormatMessage(event,log_type)
    return message

def sql(log_types):
        SQL = "INSERT INTO `" + log_types + "log` (`hostname`, `Index`, `EventID`, `TimeGenerated`, `EntryType`, `CategoryNumber`, `Message`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        return SQL

def check():
    pass

def dll_finder():
    pass

conn = connect_database("root","N011.nms1*","127.0.0.1",8629,"evt")
cur = conn.cursor()

for log_type in log_types:
    handler = win32evtlog.OpenEventLog(server, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    SQL = sql(log_type)
    event_count = 0
    while True:
        events = win32evtlog.ReadEventLog(handler, flags, 0)
        if events:
            for event in events:
                event_message = get_event_message(event, log_type)
                #                 hostname, index, EventID, TimeGen, Entry, Category, Message
                cur.execute(SQL,(hostname,event.RecordNumber,event.EventID,str(event.TimeGenerated),event.EventType,event.EventCategory,event_message))
                event_count+=1
        else:
            win32evtlog.CloseEventLog(handler)
            print(f"{log_type}의 데이터 전송완료된 이벤트 :{event_count}개")
            break
conn.commit()
conn.close()


