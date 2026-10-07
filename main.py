import dearpygui.dearpygui as dpg
from network import NetworkManager
from commands import CommandParser

WIDTH = 1280
HEIGHT = 800

def present_status(status_t):
    dpg.add_text(f"[System]: {status_t}", parent="chat_logs")

def present_message(sender, app_data, user_data):
    msg = dpg.get_value("input_t")
    msg.strip()
    if user_data[1]:
        dpg.add_text("Peer: " + msg, parent="chat_logs")
        return
    else:
        if msg.startswith('/'):
            commander.process(msg)
        else:
            commander.process(msg)
            dpg.add_text("You: " + msg, parent="chat_logs")
    
    dpg.set_value("input_t", "")
    
net = NetworkManager(present_status)
commander = CommandParser(net, present_status)


dpg.create_context()
dpg.create_viewport(title="Pyrrot", width=1280, height=800, resizable=False)

with dpg.window(label="Chat Logs", width=WIDTH, height=HEIGHT - 35, no_resize=True, no_collapse=True, no_move=True, no_close=True):
    with dpg.child_window(tag="chat_logs", width=-1, height=-1):
        pass

with dpg.window(tag="input_area", no_title_bar=True, width=WIDTH, height=35, pos=[0, HEIGHT - 35], no_resize=True, no_collapse=True, no_move=True, no_close=True):
    dpg.add_input_text(tag="input_t", hint="Enter a message or command...", width=WIDTH - 100, on_enter=True, callback=present_message, user_data=[dpg.get_value("input_t"), False])
    dpg.add_button(label="Send", pos=[WIDTH - 85, 8], width=78, callback=present_message, user_data=[dpg.get_value("input_t"), False])
    

dpg.setup_dearpygui()
dpg.show_viewport()


while dpg.is_dearpygui_running():
    while not net.incoming.qsize() == 0:
        message = net.incoming.get_nowait()
        dpg.add_text(f"{net.addr[0]}: {message}", parent="chat_logs")

    dpg.render_dearpygui_frame()

dpg.destroy_context()