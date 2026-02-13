## Table
Table-alias_table_headers = Alias Name, Description, Invokes, Arguments, Links to, Updated, Created
Table-alias_table_replaces = No description, No arguments, None
Table-alias_table_name = { $name } aliases

## Alias
Alias-dont_have_alias = You don't have the "{ $name }" alias!
Alias-alias_invalid_name = Your alias name is not valid! Your alias should only contain letters, numbers and be 2-30 characters long.
Alias-user_has_no_alias = User { $name } has no registered aliases.
Alias-deco_helper = Command used to manage aliases.
Alias-deco_usage = To use: { $prefix }alias add|check|copy|describe|edit|link|remove|rename (options)

## Add
Add-no_command_to_add = You didn't send a command! Usage: { $prefix }alias add (name) (command) (…arguments)
Add-alias_name_conflict = Cannot add alias "{ $name }" - you already have one! You can either "edit" its definition, "rename" it or "remove" it.
Add-alias_created = Your alias "{ $name }" has been created successfully.
Add-command_dont_exist = Cannot create alias! The command "{ $name }" does not exist.
Add-deco_helper = This subcommand is used to add an alias.
Add-deco_usage = How to use: { $prefix }alias add (name) (command) (…arguments)
Add-deco_description = This subcommand is used to add aliases.

# Add Examples
Add-cmd_ex1_prefix = ## How to create an alias:{"\n\n"}- The following example uses [pipe](pipe.md) to pass the response of one command to another.
Add-cmd_ex1_args = add cool_name choice 1234 123456 | count
Add-cmd_ex1_res = your alias "cool_name" has been successfully created.
Add-cmd_ex1_suffix = In the example above, we created an alias named `cool_name`. The alias will invoke the `choice` command with the arguments "1234" and "123456", and the result from `choice` will be sent to the `count` command.

Add-cmd_ex2_prefix = ## How to use the alias:
Add-cmd_ex2_args = { $prefix }{ $prefix }cool_name
Add-cmd_ex2_res = There are a total of 4 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
Add-cmd_ex2_suffix = To use the alias, just use `{ $prefix }{ $prefix }` followed by the alias name (`{ $prefix }` is the default bot prefix; if the chat prefix is different, just repeat it twice and then the alias name).

# Add Admonitions
Add-adm1_title = Restrictions for alias names!
Add-adm1_msg = - Must be between 2 and 30 characters long.{"\n"}- Can contain letters, numbers, dashes (-), underscores (_), and a wide range of Unicode characters (©), including emojis (🔥).
Add-adm2_title = Cooldown for created aliases!
Add-adm2_msg = When creating an alias, the alias cooldown will be the cooldown of the commands used in the alias. Therefore, if one command can be used 1x every 5 seconds and another 3x every 10 seconds, the alias cooldown will be 1x every 5 seconds.

## Check
Check-user_alias_list = List of your aliases: { $names } | Detailed list: { $url }
Check-no_alias_found = Could not find { $alias_name } in { $user_name } aliases or any of your aliases!
Check-list_of_alias_of = List of { $mention } aliases: { $url }
Check-list_of_special_case =
    Special case!
    Your alias "{ $name }": { $url1 }
    List of { $name }'s aliases: { $url2 }
Check-alias_not_found = { $mention } don't have the "{ $alias }" alias!
Check-alias_deleted = { $alias } alias is a link to a different alias, but the original has been deleted.
Check-normal_message = { $name } || Invoke: { $invocation } || Link: { $url }
Check-appendix_message = This alias is a link to "{ $parent }" made by { $original }. The alias has the arguments: { $invocation } || Link: { $url }
Check-appendix = This alias is a link to "{ $name }" made by { $owner }.
Check-message = { $user } alias "{ $name }" have the arguments: { $arg1 } { $arg2 }

Check-deco_helper = This subcommand is used to check infos for an alias.
Check-deco_usage = How to use: { $prefix }alias check cool_name
Check-deco_description = This subcommand is used to check infos for an aliases.

# Check Examples
Check-cmd_ex1_prefix = ## How to check an alias:
Check-cmd_ex1_args = check cool_name
Check-cmd_ex1_res = User, the alias "cool_name" has the arguments: choice 1234 123456 | count || Link: (URL)

## Copy
Copy-alias_not_provided = No target alias provided!
Copy-target_alias_invalid_name = The copied alias's name is not valid and therefore can't be copied!
Copy-no_alias_found = I couldn't find { $alias } in user { $name }!
Copy-link_to_a_link = You cannot copy links to other aliases. Instead, use { $prefix }alias copy { $user } { $target }
Copy-copy_success = Alias "{ $name }" copied successfully.
Copy-copy_with_name_of = Alias "{ $target }" copied successfully. With the name "{ $name }".

