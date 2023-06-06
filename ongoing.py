# -*- coding: utf-8 -*-
#
# ongoing.py
# Weechat script for automatized downloading of the new releases on XDCC bots.
#
# Based on the original script by Mayoi Hachikuji <mendor@yuuzukiyo.net>
# Switch to JSON breaks backwards compatibility. Take note of your bots and filters!
#
# To enable it, copy the file "ongoing.py" to ~/.weechat/python/ directory and
# execute the command "/python load python/ongoing.py"
#
# The comprehensive information about script usage can be found using
# the command "/help ongoing".
#
# Licensed under MIT, see LICENSE file content for the details.
#
#
# HERE BE DRAGONS
#

import weechat
import re
import os
import json


SCRIPT_NAME = "ongoing"
SCRIPT_AUTHOR = "Krbrs <no@mail.address>"
SCRIPT_VERSION = "2.0"
SCRIPT_LICENSE = "MIT"
SCRIPT_DESC = "Automatically downloads new files on mask from XDCC bots"
SCRIPT_COMMAND = "ongoing"

SCRIPT_CMDS = (
    "channel [name] | add_bot name regex | del_bot name | " +
    "list_bots | add_filter regex | del_filter id | list_filters"
)

SCRIPT_HELP = """Available commands:
  {0}/{2} channel{1} - get the name of the channel for monitoring
  {0}/{2} channel #nibl{1} - monitor the channel #nibl for the updates
  {0}/{2} add_bot KareRaisu .*SEND\s([0-9]+).*{1} - look for the messages from
      the bot KareRaisu matching the listed regular expression (the only
      mentioned group in regex should be pack ID! Well, this regex should work
      with the most of Eggdrop installations and masquerading ones)
  {0}/{2} list_bots{1} - list of the bots are watched
  {0}/{2} del_bot KareRaisu{1} - stop the monitoring of messages from this bot
  {0}/{2} add_filter HorribleSubs.*Kantai.*720p{1} - add filter for the files
      with the names matching with this regular expression
  {0}/{2} list_filters{1} - list of the enabled file filters with their IDs
  {0}/{2} del_filter 1{1} - delete the filter with ID 1

""".format(weechat.color("yellow"), weechat.color("chat"), SCRIPT_COMMAND)


# register new weechat script
weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

# the only default configuration option for the script
DEFAULT_OPTIONS = {
    "channel": "#news"
}

CONFIG_DIR = weechat.info_get("weechat_dir", "") + "/ongoing/"
FILE_BOTS = CONFIG_DIR + "bots.json"
FILE_FILTERS = CONFIG_DIR + "filters.json"

# create configuration directory if it doesn't exist
os.makedirs(CONFIG_DIR, exist_ok=True)


# --------------------------------------
# File manipulation helpers
def file_read(f):
    try:
        with open(f, "r") as ff:
            return json.load(ff)
    except (IOError, json.JSONDecodeError):
        return {}


def file_write(f, data):
    with open(f, "w") as ff:
        json.dump(data, ff)


# --------------------------------------
# script command handlers
def stats():
    weechat.prnt("", "stats goes here")
    return weechat.WEECHAT_RC_OK


def get_channel():
    channel_name = weechat.config_get_plugin("channel")
    weechat.prnt("", "The current channel is %s%s" % (weechat.color("green"), channel_name))
    return weechat.WEECHAT_RC_OK


def set_channel(channel_name):
    weechat.config_set_plugin("channel", channel_name.lower())
    weechat.prnt("", "The channel set to %s%s" % (weechat.color("green"), channel_name))
    return weechat.WEECHAT_RC_OK


def add_bot(bot_name, regex):
    bots = file_read(FILE_BOTS)
    bots[bot_name] = regex
    file_write(FILE_BOTS, bots)
    weechat.prnt("", "Added %s%s%s to XDCC providers list." % (weechat.color("green"), bot_name, weechat.color("chat")))
    return weechat.WEECHAT_RC_OK


def list_bots():
    bots = file_read(FILE_BOTS)
    if not bots:
        weechat.prnt("", "%sThere are no added bots to watch for updates on." % (weechat.color("red")))
    else:
        weechat.prnt("", "-- %sList of the watched bots %s--------" % (weechat.color("yellow"), weechat.color("chat")))
        for bot_name, regex in bots.items():
            weechat.prnt("", "  %s%-24s %s%s" % (weechat.color("green"), bot_name, weechat.color("chat"), regex))
        weechat.prnt("", "------------------------------------")
    return weechat.WEECHAT_RC_OK


