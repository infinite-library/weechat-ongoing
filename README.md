Gerneral info
=============

This Project is a fork of infinite-library/weechat-ongoing, which seems to not be maintained anymore.

If anybody can help improving this script, e.g. adding a bunch of bot names and querying others in the list only,
if the file was not yet downloaded or the first on the list is unavailable, **feel free to open a PR!***

weechat-ongoing
===============

Weechat script for automatized downloading of the new releases on XDCC bots.

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
