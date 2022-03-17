def listSet(curs):
    cellsdata = []
    vertic = []
    for x in curs:
        cellsdata.append(x[1:len(x)])
        vertic.append(str(x[0]))
    rows = len(cellsdata)

    return cellsdata, vertic, rows