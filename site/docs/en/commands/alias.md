---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - alias
---



# Alias

## This command can be used 3 times in succession, with a cooldown of 10 per user independent of channel.

!!! warning "Restrictions for alias names!"

    - Must be between 2 and 30 characters long.
    - Can contain letters, numbers, dashes, underscores, and a wide range of Unicode characters, including emojis.

!!! warning "Cooldown for created aliases!"

    When creating an alias, the alias cooldown will be the cooldown of the commands used in the alias. Therefore, if one command can be used 1x every 5 seconds and another 3x every 10 seconds, the alias cooldown will be 1x every 5 seconds.


This command manages custom aliases for commands. With it, you can:

 - Add a new alias for an existing command.
 - Check or list existing aliases.
 - Copy aliases from another user.
 - Describe an alias with a custom description.
 - Edit an existing alias, updating the associated command.
 - Link an alias to another alias or create an alias based on an existing alias.
 - Remove an alias.
 - Rename an alias.

Use the command followed by an action (add, check, copy, describe, edit, link, remove, rename) to perform the desired task.


## How to create an alias:
 - The following example uses [pipe](pipe.md) to pass the response of one command to another.

```text
user: +alias add cool_name choice 1234 123456 | count

bot: User, your alias "cool_name" has been successfully created.
```

In the example above, we created an alias named `cool_name`. The alias will invoke the `choice` command with the arguments "1234" and "123456", and the result from `choice` will be sent to the `count` command.

## To use the alias:

```text
user: ++cool_name

bot: User, there is a total of 4 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
or
bot: User, there is a total of 6 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
```

To use the alias, just use `++` followed by the alias name (+ is the bot's default prefix; if the chat prefix is different, simply repeat it 2 (two) times and then the alias name).

## How to check an alias:

```text
user: +alias check cool_name 

bot: User, the alias "cool_name" has the arguments: choice 1234 123456 | count || Link: <url>
```

## How to copy an alias:

```text
user: +alias copy <username> cool_name 

bot: User, alias "cool_name" copied successfully.
```

To copy an alias, you only need the username and the alias name.

## How to add a description to an alias:

```text
user: +alias description cool_name <new description>

bot: User, the description for alias "cool_name" has been successfully updated.
```

## How to edit the command/arguments of an alias:

```text
user: +alias edit cool_name choice 123 1234 12345 | count

bot: User, the alias "cool_name" has been successfully edited.
```

In the example above, the command was edited by changing the arguments from `1234 123456` to `123 1234 12345`. To update, you need to send the full command and only change the part you want to update.

## How to link an alias:

```text
user: +alias link <user> cool_name

bot: User, alias linked successfully. When the original changes, yours will also change.
```

It is also possible to create a link and change the alias name.

```text
user: +alias link <user> cool_name new_cool_name

bot: User, alias linked successfully, with a custom name "new_cool_name". When the original changes, yours will also change.
```

And if it is a link to a link:

```text
user: +alias link <user> cool_name

bot: User, you attempted to create a link from an already linked alias (alias cool_name by <user>), so I used the original as your model. When the original changes, yours will also change.
```

## To remove an alias:

```text
user: +alias remove cool_name

bot: User, your alias "cool_name" has been successfully removed.
```

When deleting an alias, the links to this alias will continue to exist and function.

## To rename an alias:

```text
user: +alias rename cool_name new_cool_name

bot: User, your alias "cool_name" has been successfully renamed to "new_cool_name".
```

# Advanced alias usage:

## First, let's create an alias:

```text
user: +alias add advanced_usage choice 1234 123456 | count {0}

bot: User, your alias "advanced_usage" has been successfully created.
```

# How to use this type of alias:

```text
user: ++advanced_usage text

bot: There are a total of 10 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
```

The normal response of the command would be: `There are a total of 4 characters. etc` or `There are a total of 6 characters. etc`, as `choice` would select between `1234` or `123456`, and then count would return the number of characters.

But, due to the addition of `{0}` after count, it will take the content of what was sent when invoking the alias and replace `{0}`.

# Other options when creating the alias are:
 - `{output}`: it will place the output of the last command at the `{output}` position.
 - `{channel}`: it will replace with the name of the current channel.
 - `{user}`: it will replace with your Twitch username.
 - `{0}`, `{1}`, `{2}` etc., you can also use `{3+}`, which will take all text sent when invoking the alias and replace.

## An example showing all would be:

```text
user: +alias add advanced_usage2 choice 1234 123456 | count {0} {channel} {output} {user} {1+}

bot: User, your alias "advanced_usage2" has been successfully created.
```

Let's imagine you used the command like this: `++advanced_usage2 something_here and in the end`:

## The bot's step-by-step process will be:
 - Replace `{0}` with `something_here`.
 - Replace `{1+}` with `and in the end`.
 - Replace `{channel}` with the channel to which the message was sent, for example, `gorenmu`.
 - Replace `{user}` with your username, for example, `xXNickOriginalXx`.
 - Send the result `choice 1234 123456 | count something_here gorenmu {output} xXNickOriginalXx` and in the end to be processed by the pipe.

## When it reaches the pipe, it will:
 - Process the first part: `choice 1234 123456` (as an example, let's say choice selected `1234`).
 - Process the second part: `count something_here gorenmu {output} xXNickOriginalXx and in the end`; when processing the second part, it will replace `{output}` with `1234`.
 - Then, the command that will be sent to count will be `count something_here gorenmu 1234 xXNickOriginalXx and in the end.`
 - And the response will be `There are a total of 50 characters. Among them, 1 is punctuation, 4 are uppercase letters, and 0 are special characters.` 
