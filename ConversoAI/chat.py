import flet as ft
from assistant import PrabalGpt

class Message():
    def __init__(self,user_name: str,text: str, message_type:str):
        self.user_name = user_name
        self.text = text
        self.message_type=message_type
        
class ChatMessage(ft.Row):
    
    def __init__(self,message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(value=self.get_initials(message.user_name)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name)
            ),
            ft.Column(
                [
                    ft.Text(message.user_name,weight="bold"),
                    ft.Text(message.text,selectable=True,width=500),
                ],
                tight=True,
                spacing=5,
            )
        ]
    # @staticmethod    
    def get_initials(self,user_name: str):
        return user_name[:1].capitalize()
        
    def get_avatar_color(self,uesr_name: str):
        color_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return color_lookup[hash(uesr_name) % len(color_lookup)]
            

def main(page: ft.Page):
    page.title = "PrabalGpt AI"
    # page.theme_mode = "light"
    # page.fonts = {
    #     "organical": "fonts/organical.ttf"
    # }
    
    smart_guru = PrabalGpt()
    
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "We need to know our names first!"
            join_user_name.update()
        else:
            page.session.set("user_name",join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, 
                                         text=f"{join_user_name.value} has joined the chat.", 
                                         message_type="login_message"
                                        )
                                )
            page.update()
      
    def send_message_click(e):
        if new_message.value != "":
            # sending the user input
            page.pubsub.send_all(Message(page.session.get("user_name"),
                                        new_message.value,
                                        message_type="chat_message"))
            
            # asking user to wait till we get our responce
            page.pubsub.send_all(Message(user_name="PrabalGpt",
                                        text="PrabalGpt is getting the response for you...",
                                        message_type="login_message"))
            
            # fetching the PrabalGpt AI responce
            ai_responce = smart_guru.PrabalGptResponse(str(new_message.value))
            page.pubsub.send_all(Message("PrabalGpt",str(ai_responce).lstrip(),message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()
            
            
    def on_message(message: Message):
        if message.message_type == "chat_message":
            m=ChatMessage(message)
        elif message.message_type=="login_message":
            m=ft.Text(message.text,italic=True, color=ft.Colors.BLACK45,size=12)
        chat.controls.append(m)
        page.update()
            
            
    page.pubsub.subscribe(on_message)     
    
    join_user_name = ft.TextField(
         label="Tell me your name...",
         autofocus=True,
         on_submit=join_chat_click,
    )
    
    # chat message
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    
    # 
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)]
        )
    
     # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius=20,
        on_submit=send_message_click,
        border_color=ft.Colors.BLUE
    ) 
    
    page.add(
        ft.Row([ft.Text("PrabalGpt AI", font_family="organical", 
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                        theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
                        color="blue")],alignment="center"),
        ft.Container(
            content=chat,
            border=ft.border.all(2,ft.Colors.BLUE),
            border_radius=20,
            padding=10,
            expand=True
        ),
        ft.Row([
            new_message,
            ft.IconButton(
                icon=ft.Icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=send_message_click,
                icon_color=ft.Colors.BLUE
            )
        ])
    )  
    
            
    

ft.app(target=main,assets_dir="assets")