import dearpygui.dearpygui as dpg
from datetime import datetime as time

# Formatting Shortcuts
WIDTH = 1280
HEIGHT = 800
IN_H = 35

def add_message():
    text = dpg.get_value("msg_input")
    dpg.add_text(text, parent="left_cell", wrap=dpg.get_item_width("left_cell"))
    dpg.add_text("@ " + time.now().strftime("%H:%M:%S"), parent="right_cell", wrap=-1)
    dpg.set_value("msg_input", "")

dpg.create_context()
dpg.create_viewport(title="Pyrrot", width=WIDTH, height=HEIGHT, resizable=False)

with dpg.window(label="Chat", width=WIDTH, height=HEIGHT - IN_H, no_resize=True, no_move=True):
    with dpg.child_window(tag="chat_logs", height=-1, autosize_x=True):
        with dpg.table(header_row=False):
            dpg.add_table_column(label="Left", init_width_or_weight=0.70)
            dpg.add_table_column(label="Right", init_width_or_weight=0.30)

            with dpg.table_row():
                with dpg.table_cell(tag="left_cell"):
                    pass
                with dpg.table_cell(tag="right_cell"):
                    pass

with dpg.window(no_title_bar=True, width=WIDTH, height=IN_H, pos=[0, HEIGHT - IN_H], no_resize=True, no_move=True):
    dpg.add_input_text(tag="msg_input", hint="Enter a message...", width=WIDTH - 100, on_enter=True, callback=add_message)
    dpg.add_button(label="Send", callback=add_message, width=80, height=19, pos=[WIDTH - 85, 8])



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()