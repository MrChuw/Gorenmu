# Translation for Set
Set-deco_helper = Main command to customize your user settings.
Set-deco_usage = Usage: {$prefix}set (subcommand) [arguments]
Set-deco_description = Main command to customize your user settings.


# Translation for Set Mention
Set-Mention-on_off_wrong_option = {$args} its not a valid option, choose between "on" or "off"
Set-Mention-mention_on = You will start receiving pings from the bot on commands again.
Set-Mention-mention_off = Every time the bot says your nick it will place an invisible character to prevent ping.

Set-Mention-deco_helper = Enable or disable bot mentions.
Set-Mention-deco_usage = Usage: {$prefix}set mention <on/off>
Set-Mention-deco_description = Allows you to enable or disable whether the bot will directly mention you when replying.

# Commands
Set-Mention-cmd_on_prefix = Enable mentions:
Set-Mention-cmd_off_prefix = Disable mentions:

# Translation for Set City
Set-City-city_added = City added successfully.
Set-City-city_removed = City removed successfully.

Set-City-deco_helper = Set or remove your saved city.
Set-City-deco_usage = Usage: {$prefix}set city (name or remove) [hidden:true]
Set-City-deco_description = Saves a city name to your profile, optionally hidden from public view.

# Commands
Set-City-cmd_set_prefix = Set a city:
Set-City-cmd_hide_prefix = Set a city and hidden:
Set-City-cmd_latlong_prefix = Set a location with lat and long and hidden:
Set-City-cmd_remove_prefix = Remove city:

# Admonitions
Set-City-adm_hide_title = Hide it
Set-City-adm_hide_msg = Use the `hidden` flag to hide your city from messages.

# Translation for Set Nick
Set-Nick-nick_too_large = Nick must be max 32 characters long not {$limit}.
Set-Nick-nick_removed = Nick removed successfully.
Set-Nick-nick_changed = Nick changed successfully.

Set-Nick-deco_helper = Set or remove a custom nickname.
Set-Nick-deco_usage = Usage: {$prefix}set nick <nickname or remove>
Set-Nick-deco_description = Lets you define a nickname that the bot will use when addressing you.

# Commands
Set-Nick-cmd_set_prefix = Set nickname:
Set-Nick-cmd_remove_prefix = Remove nickname:

# Admonitions
Set-Nick-adm_short_title = Keep it short!
Set-Nick-adm_short_msg = Nick must be max 32 characters long.

# Translation for Set Color
Set-Color-color_removed = Saved color removed successfully.
Set-Color-color_changed = Saved color changed successfully.

Set-Color-deco_helper = Save or remove a custom color.
Set-Color-deco_usage = Usage: {$prefix}set color (#hex or remove)
Set-Color-deco_description = Sets a custom hex color that may be used in future visualizations.

# Commands
Set-Color-cmd_set_prefix = Set color:
Set-Color-cmd_remove_prefix = Remove color:

# Translation for Set Reminder
Set-Reminder-reminder_on = Reminder successfully turned on.
Set-Reminder-reminder_off = Reminder successfully turned off.

Set-Reminder-deco_helper = Enable or disable reminders.
Set-Reminder-deco_usage = Usage: {$prefix}set reminder (on/off)
Set-Reminder-deco_description = Toggles whether the system will send mark you in reminders form other people.

# Commands
Set-Reminder-cmd_on_prefix = Enable reminders:
Set-Reminder-cmd_off_prefix = Disable reminders:

# Translation for Set Banword
Set-Banword-add_remove = Chose one of the valid options: add, remove or clean. Not {$args}.
Set-Banword-who = How the hell did you make this happen? I'm reporting you now.
Set-Banword-added = Banword(s) added. I will now censor any command that contains it.
Set-Banword-removed = Banword(s) removed.
Set-Banword-cleaned = I removed all the banwords words.
Set-Banword-what = I didn't understand this option {$option}

Set-Banword-deco_helper = Command used to add ban words that the bot cannot send in the chat.
Set-Banword-deco_usage = To use: {$prefix}set banword (add|remove|clean) (words)
Set-Banword-deco_description = Command used to add ban words that the bot cannot send in the chat.

# Mapping
Set-Banword-map_add = add
Set-Banword-map_remove = remove
Set-Banword-map_clean = clean

# Translation for Set Enable/Disable
Set-Enable-why = Why are you trying to enable/disable {$args}?
Set-Enable-no_command = I don't have any command called {$args}.
Set-Enable-command_already_enabled = The command {$args} is already activated.
Set-Enable-command_enabled = The command {$args} was activated.
Set-Enable-command_disabled = The command {$args} was disabled.
Set-Enable-command_already_disabled = The command {$args} is already disabled.
Set-Enable-options = If you want to enable/disable all, you can use enable/disable all.
Set-Enable-all_enabled = All commands have been activated.
Set-Enable-all_disabled = All commands have been disabled.

Set-Enable-deco_helper = A command used to activate or deactivate other commands.
Set-Enable-deco_usage = To use: {$prefix}set enable/disable (command name or all)
Set-Enable-deco_description = A command used to activate or deactivate other commands.

# Translation for Set Prefix
Set-Prefix-too_long = The prefix {$arg} is too long, please keep it shorter than {$size}.
Set-Prefix-prefix_changed = Prefix changed to {$args}

Set-Prefix-deco_helper = Command used to change the channel prefix, anything with 2 characters will work.
Set-Prefix-deco_usage = To use: {$prefix}set prefix (anything)
Set-Prefix-deco_description = Command used to change the channel prefix, anything with 2 characters will work.

# Translation for Set StartStop
Set-StartStop-started = The bot was successfully turned on.
Set-StartStop-already_on = The bot is already on.
Set-StartStop-stopped = The bot was successfully turned off.
Set-StartStop-already_off = The bot is already off.
Set-StartStop-shrug = Don't know how you get here. Maybe a bug.

Set-StartStop-deco_helper = Command used to turn the bot on or off in the chat.
Set-StartStop-deco_usage = To use: {$prefix}set start(or on)/stop(or off)
Set-StartStop-deco_description = Command used to turn the bot on or off in the chat.
