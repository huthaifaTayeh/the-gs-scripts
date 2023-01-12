from google.appscript.ui import *

class InputDialog:
    def __init__(self):
        self.dialog = createPrompt("Enter your name")
        self.text_box = self.dialog.addTextBox("Name")
        self.dialog.addButton("OK")

    def show(self):
        self.dialog.show()

    def get_input(self):
        return self.text_box.getText()

def take_input():
    dialog = InputDialog()
    dialog.show()
    name = dialog.get_input()
    return name
