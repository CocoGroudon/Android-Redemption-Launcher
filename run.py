from pywinauto import Desktop

dlg = Desktop(backend="uia").UAC_dialog
if dlg.exists():
    dlg.yes.click()