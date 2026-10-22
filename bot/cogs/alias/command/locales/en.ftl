## Table
Alias-Table-alias_table_headers = Alias Name, Description, Invokes, Arguments, Links to, Updated, Created
Alias-Table-alias_table_replaces = No description, No arguments, None
Alias-Table-alias_table_name = { $name } aliases
Alias-Table-alias_table_upload_error = Error while uploading alias for: { $name } Pls contact: { $dev }

## Alias
Alias-dont_have_alias = You don't have the "{ $name }" alias!
Alias-alias_invalid_name = Your alias name is not valid! Your alias should only contain letters, numbers and be 2-30 characters long.
Alias-user_has_no_alias = User { $name } has no registered aliases.
Alias-deco_helper = Command used to manage aliases.
Alias-deco_usage = To use: { $prefix }alias add|check|copy|describe|edit|link|remove|rename (options)

## Add
Alias-Add-error_no_name = You didn't send the alias name! Usage: { $prefix }alias add (name) (command) (…arguments)
Alias-Add-no_command_to_add = You didn't send a command! Usage: { $prefix }alias add (name) (command) (…arguments)
Alias-Add-alias_name_conflict = Cannot add alias "{ $name }" - you already have one! You can either "edit" its definition, "rename" it or "remove" it.
Alias-Add-alias_created = Your alias "{ $name }" has been created successfully.
Alias-Add-command_dont_exist = Cannot create alias! The command "{ $name }" does not exist.
Alias-Add-deco_helper = This subcommand is used to add an alias.
Alias-Add-deco_usage = How to use: { $prefix }alias add (name) (command) (…arguments)
Alias-Add-deco_description = This subcommand is used to add aliases.

# Add Examples
Alias-Add-cmd_ex1_prefix = ## How to create an alias:{"\n\n"}- The following example uses [pipe](pipe.md) to pass the response of one command to another.
Alias-Add-cmd_ex1_args = add cool_name choice 1234 123456 | count
Alias-Add-cmd_ex1_res = your alias "cool_name" has been successfully created.
Alias-Add-cmd_ex1_suffix = In the example above, we created an alias named `cool_name`. The alias will invoke the `choice` command with the arguments "1234" and "123456", and the result from `choice` will be sent to the `count` command.

Alias-Add-cmd_ex2_prefix = ## How to use the alias:
Alias-Add-cmd_ex2_args = { $prefix }{ $prefix }cool_name
Alias-Add-cmd_ex2_res = There are a total of 4 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
Alias-Add-cmd_ex2_suffix = To use the alias, just use `{ $prefix }{ $prefix }` followed by the alias name (`{ $prefix }` is the default bot prefix; if the chat prefix is different, just repeat it twice and then the alias name).

# Add Admonitions
Alias-Add-adm1_title = Restrictions for alias names!
Alias-Add-adm1_msg = - Must be between 2 and 30 characters long.{"\n"}- Can contain letters, numbers, dashes (-), underscores (_), and a wide range of Unicode characters (©), including emojis (🔥).
Alias-Add-adm2_title = Cooldown for created aliases!
Alias-Add-adm2_msg = When creating an alias, the alias cooldown will be the cooldown of the commands used in the alias. Therefore, if one command can be used 1x every 5 seconds and another 3x every 10 seconds, the alias cooldown will be 1x every 5 seconds.

## Check
Alias-Check-no_target_user = List of your aliases: { $names } | Detailed list: { $url }
Alias-Check-no_first_name = List of your aliases: { $names } | Detailed list: { $url }
Alias-Check-user_alias_list_error = Error while trying to upload alias list, try again shortly.
Alias-Check-user_alias_list = List of your aliases: { $names } | Detailed list: { $url }
Alias-Check-no_alias_found = Could not find { $alias_name } in { $user_name } aliases or any of your aliases!
Alias-Check-list_of_alias_of = List of { $mention } aliases: { $url }
Alias-Check-list_of_special_case =
    Special case!
    Your alias "{ $name }": { $url1 }
    List of { $name }'s aliases: { $url2 }
