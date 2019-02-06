

import matplotlib.pyplot as plt
import numpy as np

input_file = 'filenum1.txt'


def fit_linear(input_file):
    sum1 = 0    # sum for make things easy :)
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0
    sum6 = 0
    sum7 = 0
    sum8 = 0
    chi = 0    # the sum of all chi, from i to N
    d = []    # list
    c = []    # list
    b = []    # list
    p = []     # list
    K = []      # list
    new_list = [[], [], [], []]   # list
    Ylist = []   # list that contains all the values of Y
    Xlist = []   # list that contains all the values of X
    XYlist = []  # list that contains all the values of Y*X
    X2list = []  # list that contains all the values of x^2
    dYlist = []  # list that contains all the values of dY
    dy2list = []  # list that contains all the values of dY^2
    dXlist = []   # list that contains all the values of dX
    a = ['dx', 'x', 'y', 'dy']
    new_c = [] # list
    myfile = open(input_file, 'r+')
    data = myfile.readlines()
    Y = data[0].lower()
    Ytitle = data[len(data) - 1].split()  # all the introduction to title of y
    Xtitle = data[len(data) - 2].split()  # all the introduction to title of x
    XtitleReady = [] # the name of the title X
    YtitleReady = []  # the name of the title Y


    for i in Y:   # check if rows or col?
        if i in a:
            sum1 = sum1 + 1
    # COLLLLLLLLLLLLLLLLLL######################
    if sum1 > 2:  # it's cols
        # for k in range(0,len(data)-2):
        for l in range(0, len(data) - 3):
            v = data[l].lower().split()
            K.append(v)

        for i in K:  # Error length for col
            if len(i) != 4:
                return "Input file error: Data lists are not the same length"
                exit()

        for j in K:  # convert from col to rows
            p.append(len(j))
            new_list[0].append(j[0])
            new_list[1].append(j[1])
            new_list[2].append(j[2])
            new_list[3].append(j[3])

        for a in new_list:  # convert string to float
            for z in range(1, len(a)):
                a[z] = float(a[z])

        for b in new_list:  # Error positive in cols
            if 'dx' in b:      # check Error positive for dx in cols
                for z in b:
                    if type(z) == float and z > 0:
                        sum2 = sum2 + 1
                if sum2 + 1 != len(b):
                    return "Input file error: Not all uncertainties are positive"
                    exit()

            if 'dy' in b:      # check Error positive for dy in cols
                for z in b:
                    if type(z) == float and z > 0:
                        sum3 = sum3 + 1
                if sum3 + 1 != len(b):
                    return "Input file error: Not all uncertainties are positive"
                    exit()

        for u in new_list:  # find a,b,da,db,chi2,chi
            if 'x' in u:   # find x average
                for i in u:
                    if type(i) == float:
                        Xlist.append(i)
                        X2list.append(i ** 2)  # x^2
                        N = len(Xlist)
                        sum4 = sum4 + i
                Xaverage = sum4 / (len(u) - 1)

            if 'y' in u:  # find y average
                for i in u:
                    if type(i) == float:
                        Ylist.append(i)
                        sum5 = sum5 + i
                Yaverage = sum5 / (len(u) - 1)

            if 'dy' in u:  # find dy average
                for i in u:
                    if type(i) == float:
                        dYlist.append(i)
                        dy2list.append(i ** 2)
                        sum5 = sum5 + i
                dYaverage = sum5 / (len(u) - 1)

            if 'dx' in u:  # dx values in list
                for i in u:
                    if type(i)==float:
                        dXlist.append(i)

        for f in range(0, len(Xlist)): # list that contains the values of x*y
            z1x = Xlist[f]
            z2y = Ylist[f]
            z3 = z1x * z2y
            XYlist.append(z3)

        for j in XYlist: # the average of x*y
            sum6 = sum6 + j
        XYaverage = sum6 / len(XYlist)

        for n in X2list: # the sum of x^2 values
            sum7 = sum7 + n

        for j in dy2list: # the sum of dy^2 values
            sum8 = sum8 + j

        dy2average = sum8 / len(dy2list)  # find dy^2 average
        X2average = sum7 / len(X2list)    # find x^2 average

        a = (XYaverage - (Xaverage * Yaverage)) / (X2average - Xaverage ** 2)  # find a
        da = (dy2average / (N * (X2average - Xaverage ** 2)))                   # find da
        b = (Yaverage - a * Xaverage)                                            # find b
        db = (da * X2average)                                                     # find db

        for j in range(0, len(Xlist)):     # find the value of chi2
            chi1 = ((Ylist[j] - (a * Xlist[j] + b)) / (dYlist[j])) ** 2
            chi = chi + chi1
        for i in range(2, len(Xtitle)):    # list contains the title of X
            XtitleReady.append(Xtitle[i])

        for i in range(2, len(Ytitle)):    # list contains the title of Y
            YtitleReady.append(Ytitle[i])

        XtitleReady2 = XtitleReady[0]+" "+ XtitleReady[1]  # the title of X
        YtitleReady2 = YtitleReady[0]+" "+ YtitleReady[1]   # the title of Y

        chi2_reduced = (chi ** 2) / (N - 2)    # chi2_reduced value

        def test3():              # print the values of a,da,b,db,chi2,chi2_reduced
            print("a =", a, "+-", da, '\n')
            print("b =", b, "+-", db, '\n')
            print("chi2 =", chi, '\n')
            print("chi2_reduced =", chi2_reduced)

        test3()

        # plot the linear function
        x = np.array(Xlist)
        my_y = np.array(Ylist)
        formula = a * x + b    # the linear graph function l
        xerr = np.array(dXlist)
        yerr = np.array(dYlist)

        y = formula
        plt.errorbar(x, my_y, yerr=yerr, xerr=xerr, fmt='none', ecolor='b')
        plt.plot(x, y, "r")            # plot the function
        plt.ylabel(YtitleReady2)       # set the title of y
        plt.xlabel(XtitleReady2)       # set the title of x
        plt.show()                     # show the results
        plt.savefig("linear_fit.svg")  # save the figure

    ############################################ROW###########ROW#########ROW#########
    if sum1 <= 1:  # it's rows

        for g in range(0, 4):       # split rows into one list
            x = (data[g])
            b.append(x)
        strip_list = [item.lower().strip() for item in b]
        b = strip_list

        for h in b:
            z = h.split()
            c.append(z)

        for i in c:   # to check if all the rows have the same length
            x = len(i)
            d.append(x)

        for i in d:   # Error length for rows
            if d[0] != d[1] and d[0] != d[2] and d[3] != d[0]:
                return "Input file error: Data lists are not the same length"
                exit()

        for a in c:  # convert numbers from strings to float
            for z in range(1, len(a)):
                a[z] = float(a[z])

        for b in c:                #Error positive in rows
            if 'dx' in b:        # check Error positive for dx in rows
                for z in b:
                    if type(z) == float and z > 0:
                        sum2 = sum2 + 1
                if sum2 + 1 != len(b):
                    return "Input file error: Not all uncertainties are positive"
                    exit()

            if 'dy' in b:   # check Error positive for dy in rows
                for z in b:
                    if type(z) == float and z > 0:
                        sum3 = sum3 + 1
                if sum3 + 1 != len(b):
                    return "Input file error: Not all uncertainties are positive"
                    exit()

        for u in new_list:  #find a,b,da,db,chi2,chi
            if 'x' in u:   #find x average
                for i in u:
                    if type(i) == float:
                        Xlist.append(i)
                        X2list.append(i ** 2)  # x^2
                        N = len(Xlist)
                        sum4 = sum4 + i
                Xaverage = sum4 / (len(u) - 1)

            if 'y' in u:  # find y average
                for i in u:
                    if type(i) == float:
                        Ylist.append(i)
                        sum5 = sum5 + i
                Yaverage = sum5 / (len(u) - 1)

            if 'dy' in u:  # find dy average
                for i in u:
                    if type(i) == float:
                        dYlist.append(i)
                        dy2list.append(i ** 2)
                        sum5 = sum5 + i
                dYaverage = sum5 / (len(u) - 1)

            if 'dx' in u:  # dx values in list
                for i in u:
                    if type(i)==float:
                        dXlist.append(i)

        for f in range(0, len(Xlist)): # list that contains the values of x*y
            z1x = Xlist[f]
            z2y = Ylist[f]
            z3 = z1x * z2y
            XYlist.append(z3)

        for j in XYlist: # the average of x*y
            sum6 = sum6 + j
        XYaverage = sum6 / len(XYlist)

        for n in X2list: # the sum of x^2 values
            sum7 = sum7 + n

        for j in dy2list: # the sum of dy^2 values
            sum8 = sum8 + j

        dy2average = sum8 / len(dy2list)  # find dy^2 average
        X2average = sum7 / len(X2list)    # find x^2 average

        a = (XYaverage - (Xaverage * Yaverage)) / (X2average - Xaverage ** 2)  # find a
        da = (dy2average / (N * (X2average - Xaverage ** 2)))                   # find da
        b = (Yaverage - a * Xaverage)                                            # find b
        db = (da * X2average)                                                     # find db

        for j in range(0, len(Xlist)):     # find the value of chi2
            chi1 = ((Ylist[j] - (a * Xlist[j] + b)) / (dYlist[j])) ** 2
            chi = chi + chi1
        for i in range(2, len(Xtitle)):    # list contains the title of X
            XtitleReady.append(Xtitle[i])

        for i in range(2, len(Ytitle)):    # list contains the title of Y
            YtitleReady.append(Ytitle[i])

        XtitleReady2 = XtitleReady[0]+" "+ XtitleReady[1]  # the title of X
        YtitleReady2 = YtitleReady[0]+" "+ YtitleReady[1]   # the title of Y

        chi2_reduced = (chi ** 2) / (N - 2)    # chi2_reduced value

        # return a,da,b,db,chi,chi2_reduced
        def test3():  # print the values of a,da,b,db,chi2,chi2_reduced
            print("a =", a, "+-", da, '\n')
            print("b =", b, "+-", db, '\n')
            print("chi2 =", chi, '\n')
            print("chi2_reduced =", chi2_reduced)

        test3()

        # plot the linear function
        x = np.array(Xlist)
        my_y = np.array(Ylist)
        formula = a * x + b  # the linear graph function l
        xerr = np.array(dXlist)
        yerr = np.array(dYlist)

        y = formula
        plt.errorbar(x, my_y, yerr=yerr, xerr=xerr, fmt='none', ecolor='b')
        plt.plot(x, y, "r")  # plot the function
        plt.ylabel(YtitleReady2)  # set the title of y
        plt.xlabel(XtitleReady2)  # set the title of x
        plt.show()  # show the results
        plt.savefig("linear_fit.svg")  # save the figure

        myfile.close()  # close file

print(fit_linear(input_file))
