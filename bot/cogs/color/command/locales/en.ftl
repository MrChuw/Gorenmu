Color-color = { $res1 } { $res2 }
Color-no_user_hex = User not found or valid hex color provided.
Color-user_not_color = Provided user has no color defined on twitch.
Color-user_color = @{ $name } color is: #{ $hex_value }. Named: { $hex_name }
Color-hex_color = #{ $hex_value } its Named: { $hex_name }
Color-saved_color = And has the following saved color: #{ $hex_value }. Named: { $hex_name }.
Color-deco_helper = Command to get Twitch or hex color info.
Color-deco_usage = How to use: { $prefix }color (username | hex)
Color-deco_description = This command returns information about a user's Twitch color, a saved color, or a given hex color. It includes name lookup and color preview links.

# Commands
Color-cmd_ex1_prefix = If a valid twitch user is passed.
Color-cmd_ex1_res = @mr_chuw color is: #00FFFF. Named: Cyan / Aqua.

Color-cmd_ex2_prefix = If a valid hex code is passed.
Color-cmd_ex2_res = #FF4500 is named: Vermilion.

Color-cmd_ex3_prefix = If the user has a saved color in the database.
Color-cmd_ex3_res = @mr_chuw color is: #00FFFF. Named: Cyan / Aqua. And has the following saved color: #1E90FF. Named: Dodger Blue.

# Admonitions
Color-adm_title = Username or HEX
Color-adm_msg = You can input a Twitch username or a 6-digit hexadecimal color code like #FF00FF.