Copy-deco_helper = This subcommand is used to copy an alias.
Copy-deco_usage = How to use: { $prefix }alias copy (user) (alias) (…arguments)
Copy-deco_description = This subcommand is used to copy an alias.

# Copy Examples
Copy-cmd_ex1_prefix = ## How to copy an alias:
Copy-cmd_ex1_args = copy <username> cool_name
Copy-cmd_ex1_res = User, alias "cool_name" copied successfully.
Copy-cmd_ex1_suffix = To copy an alias, you only need the username and the alias name.

## Describe
Describe-no_args_to_parse = You didn't provide a alias or description! Use: { $prefix }alias describe (name) (…description)
Describe-description_updated = The description of alias "{ $name }" has been updated successfully.
Describe-description_reverted = The description of alias "{ $name }" has been reset successfully.

Describe-deco_helper = This subcommand is used to check infos for an alias.
Describe-deco_usage = How to use: { $prefix }alias description cool_name (new description)
Describe-deco_description = This subcommand is used to check info for an aliases.

# Describe Examples
Describe-cmd_ex1_prefix = ## How to add a description to an alias:
Describe-cmd_ex1_args = description cool_name (new description)
Describe-cmd_ex1_res = User, the description for alias "cool_name" has been successfully updated.

## Edit
Edit-no_args_provided = No alias or command name provided!
Edit-edit_link = You cannot edit links to other aliases!
Edit-edit_success = Your alias "{ $name }" has been successfully edited.
Edit-command_dont_exist = Cannot edit alias! The command "{ $name }" does not exist.

Edit-deco_helper = This subcommand is used to edit the command and arguments for an alias.
Edit-deco_usage = How to use: { $prefix }alias edit (alias) (command) (…arguments)
Edit-deco_description = This subcommand is used to edit the command and arguments for an alias.

# Edit Examples
Edit-cmd_ex1_prefix = ## How to edit an alias:
Edit-cmd_ex1_args = edit cool_name count bla bla bla bla
Edit-cmd_ex1_res = Your alias "cool_name" has been successfully edited.

# Edit Admonitions
Edit-adm1_title = Linked alias.
Edit-adm1_msg = - Because linked alias are only a pointer to other user alias, editing then is impossible.

## Link
Link-link_no_args = You didn't provide a user or alias name! Use: { $prefix }alias link (user) (alias name)
Link-alias_name_already_exists = Cannot link a new alias - you already have an alias named: { $name }!
Link-user_dont_has_alias = The provided user does not have the alias "{ $name }"!
Link-link_to_with_invalid_name = The original alias has an invalid name "{ $name }"! Please provide a custom name.
Link-link_custom_name_invalid = The custom name "{ $name }" is not valid. Please provide a valid name.
Link-link_to_link = You tried to create a link from a linked alias (alias { $target_name } by { $user_name }), so I used the original as your template{ $alias_name }. When the original changes, yours will too.
Link-link_success = Alias successfully linked{ $name }. When the original changes, yours will too.
Link-link_name_string = , with a custom name of "{ $name }"

Link-deco_helper = This subcommand is used to create link for an alias.
Link-deco_usage = How to use: { $prefix }alias link (user) cool_name
Link-deco_description = This subcommand is used to create link for an alias.

# Link Examples
Link-cmd_ex1_prefix = ## How to link an alias:
Link-cmd_ex1_args = link (user) cool_name
Link-cmd_ex1_res = User, alias linked successfully. When the original changes, yours will also change.

Link-cmd_ex2_prefix = ## It is also possible to create a link and change the alias name.
Link-cmd_ex2_args = link (user) cool_name new_cool_name
Link-cmd_ex2_res = User, alias linked successfully, with a custom name "new_cool_name". When the original changes, yours will also change.

Link-cmd_ex3_prefix = ## And if it is a link to a link:
Link-cmd_ex3_args = link (user) cool_name
Link-cmd_ex3_res = User, you attempted to create a link from an already linked alias (alias cool_name by <user>), so I used the original as your model. When the original changes, yours will also change.

## Remove
Remove-no_alias_name_provided = No alias name provided!
Remove-alias_removed = Your alias "{ $name }" has been successfully removed.

Remove-deco_helper = This subcommand is used to delete an alias.
Remove-deco_usage = How to use: { $prefix }alias remove (alias)
Remove-deco_description = This subcommand is used to delete an alias.

# Remove Examples
Remove-cmd_ex1_prefix = ## To remove an alias:
Remove-cmd_ex1_args = remove cool_name
Remove-cmd_ex1_res = User, your alias "cool_name" has been successfully removed.
Remove-cmd_ex1_suffix = When deleting an alias, the links to this alias will continue to exist and function.

