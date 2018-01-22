import json
from footsie import Share


def returnSectorJSON(shares, sector):
    """

    :param shares: A list containing all of the different in the FTSE100.
    :param sector: The sector which information is wanted for.
    """

    json_string = list()

    for s in shares:
        if s.get_sector().upper() == sector.upper():
            json_string.append(json.loads(s.returnJSON()))
    return json.dumps(json_string)

