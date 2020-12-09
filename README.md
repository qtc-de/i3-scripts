### Rofi Scripts

----

Some utility scripts for [rofi](https://github.com/davatorium/rofi). Custom scripts can
be used by the following syntax:

```console
$ rofi -show example -modi example:./.local/bin/example-script
```

Within *i3*, you most likely want to assign a corresponding key binding:

```i3
bindsym $mod+e exec --no-startup-id "rofi -show example -modi example:~/.local/bin/example-script"
```


### Scripts

-----

The following scripts are currently available:

#### i3 Pull

This script does the following:

1. Open *rofi* containing window names for all open i3 windows
2. Wait for the user to select a window in *rofi*
3. Move the selected window to the current workspace
4. Focus the moved window
