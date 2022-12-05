# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

if False:
    import logging
    logging.basicConfig(level=1)

import base64
import email
import email.policy
import imaplib
import logging
import pywikibot
import re
import urllib

from pywikibot.bot import CurrentPageBot, SingleSiteBot

logger = logging.getLogger(__name__)

class IMAP4JobQueue(imaplib.IMAP4_SSL):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        password = kwargs.pop("password", "")
        self.mailbox = kwargs.pop("mailbox", "INBOX")
        logger.debug("connecting to IMAP server")
        super().__init__(*args, **kwargs)
        if user is not None:
            logger.debug("authenticating")
            self._chk(self.login(user, password))
        logger.info(f"connected to {self.host}")

    def _chk(self, typ_dat):
        typ, dat = typ_dat
        if typ != "OK":
            raise self.error(dat[-1].decode(errors="ignore"))
        return dat

    @property
    def _messages(self):
        logger.debug(f"selecting {self.mailbox}")
        data = self._chk(self.select(self.mailbox))
        if data and data[0] == b"0":
            return
        logger.debug("fetching messages")
        for data in self._chk(self.fetch("1:*", "(UID RFC822)")):
            # Each data is either a string, or a tuple.
            if not isinstance(data, tuple):
                assert data == b")" # XXX why?
                continue
            # If a tuple, then the first part is the header
            # of the response, and the second part contains
            # the data (ie: 'literal' value).
            header, data = data
            header = header.split()
            assert header[1] == b"(UID"
            assert header[-2] == b"RFC822"
            assert header[-1] == b"{%d}" % len(data)
            imap_uid = header[2]
            yield imap_uid, data

    @property
    def messages(self):
        for imap_uid, data in self._messages:
            logger.debug(f"handling UID {imap_uid}")
            pywikibot.output(f"{base64.a85encode(data, wrapcol=72)}\n")
            msg = email_from_bytes(data)
            assert not hasattr(msg, "uid")
            msg.uid = imap_uid
            yield msg

def email_from_bytes(data):
    return email.message_from_bytes(
        data, policy=email.policy.default)

class Robot(SingleSiteBot, CurrentPageBot):
    def __init__(self, **kwargs):
        super(Robot, self).__init__(site=True, **kwargs)
        self._mbox_args = self.site.family.readinglist.mailbox
        self._mbox = None

    @property
    def mbox(self):
        if self._mbox is None:
            self._mbox = IMAP4JobQueue(**self._mbox_args)
        return self._mbox

    @property
    def generator(self):
        self.entries = []
        for msg in self.mbox.messages:
            entry = self.entry_for(msg)
            if entry is None:
                continue
            self.entries.append(entry)
            self.mbox._chk(self.mbox.uid("STORE", msg.uid,
                                         "+FLAGS", r"\Deleted"))
        if self.entries:
            yield pywikibot.Page(self.site, "Reading list")

    def treat_page(self):
        # Add the new entries.
        bits = [self.current_page.text.rstrip()]
        bits.extend(self.entries)
        text = "\n* ".join(bits) + "\n"
        # Strip duplicate entries.
        lines, seen = [], {}
        for line in text.rstrip().split("\n"):
            m = re.match(r"\*\s*(\{\{at\|.*?\}\}\s*)?", line)
            if m is not None:
                entry = line[len(m.group(0)):]
                if entry in seen:
                    continue
                seen[entry] = True
                line
            lines.append(line)
        # Store the updated wikitext.
        self.put_current("\n".join(lines) + "\n",
                         show_diff=(not self.getOption("always")))
        self.mbox._chk(self.mbox.expunge())

    REWRITES = (
        (r"^https?://en\.(m\.)?wikipedia\.org/wiki/", "wikipedia:"),
        (r"^https?://youtu\.be/", "https://www.youtube.com/watch?v="),
    )

    @classmethod
    def entry_for(cls, msg):
        for header in ("to", "cc", "bcc"):
            if msg[header]:
                return
        body = msg.get_body(('plain',))
        if body is None:
            return
        entry = body.get_content().strip()
        if not entry:
            return
        subject = msg["subject"]
        if subject is not None:
            subject = subject.strip()
        if subject:
            if entry.split(":", 1)[0].lower() not in ("http", "https"):
                return
        for pattern, repl in cls.REWRITES:
            entry = re.sub(pattern, repl, entry, 1, re.I)
        if entry.startswith("wikipedia:"):
            entry = urllib.parse.unquote(entry).replace("_", " ")
            entry = "[[%s]]" % entry
            if subject:
                entry = "%s ''<q>%s</q>''" % (entry, subject)
        elif subject:
            entry = "[%s %s]" % (entry, subject)
        date = msg["date"]
        if date is not None:
            entry = "{{at|%s}} %s" % (date, entry)
        return entry

def main(*args):
    args = pywikibot.handle_args(args)
    assert not args
    try:
        bot = Robot()
        bot.site.login()
        if False:  # XXX sys.stdin.isatty()
            bot.run()
        else:
            bot.options["always"] = True
            for page in bot.generator:
                bot._current_page = page
                bot.treat(page)
    except IMAP4JobQueue.error as e:
        if not e.args:
            raise
        msg = e.args[0].lower()
        for needle in ("deleted under",
                       "please relogin"):
            if msg.find(needle) >= 0:
                break
        else:
            raise

if __name__ == "__main__":
    if "sys" not in locals():
        import sys
    assert sys.version_info >= (3,)
    main()
