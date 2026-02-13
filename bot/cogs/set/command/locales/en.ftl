# Translation for Set
Set-deco_helper = Main command to customize your user settings.
Set-deco_usage = Usage: {$prefix}set (subcommand) [arguments]
Set-deco_description = Main command to customize your user settings.


# Translation for Set Mention
Mention-on_off_wrong_option = {$args} its not a valid option, choose between "on" or "off"
Mention-mention_on = You will start receiving pings from the bot on commands again.
Mention-mention_off = Every time the bot says your nick it will place an invisible character to prevent ping.

Mention-deco_helper = Enable or disable bot mentions.
Mention-deco_usage = Usage: {$prefix}set mention <on/off>
Mention-deco_description = Allows you to enable or disable whether the bot will directly mention you when replying.

# Commands
Mention-cmd_on_prefix = Enable mentions:
Mention-cmd_off_prefix = Disable mentions:

# Translation for Set City
City-city_added = City added successfully.
City-city_removed = City removed successfully.

City-deco_helper = Set or remove your saved city.
City-deco_usage = Usage: {$prefix}set city (name or remove) [hidden:true]
City-deco_description = Saves a city name to your profile, optionally hidden from public view.

# Commands
City-cmd_set_prefix = Set a city:
City-cmd_hide_prefix = Set a city and hidden:
City-cmd_latlong_prefix = Set a location with lat and long and hidden:
City-cmd_remove_prefix = Remove city:

# Admonitions
City-adm_hide_title = Hide it
City-adm_hide_msg = Use the `hidden` flag to hide your city from messages.

# Translation for Set Nick
Nick-nick_too_large = Nick must be max 32 characters long not {$limit}.
Nick-nick_removed = Nick removed successfully.
Nick-nick_changed = Nick changed successfully.

Nick-deco_helper = Set or remove a custom nickname.
Nick-deco_usage = Usage: {$prefix}set nick <nickname or remove>
Nick-deco_description = Lets you define a nickname that the bot will use when addressing you.

# Commands
Nick-cmd_set_prefix = Set nickname:
Nick-cmd_remove_prefix = Remove nickname:

# Admonitions
Nick-adm_short_title = Keep it short!
Nick-adm_short_msg = Nick must be max 32 characters long.

# Translation for Set Color
Color-color_removed = Saved color removed successfully.
Color-color_changed = Saved color changed successfully.

Color-deco_helper = Save or remove a custom color.
Color-deco_usage = Usage: {$prefix}set color (#hex or remove)
Color-deco_description = Sets a custom hex color that may be used in future visualizations.

# Commands
Color-cmd_set_prefix = Set color:
Color-cmd_remove_prefix = Remove color:

# Translation for Set Reminder
Reminder-reminder_on = Reminder successfully turned on.
Reminder-reminder_off = Reminder successfully turned off.

Reminder-deco_helper = Enable or disable reminders.
Reminder-deco_usage = Usage: {$prefix}set reminder (on/off)
Reminder-deco_description = Toggles whether the system will send mark you in reminders form other people.

# Commands
Reminder-cmd_on_prefix = Enable reminders:
Reminder-cmd_off_prefix = Disable reminders:

# Translation for Set Banword
Banword-add_remove = Chose one of the valid options: add, remove or clean. Not {$args}.
Banword-who = How the hell did you make this happen? I'm reporting you now.
Banword-added = Banword(s) added. I will now censor any command that contains it.
Banword-removed = Banword(s) removed.
Banword-cleaned = I removed all the banwords words.
Banword-what = I didn't understand this option {$option}

Banword-deco_helper = Command used to add ban words that the bot cannot send in the chat.
Banword-deco_usage = To use: {$prefix}set banword (add|remove|clean) (words)
Banword-deco_description = Command used to add ban words that the bot cannot send in the chat.

# Mapping
Banword-map_add = add
Banword-map_remove = remove
Banword-map_clean = clean

# Translation for Set Enable/Disable
Enable-why = Why are you trying to enable/disable {$args}?
Enable-no_command = I don't have any command called {$args}.
Enable-command_already_enabled = The command {$args} is already activated.
Enable-command_enabled = The command {$args} was activated.
Enable-command_disabled = The command {$args} was disabled.
Enable-command_already_disabled = The command {$args} is already disabled.
Enable-options = If you want to enable/disable all, you can use enable/disable all.
Enable-all_enabled = All commands have been activated.
Enable-all_disabled = All commands have been disabled.

Enable-deco_helper = A command used to activate or deactivate other commands.
Enable-deco_usage = To use: {$prefix}set enable/disable (command name or all)
Enable-deco_description = A command used to activate or deactivate other commands.

# Translation for Set Prefix
Prefix-too_long = The prefix {$arg} is too long, please keep it shorter than {$size}.
Prefix-prefix_changed = Prefix changed to {$args}

Prefix-deco_helper = Command used to change the channel prefix, anything with 2 characters will work.
Prefix-deco_usage = To use: {$prefix}set prefix (anything)
Prefix-deco_description = Command used to change the channel prefix, anything with 2 characters will work.

# Translation for Set StartStop
StartStop-started = The bot was successfully turned on.
StartStop-already_on = The bot is already on.
StartStop-stopped = The bot was successfully turned off.
StartStop-already_off = The bot is already off.
StartStop-shrug = Don't know how you get here. Maybe a bug.

StartStop-deco_helper = Command used to turn the bot on or off in the chat.
StartStop-deco_usage = To use: {$prefix}set start(or on)/stop(or off)
StartStop-deco_description = Command used to turn the bot on or off in the chat.
