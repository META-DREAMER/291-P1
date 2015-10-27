import gui.easygui as ui

def formPrompt(msg, title, fieldNames, isLogin):
    fieldValues = []
    errmsg = msg
    while 1:
        if isLogin:
            fieldValues = ui.multpasswordbox(errmsg, title, fieldNames, fieldValues)
        else:
            fieldValues = ui.multenterbox(errmsg, title, fieldNames, fieldValues)
        if fieldValues is None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg += '"%s" is a required field.\n\n' % fieldNames[i]
        if errmsg == "":
            break

    return fieldValues
