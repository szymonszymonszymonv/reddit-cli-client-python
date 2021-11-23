import logging
from time import sleep
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
from rich.prompt import Prompt
from rich import print as rprint
import keyboard
import os
from comment import Comment
import fetch
from post import Post

console = Console()

class PostsView():
    def __init__(self):
        self.active_index = 0
        self.posts = []
        self.panels = []
        self.layouts = []
        self.subreddit = "all"
        self.page = 0
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
    
    # load posts from api and show spinner
    def init_posts(self, subreddit="all", after="", before=""):
        self.subreddit=subreddit
        self.init_header_footer()
        self.posts = fetch.get_posts(subreddit, 5, after, before)
        pass
    
    def init_header_footer(self):
        instructions = "↑: navigate up / ↓: navigate down / Enter: show details"
        self.layout['header'].update(Panel(f"[b][yellow]You are browsing /r/{self.subreddit}", border_style="yellow"))
        self.layout['footer'].update(Panel(f"[orange1]{instructions}", border_style="orange1"))
    
    def init_posts_from_file(self):
        self.posts = Post.build_from_json()

    def build_view(self):
        idx = 0
        layout = self.layout['main']
        for post in self.posts:
            panel = Panel(post.__str__(), style="orange4", height=5, border_style="bright_black")
            self.panels.append(panel)
            layout_item = Layout(name="item{idx}", size=5)
            
            layout_item.update(panel)
            self.layouts.append(layout_item)
            layout.add_split(layout_item)
            idx += 1
            
        self.layout['main'].update(layout)
        return self.layout

# tablegrid with panels - each comment a panel
class CommentsView():
    def __init__(self, post):
        self.active_index = 0
        self.comments = []
        self.post = post
        self.panels = []
        self.layouts = []
        
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=6),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        instructions = "↑: navigate up / ↓: navigate down / Backspace: show posts"
        self.layout['header'].update(Panel(f"[b][yellow3]{self.post.title}\n[yellow2]{self.post.selftext}", border_style="red"))
        self.layout['footer'].update(Panel(f"[orange1]{instructions}", border_style="orange1"))

    def init_comments(self, post):
        for comment in post.comments:
            self.comments.append(Comment.build_from_dict(comment))
        
    def init_comments_from_file(self):
        self.comments = Comment.build_from_json("1comments_test1.json")
    
    # put comments into table and the table into panel
    def build_view(self):
        idx = 0
        layout = self.layout['main']
        for comment in self.comments:
            panel = Panel(comment.__str__(), style="blue", border_style="bright_black")
            self.panels.append(panel)
            layout_item = Layout(name="item{idx}", size=5)
            layout_item.update(panel)
            self.layouts.append(layout_item)
            layout.add_split(layout_item)
            idx += 1
            
        self.layout['main'].update(layout)
        return self.layout

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

class Container():
    def __init__(self):
        self.active_item = 0
        self.active_view = None
        self.posts_view = None
        self.comms_view = None
        self.active_color = "green"
        self.default_color = "bright_black"
        self.layout = Layout()
    
    def load_posts_view(self):
        logger.info("loading post view")
        
        pv = PostsView()
        pv.init_posts(subreddit="all")
        self.layout.update(pv.build_view())
        self.posts_view = pv
        self.active_view = pv
        
    def load_comms_view(self):
        logger.info("loading comments view")
        cv = CommentsView(self.posts_view.posts[self.active_item])
        cv.init_comments(self.posts_view.posts[self.active_item])
        self.layout.update(cv.build_view())
        self.comms_view = cv
        
    def change_to_comms_view(self):
        logger.info("changing to comments view")
        if len(self.posts_view.posts[self.active_item].comments) == 0:
            return 0
        self.posts_view.active_index = self.active_item
        self.load_comms_view()
        self.active_item = 0
        self.active_view = self.comms_view
        
    def change_to_posts_view(self):
        logger.info("changing to posts view")
        self.active_view = self.posts_view
        self.active_item = self.posts_view.active_index
        self.layout.update(self.posts_view.layout)
        
    def posts_turn_page_right(self):
        self.active_item = 0
        logger.info("turning page right")
        self.layout.update(Panel(Spinner('material', text="LOADING POSTS"), style="orange4"))
        last_post = self.posts_view.posts[-1]
        pv = PostsView()
        pv.page = self.posts_view.page + 1
        pv.init_posts(self.posts_view.subreddit, f"t3_{last_post.id}")
        self.layout.update(pv.build_view())
        self.posts_view = pv
        self.active_view = pv
        pass
    
    def posts_turn_page_left(self):
        if self.posts_view.page > 0:
            self.active_item = 0
            logger.info("turning page right")
            self.layout.update(Panel(Spinner('material', text="LOADING POSTS"), style="orange4"))
            first_post = self.posts_view.posts[0]
            pv = PostsView()
            pv.page = self.posts_view.page - 1
            pv.init_posts(self.posts_view.subreddit, before=f"t3_{first_post.id}")
            self.layout.update(pv.build_view())
            self.posts_view = pv
            self.active_view = pv
    
    def panels_go_up(self):
        logger.info("GOING UP")
        idx = self.active_item
        if self.active_item == 0:
            return self.active_item
        else:
            self.active_view.panels[idx]
            self.active_view.panels[idx].border_style = self.default_color
            idx -= 1
            self.active_view.panels[idx].border_style = self.active_color
            self.active_view.layouts[idx].update(self.active_view.panels[idx])
            return idx

    def panels_go_down(self):
        logger.info("GOING DOWN")
        idx = self.active_item
        if idx == len(self.active_view.layouts) - 1:
            return idx
        else:
            self.active_view.panels[idx].border_style = self.default_color
            self.active_view.layouts[idx].update(self.active_view.panels[idx])
            idx += 1
            self.active_view.panels[idx].border_style = self.active_color
            self.active_view.layouts[idx].update(self.active_view.panels[idx])
            return idx
        
    def handle_arrow_up(self):
        self.active_item = self.panels_go_up()
        
    def handle_arrow_down(self):
        self.active_item = self.panels_go_down()
        
cont = Container()
logger.info("creating a Container instance")
cont.load_posts_view()

keyboard.add_hotkey('enter', lambda: cont.change_to_comms_view())
logger.info("adding enter listener")
keyboard.add_hotkey('backspace', lambda: cont.change_to_posts_view())
logger.info("adding backspace listener")
keyboard.add_hotkey('up', lambda: cont.handle_arrow_up())
logger.info("adding up arrow listener")
keyboard.add_hotkey('down', lambda: cont.handle_arrow_down())
logger.info("adding down arrow listener")
keyboard.add_hotkey('right', lambda: cont.posts_turn_page_right())
logger.info("adding right arrow listener")
keyboard.add_hotkey('left', lambda: cont.posts_turn_page_left())
logger.info("adding left arrow listener")

with Live(cont.layout, console=console, refresh_per_second=15) as live:
    while(True):
        logger.info("waiting for keyboard input")
        keyboard.wait()


