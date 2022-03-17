def TeamContent(sector,numbers,racelist,rowdatas):
    if sector == "drivers":

        if racelist[5] not in numbers:
            numbers[racelist[5]] = str(racelist[1]) + " " + str(racelist[2])
        else:
            # elif str(numbers[racelist[5]]).count('&') =< 3:
            numbers[racelist[5]] += " & " + str(racelist[1]) + " " + str(racelist[2])

    else:
        rowdatas.append(racelist[1])
        if racelist[1] in numbers:
            rowdatas.append(numbers[str(racelist[1])])
        else:
            rowdatas.append("")
        rowdatas.append(racelist[2])

        return rowdatas