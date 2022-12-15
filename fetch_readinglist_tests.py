# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
import imaplib
import logging

from pywikibot import Family
from scripts.userscripts.readinglist import email_from_bytes, Robot

logger = logging.getLogger(__name__)

class TestFetcher(imaplib.IMAP4_SSL):
    def __init__(self, family=None):
        secrets = Family.load("hive").readinglist.mailbox
        (server, login, mailbox) = self._destructure_secrets(secrets)
        self.mailbox = self._rewrite_mailbox_name(mailbox)
        logger.info(f"connecting to {server}")
        super().__init__(**server)
        logger.info("authenticating")
        self._chk(self.login(*login))

    @classmethod
    def _destructure_secrets(cls, secrets):
        server = secrets.copy()
        username = server.pop("user")
        password = server.pop("password")
        mailbox = server.pop("mailbox")
        return (server, (username, password), mailbox)

    @classmethod
    def _rewrite_mailbox_name(cls, c):
        k = (0, 0, 0, 0, 0, 0, 7, 26, 20, 20, 26)
        return "".join(map(chr,(a ^ b for a, b in zip(map(ord, c), k))))

    def _chk(self, typ_dat):
        typ, dat = typ_dat
        if typ != "OK":
            raise self.error(dat[-1].decode(errors="ignore"))
        return dat

    @property
    def messages(self):
        logger.info(f"selecting {self.mailbox}")
        data = self._chk(self.select(self.mailbox))
        if data and data[0] == b"0":
            return
        logger.info("fetching messages")
        for data in self._chk(self.fetch("1:*", "(UID RFC822)")):
            # Each data is either a string, or a tuple.
            if not isinstance(data, tuple):
                assert data == b")"  # XXX why?
                continue
            # If a tuple, then the first part is the header
            # of the response, and the second part contains
            # the data (ie: 'literal' value).
            header, data = data
            header = header.split()
            assert header[1] == b"(UID"
            assert header[-2] == b"RFC822"
            assert header[-1] == b"{%d}" % len(data)
            logger.debug(f"handling UID {header[2]}")
            msg = email_from_bytes(data)
            assert not hasattr(msg, "uid")
            msg.uid = header[2]
            yield msg

    @property
    def shared_links(self):
        for msg in self.messages:
            body = msg.get_body(('plain',))
            body = body.get_content().strip()
            body = body.replace("\r\n", "\n")
            for encoded in body.split("\n\n"):
                try:
                    decoded = base64.a85decode(encoded)
                except ValueError as e:
                    if str(e) != "Ascii85 overflow":
                        raise
                    # A non-Ascii85 bit in the email...
                    logger.debug(f"failed to decode {repr(encoded)}")
                    continue
                decoded_msg = email_from_bytes(decoded)
                wikitext = Robot.entry_for(decoded_msg)
                yield {"date": msg["date"],
                       "encoded": encoded,
                       "content": wikitext}

def main(*args):
    messages = []
    for msg in TestFetcher(*args).shared_links:
        messages.append((len(msg["encoded"]), msg))
    for msg in sorted(messages):
        _, msg = msg
        sep = "}}"
        date, content = msg["content"].split(sep, 1)
        print(f"\x1B[32mProcessed: {msg['date']}\x1B[0m")
        print(f"\x1B[33m{msg['encoded']}\x1B[0m")
        print(f"\x1B[36m{date}{sep}\x1B[0m{content}")

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    main("hive")
