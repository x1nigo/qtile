# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import psutil

mod = "mod4"
myBrowser = "firefox"
myFileManager = "lfrun"
terminal = "st"
audiomixer = "pulsemixer"
emailClient = "neomutt"
rssFeed = "newsboat"
musicPlayer = "ncmpcpp"

colors = [
    ["#161818ef", "#161818ff"], # bg
    ["#0a0f14", "#0a0f14"],
    ["#eeeeee", "#eeeeee"],
    ["#500000", "#500000"],
    ["#c3e88d", "#c3e88d"],
    ["#ffcb6b", "#ffcb6b"],
    ["#82aaff", "#82aaff"],
    ["#a9b1f6", "#a9b1f6"],
    ["#444460", "#444460"],
    ]

keys = [
    # Some basic commands.
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("floater"), desc="Launch floating terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod, "shift"], "Space", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn("dmenu_run -l 30 -g 5 -z 800"), desc="Spawn dmenu and open a program"),
    Key([mod], "x", lazy.spawn("setbg -s"), desc="Set the background"),
    Key([mod], "grave", lazy.spawn("dmenumoji"), desc="Copy an emoji to the clipboard"),
    Key([mod], "BackSpace", lazy.spawn("sysmenu"), desc="Select a system action"),
    Key([mod], "w", lazy.spawn(myBrowser), desc="Load up the browser"),
    Key([mod], "Insert", lazy.spawn("inserter"), desc="Insert a bookmark"),
    Key([mod], "b", lazy.spawn("bookmarker"), desc="Append a bookmark"),
    Key([mod], "p", lazy.spawn("texfind"), desc="Find and display PDF files"),
    Key([mod], "r", lazy.spawn("{} -e {}" .format(terminal, myFileManager)), desc="Launch the file browser"),
    Key([mod], "apostrophe", lazy.spawn(terminal + " -f monospace:size=16 -e bc -lq"), desc="Open a terminal calculator"),
    Key([mod], "e", lazy.spawn(terminal + " -e " + emailClient), desc="Look up your email"),
    Key([mod], "n", lazy.spawn(terminal + " -e " + rssFeed), desc="Read the news"),
    Key([mod], "m", lazy.spawn(terminal + " -e " + musicPlayer), desc="Play music"),

    # Function keys
    Key([mod], "F1", lazy.spawn("readme"), desc="Navigate your way around the system"),
    Key([mod], "F2", lazy.spawn("fontwizard"), desc="Change system fonts"),
    Key([mod], "F3", lazy.spawn("{} -e {}" .format(terminal, audiomixer)), desc="Open audio controls"),
    Key([mod], "F4", lazy.spawn("selectdisplay"), desc="Configure display settings"),
    Key([mod], "F5", lazy.spawn(terminal + " -e " + "nmtui"), desc="Connect to the internet"),
    Key([mod], "F6", lazy.spawn("recorder"), desc="Record your screen and/or webcam"),
    Key([mod], "F9", lazy.spawn("mounter"), desc="Mount USB drives and/or Android phones"),
    Key([mod], "F10", lazy.spawn("unmounter"), desc="Unmount USB drives and/or Android phones"),
    Key([mod], "F11", lazy.spawn("webcam"), desc="Unmount USB drives and/or Android phones"),
    Key([mod], "F12", lazy.reload_config(), desc="Reload the config"),

    # Multimedia Controls
    # Volume + Mic
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"), desc="Raise the volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), desc="Lower the volume"),
    Key(["shift"], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SOURCE@ 5%+"), desc="Raise the mic"),
    Key(["shift"], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SOURCE@ 5%-"), desc="Lower the mic"),

    # Mute
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), desc="Mute the volume"),
    Key([], "XF86AudioMicMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), desc="Mute the mic"),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5"), desc="Increase the screen brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5"), desc="Decrease the screen brightness"),

    # Alternative Multimedia Controls
    Key([mod], "equal", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"), desc="Raise the volume"),
    Key([mod], "minus", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), desc="Lower the volume"),
    Key([mod, "shift"], "period", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SOURCE@ 5%+"), desc="Raise the mic"),
    Key([mod, "shift"], "comma", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SOURCE@ 5%-"), desc="Lower the mic"),
    Key([mod, "shift"], "equal", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), desc="Mute the volume"),
    Key([mod, "shift"], "slash", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), desc="Mute the mic"),
    Key([mod], "bracketright", lazy.spawn("xbacklight -inc 5"), desc="Increase the screen brightness"),
    Key([mod], "bracketleft", lazy.spawn("xbacklight -dec 5"), desc="Decrease the screen brightness"),

    # Window Management
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes

    Key([mod, "control"], "t", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

my_layout = {
        "border_width": 2,
        "margin": 8,
        "border_focus": colors[7],
        "border_normal": colors[0],
        "ratio": 0.5,
        }

layouts = [
    layout.MonadTall(**my_layout),
    layout.Max(),
    layout.MonadWide(**my_layout),
    layout.Columns(**my_layout),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = "BlexMono Nerd Font Mono",
    fontsize = 12,
    padding = 5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(),
                widget.TextBox(
                    "",
                    fontsize = 30,
                    foreground = colors[8],
                    mouse_callbacks = {"Button1": lazy.spawn(terminal)},
                    ),
                widget.TextBox(),
                widget.GroupBox(
                    highlight_method = "line",
                    active = colors[7],
                    inactive = colors[2],
                    borderwidth = 2,
                    highlight_color = colors[1],
                    this_current_screen_border = colors[7],
                    disable_drag = True,
                    ),
                widget.TextBox(" | "),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
                widget.TextBox(" | "),
                widget.WindowName(
                    foreground = colors[8],
                    ),
                widget.TextBox(
                    "󰄫",
                    fontsize = 22,
                    foreground = colors[7],
                    ),
                widget.CPU(),
                widget.TextBox(),
                widget.TextBox(
                    "󰄧",
                    fontsize = 22,
                    foreground = colors[7],
                    ),
                widget.Memory(),
                widget.TextBox(),
                widget.TextBox(
                    "󰠓",
                    fontsize = 22,
                    foreground = colors[7],
                   ),
                widget.CryptoTicker(
                    crypto = "BTC",
                    api = "coinbase",
                    format = "{symbol}{amount:.2f}",
                    ),
                widget.TextBox(),
                widget.TextBox(
                    "󰃠",
                    fontsize = 22,
                    foreground = colors[7],
                    ),
                widget.Backlight(
                    backlight_name = "intel_backlight",
                    ),
                widget.TextBox(),
                widget.TextBox(
                    "󰒍",
                    fontsize = 22,
                    foreground = colors[7],
                    ),
                widget.Net(
                    format = "{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}"
                    ),
                widget.TextBox(),
                widget.TextBox(
                    "󰋔",
                    fontsize = 22,
                    foreground = colors[7],
                    ),
                widget.Battery(
                    battery = 0,
                    charge_char = "^",
                    discharge_char = "v",
                    empty_char = "x",
                    format = "{char}: {percent:2.0%}"
                    ),
                widget.TextBox(),
                widget.TextBox(
                        "",
                        fontsize = 22,
                        foreground = colors[7],
                        ),
                widget.Clock(format = "%Y %b %d (%a) %I:%M%p"),
                widget.TextBox(),
            ],
            20,
            background = colors[0],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
        float_rules = [
            Match(title = "termfloat"),
            ],
        border_width = 2,
        border_focus = colors[3],
        border_normal = colors[8],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# Enable window swallowing (?)
@hook.subscribe.client_new
def _swallow(window):
    pid = window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
