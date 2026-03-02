import gi
import os
import webview

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')

from gi.repository import Gtk 

def startScreen(title, file):
    abs_path = os.path.abspath(file)
    file_path = 'file://' + abs_path

    webview.create_window(title, file_path)
    webview.start()
