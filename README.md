weechat-ongoing
===============

Weechat script for automatized downloading of the new releases on XDCC bots.

I don't think that I'm gonna continue maintaining it because of reasons. Using [more up to date version](https://github.com/krbrs/weechat-ongoing) is more recommended.

To enable it copy the file `ongoing.py` to `~/.weechat/python/` directiry and
execute the command `/python load python/ongoing.py`

The comprehensive information about script usage can be found using
the command `/help ongoing`.

Don't forget to set the option `xfer.file.auto_accept_files` to `on` (see
[an appropriate Weechat user's guide section](https://weechat.org/files/doc/stable/weechat_user.en.html#xfer_options)
for the details).

License
-------

[MIT](https://opensource.org/licenses/MIT)
