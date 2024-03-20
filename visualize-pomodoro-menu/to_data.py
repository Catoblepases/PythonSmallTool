import os
import json
import datetime

LOCATION="/Users/celes/Library/Containers/com.github.ivoronin.TomatoBar/Data/Library/Caches/TomatoBar.log"
def load_log_file(filename):
    data = []
    with open(filename, "r") as file:
        for line in file:
            try:
                json_object = json.loads(line)
                if "event" in json_object:
                    data.append(json_object)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from line: {line.strip()}")

    return data


def create_event_list(filename):
    content = load_log_file(filename)
    Event_List = []
    for obj in content:
        if obj["toState"] == "work":
            start = obj["timestamp"]
        elif (start != -1) and (
            (obj["toState"] == "rest") or (obj["toState"] == "idle")
        ):
            end = obj["timestamp"]
            datetime_start = datetime.datetime.fromtimestamp(start)
            datetime_end = datetime.datetime.fromtimestamp(end)
            Event_List.append(
                {
                    "date": datetime_start,
                    "focustime": round(
                        (datetime_end - datetime_start).total_seconds() / 60
                    ),
                }
            )
            start = -1
    return Event_List


def create_date_list(Event_List):
    dic = dict()
    for item in Event_List:
        date, focustime = item["date"].date(), item["focustime"]
        if date in dic:
            dic[date] += round(focustime / 60, 1)
        else:
            dic[date] = round(focustime / 60, 1)
    return dic


def export_date_list():
    return create_date_list(create_event_list(LOCATION))
