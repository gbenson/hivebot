# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

if False:
    import logging
    logging.basicConfig(level=1)

import mwparserfromhell
import pywikibot
import re

from pywikibot import pagegenerators
from pywikibot.bot import (ExistingPageBot,
                           MultipleSitesBot,
                           NoRedirectPageBot)

class Robot(MultipleSitesBot, ExistingPageBot, NoRedirectPageBot):
    def __init__(self, searchfor=None, **kwargs):
        self._summary = f"link [[{searchfor}]]"
        self._search_for = searchfor.lower()
        generator = kwargs.pop("generator", None)
        if generator is None:
            gen_factory = pagegenerators.GeneratorFactory()
            gen_factory.handleArg("-search:" + self._search_for)
            gen_factory.handleArg("-ns:0")
            generator = gen_factory.getCombinedGenerator(preload=True)
        super(Robot, self).__init__(generator=generator, **kwargs)

    def _page_is_linked(self, page):
        assert page.content_model == "wikitext"
        code = mwparserfromhell.parse(page.text)
        return not(not code.filter_wikilinks(
            matches=lambda n: n.title.strip().lower() == self._search_for))

    def skip_page(self, page):
        if page.title().lower() == self._search_for:
            return True
        if self._page_is_linked(page):
            return True
        return super(Robot, self).skip_page(page)

    def treat_page(self):
        self.put_current(re.sub("(%s)" % self._search_for,
                                r"[[\1]]",
                                self.current_page.text,
                                count=1,
                                flags=re.I),
                         summary=self._summary)

def main(*args):
    args = pywikibot.handle_args(args)
    assert len(args) == 1
    Robot(*args).run()
    return True

if __name__ == "__main__":
    if "sys" not in locals():
        import sys
    assert sys.version_info >= (3,)
    main()
