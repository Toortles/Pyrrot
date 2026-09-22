import dearpygui.dearpygui as dpg
from datetime import datetime as time
from network import NetworkManager

# Formatting Shortcuts
WIDTH = 1280
HEIGHT = 800
IN_H = 35

def status_message(status: str):
    dpg.add_text("[SYSTEM]: " + status, parent="chat_logs")

def display_message(text: str, own: bool):
    label = "You" if own else "Peer"
    dpg.add_text(f"{label} @ " + time.now().strftime("%H:%M:%S"), parent="chat_logs", wrap=WIDTH)
    dpg.add_text(text, parent="chat_logs")

def on_send(sender=None, app_data=None, user_data=None):
    local_text = dpg.get_value("msg_input")

    if not local_text:
        return # Don't do anything if there's no text

    net_manager.send_message(local_text)
    display_message(local_text, True)
    dpg.set_value("msg_input", "")

net_manager = NetworkManager()

dpg.create_context()
dpg.create_viewport(title="Pyrrot", width=WIDTH, height=HEIGHT, resizable=False)

with dpg.window(label="Chat", width=WIDTH, height=HEIGHT - IN_H, no_resize=True, no_move=True):
    with dpg.child_window(tag="chat_logs", height=-1, autosize_x=True):
        pass

with dpg.window(no_title_bar=True, width=WIDTH, height=IN_H, pos=[0, HEIGHT - IN_H], no_resize=True, no_move=True):
    dpg.add_input_text(tag="msg_input", hint="Enter a message...", width=WIDTH - 100, on_enter=True, callback=on_send)
    dpg.add_button(label="Send", callback=on_send, width=80, height=19, pos=[WIDTH - 85, 8])

def process_messages():
    messages = net_manager.get_queued_messages()

    for text in messages:
        display_message(text, False)

net_manager.start_connection("127.0.0.1", status_cb=status_message)

dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    
    process_messages()

    dpg.render_dearpygui_frame()

dpg.destroy_context()