def del_bot(bot_name):
    bots = file_read(FILE_BOTS)
    if bot_name in bots:
        bots.pop(bot_name)
        weechat.prnt("", "%s%s%s has been removed from the list." % (weechat.color("green"), bot_name, weechat.color("chat")))
        file_write(FILE_BOTS, bots)
    else:
        weechat.prnt("", "There is no bot named %s%s%s in the list to delete." % (weechat.color("red"), bot_name, weechat.color("chat")))
    return weechat.WEECHAT_RC_OK


def add_filter(fltr):
    filters_h = file_read(FILE_FILTERS)
    filters = filters_h.get('filters', [])
    filters.append(fltr)
    file_write(FILE_FILTERS, {"filters": filters})
    weechat.prnt("", "Added %s%s%s to file filters list." % (weechat.color("green"), fltr, weechat.color("chat")))
    return weechat.WEECHAT_RC_OK


def list_filters():
    filters_h = file_read(FILE_FILTERS)
    filters = filters_h.get("filters", [])
    if not filters:
        weechat.prnt("", "%sThere are no added file filters." % (weechat.color("red")))
    else:
        weechat.prnt("", "-- %sList of the file filters %s--------" % (weechat.color("yellow"), weechat.color("chat")))
        for i, fltr in enumerate(filters, start=1):
            weechat.prnt("", "%4s  %s%s%s" % (i, weechat.color("green"), fltr, weechat.color("chat")))
        weechat.prnt("", "------------------------------------")
    return weechat.WEECHAT_RC_OK


def del_filter(fltr_id):
    filters_h = file_read(FILE_FILTERS)
    filters = filters_h.get("filters", [])
    try:
        fid = int(fltr_id)
        if fid <= 0 or fid > len(filters):
            weechat.prnt("", "There is no filter ID %s%s%s in the list to delete." % (weechat.color("red"), fltr_id, weechat.color("chat")))
            return weechat.WEECHAT_RC_OK
        fltr_data = filters.pop(fid - 1)
        weechat.prnt("", "%s%s%s has been removed from the list." % (weechat.color("green"), fltr_data, weechat.color("chat")))
        file_write(FILE_FILTERS, {"filters": filters})
    except ValueError:
        weechat.prnt("", "Invalid filter ID %s%s%s." % (weechat.color("red"), fltr_id, weechat.color("chat")))
    return weechat.WEECHAT_RC_OK


# --------------------------------------
# handler for the hook for script commands
def ongoing_hook(data, buffer, args):
    a = args.split(" ", 1)
    command = a[0]
    try:
        retval = weechat.WEECHAT_RC_OK
        if command == "stats":
            retval = stats()
        elif command == "channel":
            if len(a) == 1:
                retval = get_channel()
            else:
                retval = set_channel(a[1])
        elif command == "add_bot":
            [bot_name, regex] = a[1].split(" ", 1)
            retval = add_bot(bot_name, regex)
        elif command == "list_bots":
            retval = list_bots()
        elif command == "del_bot":
            retval = del_bot(a[1])
        elif command == "add_filter":
            retval = add_filter(a[1])
        elif command == "list_filters":
            retval = list_filters()
        elif command == "del_filter":
            retval = del_filter(a[1])
    except IndexError:
        retval = weechat.WEECHAT_RC_ERROR
    return retval


# --------------------------------------
# handle for the hook for parsing channel messages
def parse_messages(data, signal, signal_data):
    srv = signal.split(',', 2)[0]
    msghash = weechat.info_get_hashtable("irc_message_parse", {"message": signal_data})
    if msghash['channel'].lower() == weechat.config_get_plugin("channel"):
        bots = file_read(FILE_BOTS)
        if msghash['nick'] in bots:
            regex = bots[msghash['nick']]
            filters = file_read(FILE_FILTERS).get('filters', [])
            for fltr in filters:
                if re.search(fltr, msghash['arguments']):
                    g = re.search(regex, msghash['arguments'])
                    if g:
                        file_id = g.group(1)
                        weechat.command("", "/msg -server %s %s xdcc send %s" % (srv, msghash['nick'], file_id))
                    break
    return weechat.WEECHAT_RC_OK


# --------------------------------------
# register the hook for script commands
weechat.hook_command(SCRIPT_COMMAND, SCRIPT_DESC, SCRIPT_CMDS, SCRIPT_HELP,
                     "channel %(channel_name)"
                     " || add_bot %(bot_name) %(regex)"
                     " || list_bots"
                     " || del_bot %(bot_name)"
                     " || add_filter %(filter)"
                     " || list_filters"
                     " || del_filter %(filter_id)",
                     "ongoing_hook", "")


# --------------------------------------
# register the hook for parsing channel messages
weechat.hook_signal("*,irc_in2_privmsg", "parse_messages", "")
