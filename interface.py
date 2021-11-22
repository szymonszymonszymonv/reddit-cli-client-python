from time import sleep
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import print as rprint
import keyboard
import os
import fetch
from post import Post

console = Console()



# when switching from PostsView to CommentsView - update layout['main'] 
# tablegrid with panels - each post a panel
class PostsView():
    def __init__(self):
        self.active_index = 0
        self.posts = []
        self.posts_panels = []
        self.posts_layouts = []
        pass
    
    # load posts from api and show spinner
    def init_posts(self):
        self.posts = fetch.get_posts("all", 10)
        pass
    
    def init_posts_from_file(self):
        self.posts = Post.build_from_json()
    
    # put posts into table and the table into panel
    def build_view(self, layout: Layout):
        idx = 0
        for post in self.posts:
            panel = Panel(post.__str__(), style="blue", border_style="bright_black")
            self.posts_panels.append(panel)
            layout_item = Layout(name="item{idx}", size=4)
            layout_item.update(panel)
            self.posts_layouts.append(layout_item)
            layout.add_split(layout_item)
            idx += 1
            
        # return panel
        return layout


# tablegrid with panels - each comment a panel
class CommentsView():
    def __init__(self):
        self.active_index = 0
        self.comments = []

    def init_comments(self, post):
        for comment in post.comments:
            self.comments.append(comment)
    
    # put comments into table and the table into panel
    def build_view(self):
        table = Table.grid(expand=True)
        for comment in self.comments:
            table.add_row(comment)
            
        panel = Panel(table, style="white on blue")
        return panel


class Interface():
    def __init__(self):
        self.posts_view = PostsView()
        self.comments_view = CommentsView()
        self.active_view = self.posts_view # begin with displaying posts
        self.active_view.init_posts_from_file()
        self.active_item = self.active_view.active_index
        self.active_color = "green"
        self.default_color = "bright_black"
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        instructions = "↑: navigate up\t↓: navigate down\tEnter: show details"
        self.layout['header'].update(Panel("[b][yellow]Welcome to Reddit!", border_style="yellow"))
        self.layout['footer'].update(Panel(f"[orange1]{instructions}", border_style="orange1"))
        view = self.active_view.build_view(self.layout['main'])
        self.layout['main'].update(view)
        
        
    def clear(self):
        os.system('cls')

    def panels_go_up(self):
        idx = self.active_item
        if self.active_item == 0:
            return self.active_item
        else:
            self.active_view.posts_panels[idx]
            self.active_view.posts_panels[idx].border_style = self.default_color
            idx -= 1
            self.active_view.posts_panels[idx].border_style = self.active_color
            self.active_view.posts_layouts[idx].update(self.active_view.posts_panels[idx])
            return idx

    def panels_go_down(self):
        idx = self.active_item
        if idx == len(self.active_view.posts_layouts) - 1:
            return idx
        else:
            self.active_view.posts_panels[idx].border_style = self.default_color
            self.active_view.posts_layouts[idx].update(self.active_view.posts_panels[idx])
            idx += 1
            self.active_view.posts_panels[idx].border_style = self.active_color
            self.active_view.posts_layouts[idx].update(self.active_view.posts_panels[idx])
            return idx

    def render(self):
        self.clear()
        rprint(self.layout)
            
    def handle_arrow_down(self):
        self.active_item = self.panels_go_down()
        
    def handle_arrow_up(self):
        self.active_item = self.panels_go_up()
        
        
interface = Interface()

keyboard.add_hotkey('down', lambda: interface.handle_arrow_down())
keyboard.add_hotkey('up', lambda: interface.handle_arrow_up())

with Live(interface.layout, auto_refresh=True, refresh_per_second=4) as live:
    keyboard.wait()
