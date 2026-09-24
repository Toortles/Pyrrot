import dearpygui.dearpygui as dpg
from network import NetworkManager

net = NetworkManager()

dpg.create_context()
dpg.create_viewport(title="Pyrrot", width=1280, height=800, resizable=False)

with dpg.window(label="Test"):
    dpg.add_text("Hello Window!")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()