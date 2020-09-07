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
        self._search_for = searchfor.lower()
        generator = kwargs.pop("generator", None)
        if generator is None:
            gen_factory = pagegenerators.GeneratorFactory()
            gen_factory.handleArg("-search:" + self._search_for)
            gen_factory.handleArg("-ns:0")
            generator = gen_factory.getCombinedGenerator(preload=True)
        super(Robot, self).__init__(generator=generator, **kwargs)

    @property
    def current_page_is_linked(self):
        page = self.current_page
        assert page.content_model == "wikitext"
        code = mwparserfromhell.parse(page.text)
        return not(not code.filter_wikilinks(
            matches=lambda n: n.title.strip().lower() == self._search_for))

    def treat_page(self):
        if self.current_page.title().lower() == self._search_for:
            return
        if self.current_page_is_linked:
            return
        self.put_current(re.sub("(%s)" % self._search_for,
                                r"[[\1]]",
                                self.current_page.text,
                                count=1,
                                flags=re.I),
                         summary="link [[%s]]" % self._search_for)

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
