#!/usr/bin/env python3

#############################################################################################################################################################################
# This script does the following:                                                                                                                                           #
#   1. Open rofi containing window names for all open i3 windows                                                                                                            #
#   2. Wait for the user to select a window in rofi                                                                                                                         #
#   3. Move the selected window to the current workspace                                                                                                                    #
#   4. Focus the moved window                                                                                                                                               #
#                                                                                                                                                                           #
# For the best experience it is recommended to run the script as rofi 'window-command' in window mode.                                                                      #
# With a configuration as suggested below, you can pull the selected window pressing Return and focus                                                                       #
# it using Shift+Return                                                                                                                                                     #
#                                                                                                                                                                           #
# Sample installation within i3:                                                                                                                                            #
#   bindsym $mod+p exec --no-startup-id "rofi -show window -modi window -window-command 'pull-window {window}' -kb-accept-alt 'Return' -kb-accept-entry 'Shift+Return'"     #
#############################################################################################################################################################################

import sys
import i3ipc

name_length = 45
class_length = 30
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
            workspace = node.workspace().name

            if workspace.startswith('__i3_scratch'):
                workspace = 'S'

            print(f"{workspace}".ljust(workspace_length), end="")
            print(f"{class_name}".ljust(class_length), end="")
            print(f"{node_name}".ljust(name_length), end="")
            print(f"{node.window}")


def move_to_current(window_id):
    '''
    Moves a window (identified by window_id) to the current workspace.
    '''
    focused = i3_tree.find_focused()
    workspace_id = focused.workspace().name
    i3.command(f"[id={window_id}] move to workspace {workspace_id}")
    i3.command(f"[id={window_id}] focus")


if len(sys.argv) == 1:
    print_windows()

else:
    selection = sys.argv[1]

    if selection.isnumeric():
        move_to_current(selection)

    window_id = selection[total_length:]

    if not window_id.isnumeric():
        raise ValueError(f"Window ID ({window_id}) is not numeric.")

    move_to_current(window_id)
