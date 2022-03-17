def tabHeight(lay,sorthide,tabrow):

    x = 470 + (tabrow + 1) * 40
    if sorthide == False or x > 850:
        lay.setFixedHeight(850)

        if sorthide != False:
            lay.table.setFixedHeight(375)
        else:
            lay.table.setFixedHeight(340)
    else:
        lay.setFixedHeight(x)
        lay.table.setFixedHeight(x - 470)
