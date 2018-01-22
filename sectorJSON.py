import json
from footsie import Share


def returnSectorJSON(shares, sector):
    """

    :param shares: A list containing all of the different shares in the FTSE100.
    :param sector: The sector which information is wanted for.
    :return JSON containing all of the shares in the sector requested.
    """

    json_string = list()
    for s in shares:
        if s.get_sector().upper() == sector.upper():
            json_string.append(json.loads(s.returnJSON()))
    return json.dumps(json_string)


def returnSubSectorJSON(shares, sub_sector):
    """

        :param shares: A list containing all of the different shares in the FTSE100.
        :param sub_sector: The sector which information is wanted for.
        :return JSON containing all of the shares in the sub-sector requested.
        """

    json_string = list()
    for s in shares:
        if s.get_sub_sector().upper() == sub_sector.upper():
            json_string.append(json.loads(s.returnJSON()))
    return json.dumps(json_string)


