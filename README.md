### i3 Scripts

----

Some utility scripts for [i3](https://i3wm.org/). Detailed installation instruction is contained
within each script. [rofi](https://github.com/davatorium/rofi) based scripts can be used by the following syntax:

```console
$ rofi -show example -modi example:~/.local/bin/example-script
```

Within *i3*, you most likely want to assign a corresponding key binding:

```i3
bindsym $mod+e exec --no-startup-id "rofi -show example -modi example:~/.local/bin/example-script"
```

### Requirements

----

* All scripts rely on the [i3ipc](https://pypi.org/project/i3ipc/) python package
* Some scripts rely on [rofi](https://github.com/davatorium/rofi)
* Some scripts rely on [flameshot](https://github.com/flameshot-org/flameshot)


### Scripts

----

The following scripts are currently available:

#### pull-window.py

1. Opens *rofi* containing window names for all open i3 windows
2. Wait for the user to select a window in *rofi*
3. Move the selected window to the current workspace
4. Focus the moved window


#### swap-workspace.py

1. Opens *rofi* containing a list of all available workspaces
2. Wait for the user to select a workspace in *rofi*
3. Swap all windows from the current workspace with all windows
   of the selected one


#### swap-window.py

1. Opens *rofi* containing window names for all open i3 windows
2. Wait for the user to select a window in *rofi*
3. Swaps the currently focused window with the selected one


#### i3-flameshot.py

1. Starts flameshot as usual
2. After taking the screenshot, additional windows (e.g. save menu)
   is displayed on the same workspace where you invoked the script
   from.
