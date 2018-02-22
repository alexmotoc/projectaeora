import json


def obj_dict(obj):
    return obj.__dict__


def news_reply(lse_list, yahoo_list):
    overall_dict = {
        "London Stock Exchange": lse_list,
        "Yahoo News": yahoo_list
                    }

    output_json = json.dumps(overall_dict, default=lambda o: o.__dict__, indent=4)

    return output_json