Alias-Check-alias_not_found = { $mention } don't have the "{ $alias }" alias!
Alias-Check-alias_deleted = { $alias } alias is a link to a different alias, but the original has been deleted.
Alias-Check-normal_message = { $name } || Invoke: { $invocation } || Link: { $url }
Alias-Check-appendix_message = This alias is a link to "{ $parent }" made by { $original }. The alias has the arguments: { $invocation } || Link: { $url }
Alias-Check-appendix = This alias is a link to "{ $name }" made by { $owner }.
Alias-Check-message = { $user } alias "{ $name }" have the arguments: { $arg1 } { $arg2 }

Alias-Check-deco_helper = This subcommand is used to check infos for an alias.
Alias-Check-deco_usage = How to use: { $prefix }alias check cool_name
Alias-Check-deco_description = This subcommand is used to check infos for an aliases.

# Check Examples
Alias-Check-cmd_ex1_prefix = ## How to check an alias:
Alias-Check-cmd_ex1_args = check cool_name
Alias-Check-cmd_ex1_res = User, the alias "cool_name" has the arguments: choice 1234 123456 | count || Link: (URL)

## Copy
Alias-Copy-alias_not_provided = No target alias provided!
Alias-Copy-target_alias_invalid_name = The copied alias's name is not valid and therefore can't be copied!
Alias-Copy-no_alias_found = I couldn't find { $alias } in user { $name }!
Alias-Copy-link_to_a_link = You cannot copy links to other aliases. Instead, use { $prefix }alias copy { $user } { $target }
Alias-Copy-copy_success = Alias "{ $name }" copied successfully.
Alias-Copy-copy_with_name_of = Alias "{ $target }" copied successfully. With the name "{ $name }".

Alias-Copy-deco_helper = This subcommand is used to copy an alias.
Alias-Copy-deco_usage = How to use: { $prefix }alias copy (user) (alias) (…arguments)
Alias-Copy-deco_description = This subcommand is used to copy an alias.

# Copy Examples
Alias-Copy-cmd_ex1_prefix = ## How to copy an alias:
Alias-Copy-cmd_ex1_args = copy <username> cool_name
Alias-Copy-cmd_ex1_res = User, alias "cool_name" copied successfully.
Alias-Copy-cmd_ex1_suffix = To copy an alias, you only need the username and the alias name.

## Describe
Alias-Describe-no_args_to_parse = You didn't provide a alias or description! Use: { $prefix }alias describe (name) (…description)
Alias-Describe-description_updated = The description of alias "{ $name }" has been updated successfully.
Alias-Describe-description_reverted = The description of alias "{ $name }" has been reset successfully.

Alias-Describe-deco_helper = This subcommand is used to check infos for an alias.
Alias-Describe-deco_usage = How to use: { $prefix }alias description cool_name (new description)
Alias-Describe-deco_description = This subcommand is used to check info for an aliases.

# Describe Examples
Alias-Describe-cmd_ex1_prefix = ## How to add a description to an alias:
Alias-Describe-cmd_ex1_args = description cool_name (new description)
Alias-Describe-cmd_ex1_res = User, the description for alias "cool_name" has been successfully updated.

## Edit
Alias-Edit-no_args_provided = No alias or command name provided!
Alias-Edit-edit_link = You cannot edit links to other aliases!
Alias-Edit-edit_success = Your alias "{ $name }" has been successfully edited.
Alias-Edit-command_dont_exist = Cannot edit alias! The command "{ $name }" does not exist.

Alias-Edit-deco_helper = This subcommand is used to edit the command and arguments for an alias.
Alias-Edit-deco_usage = How to use: { $prefix }alias edit (alias) (command) (…arguments)
Alias-Edit-deco_description = This subcommand is used to edit the command and arguments for an alias.

# Edit Examples
Alias-Edit-cmd_ex1_prefix = ## How to edit an alias:
Alias-Edit-cmd_ex1_args = edit cool_name count bla bla bla bla
Alias-Edit-cmd_ex1_res = Your alias "cool_name" has been successfully edited.

