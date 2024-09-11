---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - count
---


# Count

## This command can be used 3 times in succession, with a cooldown of 10 per user independent of channel.

This command can count the number of characters, uppercase letters, punctuation marks, and special characters in a text or the content of a URL. If you provide a link and the tag `type:url`, the command fetches the page's content and performs the count based on what it finds. And it will cache the page content for 30 minutes (thirty minutes).



## The way to use this command is:

```text
    user: +count some nice text! with some 😄 caracteres, spacial!

    bot: User, There is a total of 48 characters. Of these, 3 are punctuation marks, 0 are uppercase letters, and 1 are special characters.
```

```text
    user: +count https://example.org/

    bot: User, There is a total of 20 characters. Of these, 5 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
```

```text
    user: +count  type:url https://example.com/

    bot: User, There is a total of 1257 characters. Of these, 188 are punctuation marks, 21 are uppercase letters, and 0 are special characters.
```

```text
    user: +count type:url https://example.com/ https://example.org/

    bot: User, User, There is a total of 2514 characters. Of these, 376 are punctuation marks, 42 are uppercase letters, and 0 are special characters.
```

