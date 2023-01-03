#!/usr/bin/env python3

###############################################################################################
# This script does the following:                                                             #
#   1. Open rofi containing window names for all open i3 windows                              #
#   2. Wait for the user to select a window in rofi                                           #
#   3. Swaps the currently focused window with the selected one                               #
#                                                                                             #
# Sample installation within i3:                                                              #
#   bindsym $mod+p exec --no-startup-id "rofi -show swapw -modi swapw:~/.local/bin/swapw.py"  #
###############################################################################################

import sys
import i3ipc

name_length = 55
class_length = 20
workspace_length = 5
total_length = name_length + class_length + workspace_length

i3 = i3ipc.Connection()
i3_tree = i3.get_tree()


def truncate(string, length):
    '''
    Truncates the specified string at the specified length.
    '''
    if len(string) <= length:
        return string

    return string[0:length - 3] + "..."


def print_windows():
    '''
    Print information for each open window based on i3_tree.
    '''
    for node in i3_tree:
        if node.window and node.parent.type != 'dockarea':

            node_name = truncate(node.name, name_length - 5)
            class_name = truncate(node.window_class, class_length - 5)
            workspace_name = node.workspace().name

            if workspace_name == '__i3_scratch':
                workspace_name = 'S'

            print(f"{workspace_name}".ljust(workspace_length), end="")
            print(f"{class_name}".ljust(class_length), end="")
            print(f"{node_name}".ljust(name_length), end="")
            print(f"{node.window}")


def swap_window(window_id):
    '''
    Swaps the currently focused window with the window identified by window_id.
    '''
    i3.command(f"swap container with id {window_id}")


if len(sys.argv) == 1:
    print_windows()

else:
    selection = sys.argv[1]
    window_id = selection[total_length:]

    if not window_id.isnumeric():
        raise ValueError(f"Window ID ({window_id}) is not numeric.")

    swap_window(window_id)
