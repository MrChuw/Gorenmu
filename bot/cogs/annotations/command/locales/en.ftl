## Add
Add-deco_helper = This subcommand is used to add an note.
Add-deco_usage = How to use: { $prefix }note add (text)
Add-deco_description = This command is used to add annotation.

# Add Examples
Add-cmd_ex1_args = add A note about something I want to be able to check forever.
Add-cmd_ex1_res = Note successfully created. 📝 (ID: (note ID))
Add-cmd_ex2_args = add title:"title easier to remember" A note about something I want to be able to check forever.
Add-cmd_ex2_res = Note successfully created. 📝 (ID: (note ID))

# Add Admonitions
Add-adm1_title = Maximum Length for 'add'!
Add-adm1_msg = The message cannot exceed 450 characters; if it does, an error will be returned.
Add-adm2_title = Maximum Length for 'add' Title!
Add-adm2_msg = The title cannot exceed 32 characters; if it does, an error will be returned.
Add-adm3_title = Annotations and Aliases
Add-adm3_msg = Use aliases and notes together to create custom commands. For example, with { $prefix }alias add cakes note check (id), you can use { $prefix }{ $prefix }cakes to have the bot automatically send the note content, without needing to use the full command note check (id).

## Check
Check-deco_helper = This subcommand is used to check infos for an note.
Check-deco_usage = How to use: { $prefix }note check (id)
Check-deco_description = This subcommand is used to check an annotation.

# Check Examples
Check-cmd_ex1_args = check
Check-cmd_ex1_res = Your notes are those with ID: (title if available [id])
Check-cmd_ex2_args = check (id)
Check-cmd_ex2_res = (Note content)

## Delete
Delete-deco_helper = This subcommand is used to delete an note.
Delete-deco_usage = How to use: { $prefix }note delete cool_name
Delete-deco_description = This subcommand is used to delete an annotation.

# Delete Examples
Delete-cmd_ex1_args = delete (id)
Delete-cmd_ex1_res = Your note with ID (id) was successfully deleted. 🗑

## Annotations (Base)
Annotations-title_too_long = The title must have a maximum of 32 characters.
Annotations-too_few_characters = You forgot to send the annotation content.
Annotations-annotation_created = Note successfully created. 📝 (ID: { $note_id })
Annotations-no_annotations_with_id = You don't have any annotation with ID { $note_id }.
Annotations-all_annotations = Your annotations are the ones with ID: { $note_id }
Annotations-annotation_content = { $content }
Annotations-deleted = Your annotation with ID { $note_id } was successfully deleted. 🗑
Annotations-option_not_recognized = The valid options are only "add" "check" "delete"
Annotations-no_annotation_present = You don't have any annotations saved.
Annotations-deco_helper = Creates permanent notes for the user.
Annotations-deco_usage = To use: { $prefix }note add/check/delete
Annotations-deco_description = Creates permanent notes for the user.
