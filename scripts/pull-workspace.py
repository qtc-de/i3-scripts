#!/usr/bin/env python3

###############################################################################################
# This script does the following                                                              #
#   1. Open rofi containing all available workspace numbers                                   #
#   2. Wait for the user to select a workspace in rofi                                        #
#   3. Move the selected workspace to the current output and focus it                         #
#                                                                                             #
# Sample installation within i3:                                                              #
#   bindsym $mod+p exec --no-startup-id "rofi -show pullw -modi pullw:~/.local/bin/pullw.py"  #
###############################################################################################

import sys
import i3ipc

i3 = i3ipc.Connection()
i3_tree = i3.get_tree()

focused = i3_tree.find_focused()
current = focused.workspace().name


def print_workspaces():
    '''
    Print information for each available workspace within the i3_tree.
    '''
    for workspace in sorted(i3_tree.workspaces(), key=lambda x: int(x.name)):

        if workspace.name == current:
            continue

        print(f'Workspace: {workspace.name}')


def pull_workspace(workspace_name):
    '''
    Move the workspace identified by workspace_name to the current output.
    '''
    outputs = i3.get_outputs()

    for output in outputs:
        if output.current_workspace == current:

            i3.command(f"[workspace={workspace_name}] move workspace to output {output.name}")
            i3.command(f"[workspace={workspace_name}] focus")
            break


if len(sys.argv) == 1:
    print_workspaces()

else:
    selection = sys.argv[1]
    workspace_name = selection.split()[-1]

    if not workspace_name.isnumeric():
        raise ValueError(f"Workspace Name ({workspace_name}) is not numeric.")

    pull_workspace(workspace_name)
