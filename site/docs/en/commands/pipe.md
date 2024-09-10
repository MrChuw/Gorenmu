---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - pipe
---



# Pipe

# This is not really a command.

!!! warning "Cooldown!"

    The cooldown for the pipe will be the same as the cooldown of the commands used.

The Pipe is represented by the character "|" (vertical bar), and it is used to forward the output of one command to another.

## How to use pipe:

```text
user: +example_command_1 <command options> | example_command_2 
or 
user: +example_command_1 <command options> | example_command_2 <command 2 options> {output} <remaining command 2 options>
```

## The bot's step-by-step will be:
 - Execute `example_command_1` with `<command options>` if any.
 - Then it will execute `example_command_2` with the response from `example_command_1` added as an argument.
   - If you use `{output}`, it will place the response from `example_command_1` in the specified position.

