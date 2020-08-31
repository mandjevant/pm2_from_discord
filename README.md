# pm2_from_discord

Access pm2 on multiple servers through discord.

## Configuration

- Add a file `conf.ini` and populate it like `example.conf.ini`
- Add a folder `ssh_keys`
- Place your `.pem` key(s) in folder `ssh_keys`
- Optionally populate `on_message_users` in `scripts.py` to be notified when the bot detects a regex match.

## License
[MIT](https://choosealicense.com/licenses/mit/)