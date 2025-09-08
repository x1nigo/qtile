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

import os

import libqtile.resources
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "st" # guess_terminal()
browser = "zen-browser" # librewolf, firefox, etc.
filemanager = "lfup"
volumecontrols = "pulsemixer"

@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'monadtall':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'monadtall'

keys = [

    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "Return", lazy.spawn(terminal), lazy.window.toggle_floating()), # Doesn't really work as I need it to.
    Key([mod], "w", lazy.spawn(browser)),
    Key([mod], "r", lazy.spawn("{} -e {}" .format(terminal, filemanager))),
    Key([mod], "d", lazy.spawn("dmenu_run")),
    Key([mod], "b", lazy.spawn("bookmarker")),
    Key([mod], "v", lazy.spawn("watchvid")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "x", lazy.spawn("setbg -d")),
    Key([mod, "shift"], "x", lazy.spawn("setbg -x")),
    Key([mod, "shift"], "Space", lazy.window.toggle_floating()),
    Key([mod], "apostrophe", lazy.spawn(terminal + " -t termfloat -f monospace:size=16 -g 50x20 -e bc -lq")),
    Key([mod], "Insert", lazy.spawn("inserter")),
    Key([mod], "grave", lazy.spawn("dmenumoji")),
    Key([mod], "BackSpace", lazy.spawn("systemmenu")),

    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-")),

    Key([mod], "F1", lazy.spawn("readme")),
    Key([mod], "F2", lazy.spawn("fontwizard")),
    Key([mod], "F3", lazy.spawn("{} -e {}" .format(terminal, volumecontrols))),
    Key([mod], "F4", lazy.spawn("selectdisplay")),
    Key([mod], "F12", lazy.reload_config()),
    Key([], "Print", lazy.spawn("printscreen")),

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
#     Key(
#         [mod, "shift"],
#         "Return",
#         lazy.layout.toggle_split(),
#         desc="Toggle between split and unsplit sides of stack",
#     ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod], "space", lazy.window.move_to_top(), desc="Move window to top"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
# for vt in range(1, 8):
#     keys.append(
#         Key(
#             ["control", "mod1"],
#             f"f{vt}",
#             lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
#             desc=f"Switch to VT{vt}",
#         )
#     )

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

my_layout = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "#870000",
    "border_normal": "#282828",
    }

separator_values = {
    "size_percent": 50,
    "foreground": "#373737",
    }

layouts = [
    layout.MonadTall(**my_layout),
    layout.Max(),
    # layout.Columns(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(**my_layout)

widget_defaults = dict(
    font="monospace",
    foreground="#ebdbb2",
    fontsize=13,
    padding=4,
)
extension_defaults = widget_defaults.copy()

# logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(filename = "~/.config/qtile/python.png", margin = 2),
                widget.GroupBox(
                    highlight_method = "line", # block, text, etc.
                    active = "#ebdbb2",
                    inactive = "#373737",
                    borderwidth = 2,
                    highlight_color = ["#121212", "#1d2021"],
                    block_highlight_text_color = "#ebdbb2",
                    this_current_screen_border = "#dc2800",
                    ),
                widget.Sep(**separator_values),
                widget.CurrentLayout(),
                widget.Sep(**separator_values),
                widget.LaunchBar(
                    progs = [("🦊", "zen-browser", "Browser"),
                             ("🎯", "st", "The simple terminal"),
                             ("🖌️", "gimp", "Gimp"),
                             ("📜", "libreoffice", "Libre Office"),
                             ("📡", "st -e nmtui", "Network Manager"),
                             ],
                    ),
                widget.Sep(**separator_values),
                widget.WindowName(
                    foreground = "#a7d7f7",
                    max_chars = 40,
                    ),
                widget.Spacer(),
                widget.MemoryGraph(),
                widget.Sep(**separator_values),
                widget.Volume(
                    mute_format = "🔇",
                    unmute_format = "📢 Vol: {volume}%",
                    ),
                widget.Sep(**separator_values),
                widget.Battery(
                    fmt = "{}",
                    discharge_char = "🔋",
                    empty_char = "🪫",
                    charge_char = "🔌",
                    full_char = "⚡",
                    full_short_text = "",
                    update_interval = 10,
                    notify_below = 20,
                    notification_timeout = 0,
                    ),
                widget.Sep(**separator_values),
                widget.Systray(),
                widget.Clock(format="%d %B %Y (%A) 🕗 %I:%M%p"),
            ],
            26, # Bar height
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background = "#1d2021",
            # margin = [8, 8, 0, 8],
        ),
#         wallpaper=logo,
#         wallpaper_mode="center",
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
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
