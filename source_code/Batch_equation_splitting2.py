def eqtn_split(eqtn):
    eqtn = eqtn.replace(" ", "")
    eqtn = eqtn.replace("\xa0", "")
    eqtn = eqtn + '+'
    temp1 = 0
    temp2 = 0
    temp3 = 0
    moles = []
    compounds = []
    derived = []
    for i in range(len(eqtn)):
        if eqtn[i] == '+':

            for j in range(i - temp1):
                if eqtn[temp1 + j].isidentifier():
                    temp2 = temp1 + j
                    break
            if '[' in eqtn[temp1:i]:
                for j in range(i - temp1):
                    if eqtn[temp1 + j] == '[':
                        temp3 = temp1 + j

                moles.append(float(eqtn[temp1:temp2]))
                compounds.append(eqtn[temp2:temp3])
                derived.append(eqtn[temp3 + 1:i - 1])

            else:
                moles.append(float(eqtn[temp1:temp2]))
                compounds.append(eqtn[temp2:i])
                derived.append("")

            temp1 = i + 1
    oxides = derived[:]
    for comp in range(len(compounds)):
        if derived[comp] == "":
            oxides[comp] = compounds[comp]
        else:
            oxides[comp] = derived[comp]

    return [moles, compounds, derived, oxides]
