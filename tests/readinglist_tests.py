# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from base64 import a85decode
from parameterized import parameterized
from unittest import TestCase

from scripts.userscripts.readinglist import email_from_bytes, Robot

# nosetests -v tests/readinglist_tests.py

class TestReadingListParser(TestCase):

    """Regression tests for Robot.entry_for."""

    @parameterized.expand((
        ("URL-only generic link",
         r'''
6t(1K3Zq.8DCcnc3$:t7Fs&Oo1,9t,2EEQQ3\rc=/MJk40F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$:A`LFCf?3/Q@"7ANCrUAU&;ME,8rsDEAtNBOPq&ATU'ZF`_4
I3$Je=6Z6jaASuTA<,uDbF(T!(/OaPeDe*R"B0%.o@VKon$;F)d74hPOEcYr5DE8mp/hd_A%
16cjFDu:^0/%9YDJsQ0@4l&.D(fR@G:doT/UD,M/Tc2T/R`[?@<loGBl5M;@<Q(#@rc:&F>"
(1''',
         '{{at|Mon, 28 Nov 2022 16:19:39 -0000}} '
         'https://pinoria.com/how-to-zip-two-arrays-in-javascript/'

         ),
        ("URL-only Wikipedia link",
         r'''
6t(1K3Zq.8DCcnc3$:t7Fs&Oo1,9t,2```K3\`?3.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3Znk=<HD_l/O=#\DKIo^9.`.H9jqaP+D,P4+@0m
UEc5Z&%15g@F)tc&AM$JA3ZpOQ1,C[C5r(eZ2+0kj/Mop`74gep3(5DU7PHSd5t!Xu3AiQWB
4>FiF)PqKDImoR%15g$9gpX7ATDj+Df.TY0eP-h$:A`LFCf?3/Q@"7ANCrUAU&;ME,8rsDEA
:7+Cf(nEcYf64`tjY/N=1H6Z6jaASuTA<,uDbF(T!(/OaPeDe*R"B0%/TF`2A5A1_b@Bl8$$
@VfTb$<SlQ3Gi2=Cb84hASuU(FEoni+`';!1F@$'0ICd\4]#$F7S-]/Aj'*^=B$Vd4YS4&4\
edJ71BS5$>=O'E-"&n04f#a1.?%C1.?D$CM@a!A8,I81.?,%B.nICCM>FqARTY%?Xn"kD/X<
!D09Z:BlIm"''',

         '{{at|Mon, 28 Nov 2022 17:30:11 +0000}} '
         '[[wikipedia:Least common multiple]]'

         ),
    ))
    def test(self, name, encoded_msg, expect):
        msg = email_from_bytes(a85decode(encoded_msg))
        self.assertEqual(Robot.entry_for(msg), expect)