# Edit Admonitions
Alias-Edit-adm1_title = Linked alias.
Alias-Edit-adm1_msg = - Because linked alias are only a pointer to other user alias, editing then is impossible.

## Link
Alias-Link-link_no_args = You didn't provide a user or alias name! Use: { $prefix }alias link (user) (alias name)
Alias-Link-alias_name_already_exists = Cannot link a new alias - you already have an alias named: { $name }!
Alias-Link-user_dont_has_alias = The provided user does not have the alias "{ $name }"!
Alias-Link-link_to_with_invalid_name = The original alias has an invalid name "{ $name }"! Please provide a custom name.
Alias-Link-link_custom_name_invalid = The custom name "{ $name }" is not valid. Please provide a valid name.
Alias-Link-link_to_link = You tried to create a link from a linked alias (alias { $target_name } by { $user_name }), so I used the original as your template{ $alias_name }. When the original changes, yours will too.
Alias-Link-link_success = Alias successfully linked{ $name }. When the original changes, yours will too.
Alias-Link-link_name_string = , with a custom name of "{ $name }"

Alias-Link-deco_helper = This subcommand is used to create link for an alias.
Alias-Link-deco_usage = How to use: { $prefix }alias link (user) cool_name
Alias-Link-deco_description = This subcommand is used to create link for an alias.

# Link Examples
Alias-Link-cmd_ex1_prefix = ## How to link an alias:
Alias-Link-cmd_ex1_args = link (user) cool_name
Alias-Link-cmd_ex1_res = User, alias linked successfully. When the original changes, yours will also change.

Alias-Link-cmd_ex2_prefix = ## It is also possible to create a link and change the alias name.
Alias-Link-cmd_ex2_args = link (user) cool_name new_cool_name
Alias-Link-cmd_ex2_res = User, alias linked successfully, with a custom name "new_cool_name". When the original changes, yours will also change.

Alias-Link-cmd_ex3_prefix = ## And if it is a link to a link:
Alias-Link-cmd_ex3_args = link (user) cool_name
Alias-Link-cmd_ex3_res = User, you attempted to create a link from an already linked alias (alias cool_name by <user>), so I used the original as your model. When the original changes, yours will also change.

## Remove
Alias-Remove-no_alias_name_provided = No alias name provided!
Alias-Remove-alias_removed = Your alias "{ $name }" has been successfully removed.

Alias-Remove-deco_helper = This subcommand is used to delete an alias.
Alias-Remove-deco_usage = How to use: { $prefix }alias remove (alias)
Alias-Remove-deco_description = This subcommand is used to delete an alias.

# Remove Examples
Alias-Remove-cmd_ex1_prefix = ## To remove an alias:
Alias-Remove-cmd_ex1_args = remove cool_name
Alias-Remove-cmd_ex1_res = User, your alias "cool_name" has been successfully removed.
Alias-Remove-cmd_ex1_suffix = When deleting an alias, the links to this alias will continue to exist and function.

## Rename
Alias-Rename-no_name_provided = You must provide both the current alias name and the new one!
Alias-Rename-alias_already_exists = You already have the "{ $name }" alias!
Alias-Rename-alias_renamed = Your alias "{ $old }" has been successfully renamed to "{ $new }".

Alias-Rename-deco_helper = This subcommand is used to rename an alias.
Alias-Rename-deco_usage = How to use: { $prefix }alias rename cool_name new_cool_name
Alias-Rename-deco_description = This subcommand is used to rename an alias.

# Rename Examples
Alias-Rename-cmd_ex1_prefix = ## To rename an alias:
Alias-Rename-cmd_ex1_args = rename cool_name new_cool_name
Alias-Rename-cmd_ex1_res = User, your alias "cool_name" has been successfully renamed to "new_cool_name".

## Extras
Alias-Extras-deco_description = This section is about advanced alias usage.

