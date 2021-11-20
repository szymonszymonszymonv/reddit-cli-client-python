from rich.panel import Panel
from rich import print as rprint
import keyboard
import os

class Interface():
    def __init__(self):
        panel = Panel.fit("[blue]Hi, I'm a Panel\nsometext\nothertext", border_style="green")
        panel2 = Panel.fit("[blue]im a panel too", border_style="bright_black")
        panel3 = Panel.fit("[blue]HEY ME TOO", border_style="bright_black")
        panel4 = Panel.fit("[blue]SAME WTF", border_style="bright_black")
        self.panels = [panel, panel2, panel3, panel4]
        self.active_panel = 0
        self.active_color = "green"
        self.default_color = "bright_black"
        
    def clear(self):
        os.system('cls')

    def panels_go_up(self):
        if self.active_panel == 0:
            return self.active_panel
        else:
            self.panels[self.active_panel].border_style = self.default_color
            self.active_panel -= 1
            self.panels[self.active_panel].border_style = self.active_color
            return self.active_panel

    def panels_go_down(self):
        if self.active_panel == len(self.panels) - 1:
            return self.active_panel
        else:
            self.panels[self.active_panel].border_style = self.default_color
            self.active_panel += 1
            self.panels[self.active_panel].border_style = self.active_color
            return self.active_panel

    def render(self):
        self.clear()
        for panel in self.panels:
            rprint(panel)
            
    def handle_arrow_down(self):
        self.active_panel = self.panels_go_down()
        self.render()
        
    def handle_arrow_up(self):
        self.active_panel = self.panels_go_up()
        self.render()
        
interface = Interface()
keyboard.add_hotkey('down', interface.handle_arrow_down)
keyboard.add_hotkey('up', interface.handle_arrow_up)

interface.render()

keyboard.wait()
