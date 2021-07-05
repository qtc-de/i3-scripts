#!/usr/bin/env python3

###############################################################################################
# This script does the following:                                                             #
#   1. Caches the currently focused workspace id                                              #
#   2. Registers an i3 event listener that looks out for the *Save as* window of flameshot    #
#   3. Starts flameshot as regulary                                                           #
#   4. Moves the *Save as* window of flameshot to the previously cached workspace             #
#                                                                                             #
# Sample installation within i3:                                                              #
#   bindsym $mod+Shift+s --release exec --no-startup-id i3-flameshot
###############################################################################################

import sys
import asyncio
import subprocess
from i3ipc import Event
from i3ipc.aio import Connection

current_workspace = 0


async def on_new_window(i3, e):
    '''
    Event that triggers during window creation. Checks whether the newly created window
    belongs to flameshot and moves it to the workspace, where flameshot was actually
    invoked.
    '''
    if e.container.name == "Save screenshot" and e.container.window_class == "flameshot":
        window_id = e.container.window
        await i3.command(f"[id={window_id}] move to workspace {current_workspace}")
        await i3.command(f"[id={window_id}] focus")
        i3.main_quit()


async def get_current_workspace(i3):
    '''
    Returns the id of the currently focused workspace.
    '''
    i3_tree = await i3.get_tree()
    focused = i3_tree.find_focused()
    return focused.workspace().name


async def consume():
    '''
    Caches the currently focused workspace id and registers an event listener for
    newly opened windows. Afterwards, it starts the regular flameshot utility and
    enters the event loop.
    
    As soon as the *Save As* window of flameshot appears, the window is moved to the 
    previously cached workspace.
    '''
    global current_workspace

    i3 = await Connection().connect()
    current_workspace = await get_current_workspace(i3)
    i3.on(Event.WINDOW_NEW, on_new_window)

    subprocess.call(["flameshot", "gui"])
    await asyncio.wait_for(i3.main(), timeout=30)


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())

finally:
    loop.close()