# Extras Examples
Alias-Extras-cmd_ex1_prefix = ## First, let's create an alias:
Alias-Extras-cmd_ex1_args = add advanced_usage choice 1234 123456 | count {"{0}"}
Alias-Extras-cmd_ex1_res = User, your alias "advanced_usage" has been successfully created.

Alias-Extras-cmd_ex2_prefix = ## How to use this type of alias:
Alias-Extras-cmd_ex2_args = { $prefix }{ $prefix }advanced_usage text
Alias-Extras-cmd_ex2_res = There are a total of 10 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
Alias-Extras-cmd_ex2_suffix =
    The normal response of the command would be: `There are a total of 4 characters. etc` or `There are a total of 6 characters. etc`, as `choice` would select between `1234` or `123456`, and then count would return the number of characters.
    {"\n\n"}But, due to the addition of `{"{0}"}` after count, it will take the content of what was sent when invoking the alias and replace `{"{0}"}`.
    {"\n\n"}So the command passed to count it would be something like: `text 1234`

Alias-Extras-cmd_ex3_prefix = ## An example showing all would be:
Alias-Extras-cmd_ex3_args = add advanced_usage2 choice 1234 123456 | count {"{0}"} {"{channel}"} {"{output}"} {"{user}"} {"{1+}"}
Alias-Extras-cmd_ex3_res = User, your alias "advanced_usage2" has been successfully created.

# Extras Admonitions
Alias-Extras-adm1_title = The bot's step-by-step process will be:
Alias-Extras-adm1_msg =
    - Replace `{"{0}"}` with `something_here`.
    - Replace `{"{1+}"}` with `and in the end`.
    - Replace `{"{channel}"}` with the channel to which the message was sent, for example, `gorenmu`.
    - Replace `{"{user}"}` with your username, for example, `xXNickOriginalXx`.
    - The full command would be `choice 1234 123456 | count something_here gorenmu {"{output}"} xXNickOriginalXx` which would be processed by the pipe handler.

Alias-Extras-adm2_title = The pipe handle, will do:
Alias-Extras-adm2_msg =
    - Process the first part: `choice 1234 123456` (as an example, let's say choice selected `1234`).
    - Process the second part: `count something_here gorenmu {"{output}"} xXNickOriginalXx and in the end`; when processing the second part, it will replace `{"{output}"}` with `1234`.
    - Then, the arguments that will be sent to count will be `something_here gorenmu 1234 xXNickOriginalXx and in the end.`
    - And the response will be `There are a total of 50 characters. Among them, 1 is punctuation, 4 are uppercase letters, and 0 are special characters.`

Alias-Extras-adm3_title = Other options when creating the alias are:
Alias-Extras-adm3_msg =
    - `{"{output}"}`: it will place the output of the last command at the `{"{output}"}` position.
    - `{"{channel}"}`: it will replace with the name of the current channel.
    - `{"{user}"}`: it will replace with your Twitch username.
    - `{"{0}"}`, `{"{1}"}`, `{"{2}"}` etc., you can also use `{"{3+}"}`, which will take all text sent when invoking the alias and replace.

## Templates
# Partes da documentação
Alias-Template-part1 =
    # { $command_title }
    {"\n\n"}## This command can be used { $rate } times in succession, with a cooldown of { $per } per { $cooldown_type }.{"\n\n"}
Alias-Template-part2 = { $description }{"\n\n"}{ $aliases }{"\n\n"}
Alias-Template-part3 = ## The way to use this command is:{"\n\n"}

# Templates específicos
Alias-Template-alias_template =
    ## All the alias available for { $command_title } are:
        - { $aliases }{"\n\n"}
Alias-Template-command_template =
    ```text
        user: { $prefix }{ $command_name } { $args }

        bot: User, { $response }
    ```{"\n"}
Alias-Template-admonition_template =
    !!! { $type } "{ $title }"

            { $message }{"\n\n"}

# Tipos de Bucket (Cooldown)
Alias-Template-bucket_type = { $type ->
    [channel] all user per channel
    [member] user per channel
    [user] user independent of channel
    [subscriber] subscriber
    [mod] moderation
    *[default] user
}
