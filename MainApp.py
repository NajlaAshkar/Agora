from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from Models import validate_database
import Models.Mapping as Mapping


class MainApp(MDApp):
    def build(self):
        #print(Mapping.get_region("GIZO "))
        return MDLabel(text="Hello, World", halign="center")


if __name__ == '__main__':
    validate_database()
    MDApp = MainApp()
    MDApp.run()