## Rename
Rename-no_name_provided = You must provide both the current alias name and the new one!
Rename-alias_already_exists = You already have the "{ $name }" alias!
Rename-alias_renamed = Your alias "{ $old }" has been successfully renamed to "{ $new }".

Rename-deco_helper = This subcommand is used to rename an alias.
Rename-deco_usage = How to use: { $prefix }alias rename cool_name new_cool_name
Rename-deco_description = This subcommand is used to rename an alias.

# Rename Examples
Rename-cmd_ex1_prefix = ## To rename an alias:
Rename-cmd_ex1_args = rename cool_name new_cool_name
Rename-cmd_ex1_res = User, your alias "cool_name" has been successfully renamed to "new_cool_name".

## Extras
Extras-deco_description = This section is about advanced alias usage.

# Extras Examples
Extras-cmd_ex1_prefix = ## First, let's create an alias:
Extras-cmd_ex1_args = add advanced_usage choice 1234 123456 | count {"{0}"}
Extras-cmd_ex1_res = User, your alias "advanced_usage" has been successfully created.

Extras-cmd_ex2_prefix = ## How to use this type of alias:
Extras-cmd_ex2_args = { $prefix }{ $prefix }advanced_usage text
Extras-cmd_ex2_res = There are a total of 10 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
Extras-cmd_ex2_suffix =
    The normal response of the command would be: `There are a total of 4 characters. etc` or `There are a total of 6 characters. etc`, as `choice` would select between `1234` or `123456`, and then count would return the number of characters.
    {"\n\n"}But, due to the addition of `{"{0}"}` after count, it will take the content of what was sent when invoking the alias and replace `{"{0}"}`.
    {"\n\n"}So the command passed to count it would be something like: `text 1234`

Extras-cmd_ex3_prefix = ## An example showing all would be:
Extras-cmd_ex3_args = add advanced_usage2 choice 1234 123456 | count {"{0}"} {"{channel}"} {"{output}"} {"{user}"} {"{1+}"}
Extras-cmd_ex3_res = User, your alias "advanced_usage2" has been successfully created.

# Extras Admonitions
Extras-adm1_title = The bot's step-by-step process will be:
Extras-adm1_msg =
    - Replace `{"{0}"}` with `something_here`.
    - Replace `{"{1+}"}` with `and in the end`.
    - Replace `{"{channel}"}` with the channel to which the message was sent, for example, `gorenmu`.
    - Replace `{"{user}"}` with your username, for example, `xXNickOriginalXx`.
    - The full command would be `choice 1234 123456 | count something_here gorenmu {"{output}"} xXNickOriginalXx` which would be processed by the pipe handler.

Extras-adm2_title = The pipe handle, will do:
Extras-adm2_msg =
    - Process the first part: `choice 1234 123456` (as an example, let's say choice selected `1234`).
    - Process the second part: `count something_here gorenmu {"{output}"} xXNickOriginalXx and in the end`; when processing the second part, it will replace `{"{output}"}` with `1234`.
    - Then, the arguments that will be sent to count will be `something_here gorenmu 1234 xXNickOriginalXx and in the end.`
    - And the response will be `There are a total of 50 characters. Among them, 1 is punctuation, 4 are uppercase letters, and 0 are special characters.`

Extras-adm3_title = Other options when creating the alias are:
Extras-adm3_msg =
    - `{"{output}"}`: it will place the output of the last command at the `{"{output}"}` position.
    - `{"{channel}"}`: it will replace with the name of the current channel.
    - `{"{user}"}`: it will replace with your Twitch username.
    - `{"{0}"}`, `{"{1}"}`, `{"{2}"}` etc., you can also use `{"{3+}"}`, which will take all text sent when invoking the alias and replace.

## Templates
# Partes da documentação
Template-part1 =
    # { $command_title }
    {"\n\n"}## This command can be used { $rate } times in succession, with a cooldown of { $per } per { $cooldown_type }.{"\n\n"}
Template-part2 = { $description }{"\n\n"}{ $aliases }{"\n\n"}
Template-part3 = ## The way to use this command is:{"\n\n"}

# Templates específicos
Template-alias_template =
    ## All the alias available for { $command_title } are:
        - { $aliases }{"\n\n"}
Template-command_template =
    ```text
        user: { $prefix }{ $command_name } { $args }

        bot: User, { $response }
    ```{"\n"}
Template-admonition_template =
    !!! { $type } "{ $title }"

            { $message }{"\n\n"}

# Tipos de Bucket (Cooldown)
Template-bucket_type = { $type ->
    [channel] all user per channel
    [member] user per channel
    [user] user independent of channel
    [subscriber] subscriber
    [mod] moderation
    *[default] user
}
