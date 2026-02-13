# Translation for Count
Count-character_count = There is a total of { $length } characters. Of these, { $punc } are punctuation marks, { $upper } are uppercase letters, and { $special } are special characters.

Count-deco_helper = Counts the number of symbols in a text or a URL.
Count-deco_usage = To use: { $prefix }count (text) or type:url (URL URL URL URL)
Count-deco_description = This command can count the number of characters, uppercase letters, punctuation marks, and special characters in a text or the content of a URL. If you provide a link and the tag `type:url`, the command fetches the page's content and performs the count based on what it finds. And it will cache the page content for 30 minutes (thirty minutes).

# Commands
Count-cmd_ex1_prefix = Simple text count with emoji.
Count-cmd_ex1_res = There is a total of 48 characters. Of these, 3 are punctuation marks, 0 are uppercase letters, and 1 are special characters.

Count-cmd_ex2_prefix = Counting characters in a link (as plain text).
Count-cmd_ex2_res = There is a total of 20 characters. Of these, 5 are punctuation marks, 0 are uppercase letters, and 0 are special characters.

Count-cmd_ex3_prefix = Counting content fetched from a URL.
Count-cmd_ex3_res = There is a total of 1257 characters. Of these, 188 are punctuation marks, 21 are uppercase letters, and 0 are special characters.
