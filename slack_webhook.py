from slack_sdk import WebClient
from datetime import datetime, timedelta
import pandas as pd
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

with open("token",'r+') as f:
    client = WebClient(token=f.read())
channel_id = "D043GTBAVEV"

# listing the scheduled messages
def list_scheduled_messages(channel):
    print("Yo")
    response = client.chat_scheduledMessages_list(channel=channel)
    messages = response.data.get('scheduled_messages')
    ids = []
    for msg in messages:
        ids.append(msg.get('id'))

    print(ids,len(ids))
    return True


def ids_func(i):
        result=client.chat_deleteScheduledMessage(
                channel=channel_id, scheduled_message_id=i)
        return(result)

# delete the scheduled messages 
def delete_scheduled_messages(ids):
        x = lambda b : ids.replace(b,'')
        ids=x('[')
        ids=x(']')
        ids=x("'")
        ids = (ids.split(','))
        print("The list of messages: ")
        print(ids,type(ids))
        for i in ids:
            try:
                print("..................")
                print(i.strip())
                print("----------------------------------------------------------------------")
                print(ids_func(i.strip()))
                print("----------------------------------------------------------------------")
        
            except Exception as e:
                    print(e)
        return True
            
# scheduled the messages
def schedule_messages():
    ids = []
    dictofschedules={}
    count=1
    for i in range(10):
            now = datetime.now()
            now_plus_10 = (now + timedelta(minutes = 2*count)).strftime('%s')
            result = client.chat_scheduleMessage(
                channel=channel_id,
                text="The certificate of "+slack_info[1]+" is expired on "+slack_info[2]+" "+slack_info[3]+" "+slack_info[4]+" at "+slack_info[5]+" "+slack_info[6],
                # post_at=schedule_timestamp
                post_at=now_plus_10
            )
            id_ = result.get('scheduled_message_id')
            print('id_',type(id_))
            ids.append(id_)
            print()
            print("Nowplus_10: ", now_plus_10," + ",id_+" Time "+str(now + timedelta(minutes = 2*count)))
            count+=1
    df_header_index_col = pd.read_csv('schedule.csv', sep=',',names=('nameoffile','schedulers'))
    df_header_index_col.loc[len(df_header_index_col.index)] = [slack_info[1], ids ]
    df_header_index_col.to_csv('schedule.csv',header=False,index=False)


if __name__ == "__main__":
    slack_info =[]
    for thing in sys.argv:
        slack_info.append(thing)
    if slack_info[1]=='0':
        print("-----------------------------------------------------------------------------------------------------")
        print("The list of scheduled messages: ")
        list_scheduled_messages(channel_id)
        print("-----------------------------------------------------------------------------------------------------")
        if delete_scheduled_messages(slack_info[2]):
            print(slack_info[2],slack_info[3])
            import pandas as pd
            df_header_index_col = pd.read_csv('schedule.csv', sep=',',names=('nameoffile','schedulers'))
            # df_header_index_col = df_header_index_col.reset_index() 
            print("Starting:",df_header_index_col)
            for a,b in df_header_index_col.iterrows():
                print(b['nameoffile']+"............."+b['schedulers'])
                if b['nameoffile']== slack_info[3] and b['schedulers']==slack_info[2]:
                    print(a)
                    df_header_index_col = df_header_index_col.drop(a)
            print("Ending:",df_header_index_col)
            df_header_index_col.to_csv('schedule.csv',header=False,index=False)
        print("-----------------------------------------------------------------------------------------------------")
        print("The list of scheduled messages: ")
        list_scheduled_messages(channel_id)
        print("-----------------------------------------------------------------------------------------------------")
    elif slack_info[7]=='1':
        schedule_messages()
        list_scheduled_messages(channel_id)
    
