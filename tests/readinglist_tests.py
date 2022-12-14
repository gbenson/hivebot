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

        ("URL+subject generic link",
         r'''
6t(1K3Zpn4Be1A\3?U_$@j!N\1,9t-1-.6N3\W92.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3ZqL;Gp$X9+EMI<AKYf-Df'P<AoDKr5>uJCFD,6
2+Ceht+E1b1F!,R<Ec6)5BHU_+A8cC,G@>bL%16*VATB@gB4Yt&3Zq'I3?V%)Bl"o(DfQsdD
Idd+Bk.Y[9kABe@:s.'8OPT^4>95l0f_Nd67k)^0eb193A<`N3C>P\/OMu^6o@7f1GL^?76k
KpASuR-DD#g<F?U-@9hA&J/QQG'F(oQ13Zp.00F\@VDf0Z.DKII0H#R=U+EV1>F>%TL@;0U@
%144fBOPq&ATU(XFCm*a%15I@DKKH-F=gI4@;^-uATB@kDI[TqBl7QE+E;OBFCeu7E,oZ1FC
AWpAISuK/PA*@@;0O08RuCMFD5iB3ZoS^4Yf#ED`od$EH=9>;FO&H==.WC<(0ng-?)+%-?21
D:JO=f$4R>UFEDJC3\N-pBQ@[%F)5c5D0%iq7:U7Q04nX4F"[''',

         '{{at|Fri, 09 Dec 2022 22:47:01 +0000}} '
         '[https://ahrenslooms.com/faqs/ Why do some looms fold?So they '
         'can pass through a doorway.]'

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

        ("URL+subject Wikipedia link",
         r'''
6t(1K3Zq@0F=\Oh0H`bp@j!N\1,9t,0KLmF3\rW9.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3Zpq8DJim'%16*VATB@gB4Yt&3Zq'I3?V%)Bl"o
(DfQsdDIdd+Bk.Y[9kABe@:s.'8OPT^4>K;Y6U<Xk3@us@0ek7:76!.V3B9Gb/M]^`2DR`k3
&F)\6U59nASuR-DD#g<F?U-@9hA&J/QQG'F(oQ13Zp.00F\@VDf0Z.DKII0H#R=U+EV1>F>%
TL@;0U@%144fBOPq&ATU(XFCm*a%15I@DKKH-F=gI4@;^-uATB@kDI[TqBl7QE+E;OBFCeu7
E,oZ1FCAWpAISuK/PA*@@;0O08RuCMFD5iB3ZoS^4Yo)FD`od$EH=9>;FO&H==.WC<(0ng-?
)+%-?21D:JO=f$4R>UFEDJC3\N-tDETaDD*9XCGA1i,E+NQo@6HA7DfTJDGA1i,01U/&FD,6
+''',

         '{{at|Sat, 10 Dec 2022 10:05:35 +0000}} '
         "[[wikipedia:Gunther]] ''<q>Gunnar</q>''"

         ),

        ("URL+body Wikipedia link, with markup",
         r'''
6t(1K3ZqL8A1SiX1a#1t@j!N\1,9t+1HI<G3\i]<.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3Znk=<HD_l/O=#\DKIo^9.`.H9jqaP+D,P4+@0m
UEc5Z&%15g@F)tc&AM$JA3ZpOD5s[Fu1c76E0eu-T/Mop_5qPA_3&E3I2`X8`2)R<[0L\GrB
4>FiF)PqKDImoR%15g$9gpX7ATDj+Df.TY0eP-h$:A`LFCf?3/Q@"7ANCrUAU&;ME,8rsDEA
:7+Cf(nEcYf64`tjY/N=1H6Z6jaASuTA<,uDbF(T!(/OaPeDe*R"B0%/TF`2A5A1_b@Bl8$$
@VfTb$<SlQ3Gi2=Cb84hASuU(FEoni+`':u1,1+o4YS4&F$3>t77KjN->#D?79EM9E'6'8-?
21D:JO=f$4R>UFEDJC3\N-tDETaDD*9XCGA1i,E+NQo@6HA7DfTJDGA1i,02Q(nATMs-DJ<N
s?Ya4bAncO%BFP:X$;Fr>AKY])+Br&@AR][uDI$O21.<<JEb/iHH[B7:FCcS4ATr3CFD5i5A
N_h;<+ohc9OW!a+A69XAncO%BHTcQ@ruX0Gp#[A%16tq:gn0OF*),6AKZACEbmlp6tg[aE&o
X*GB\6o1.?.jCh7[0Bl7L!Df092DfRur7;m3Z06;)HE%c9OBlH3j7;upZ5@JSSBfun4@r,^2
1c@'71.EC6GAhM;4YoK&@;KLrFD5W(+AHclBln96+FI^.FCdTk6o$SA8p,#_+>PW*0HbacEb
m=KFCB96F$2<IA7]14%16VgHsq&*BPDX$/Tl)M4YoK>FEDJC3\N.1AR[eX7:C4HBPDX$4YfH
EEb@%LAR[;J0JP:93ANNI1,LpE2_SidFDs8o06_Va4Uh`]1.?.jCh7[0Bl7L!Df092DfRur7
;m3Z06;)HE%c9OBlH3j7;upZ5@JSSBk(sj0f1dC,r.q4Hsq&*BPDX$/S&:3AN_h;1,h?*$6W
8YE-,Z.@V'R&1,(F;+FSZ#061W94o''',

         '{{at|Wed, 14 Dec 2022 03:30:29 +0000}} '

         ),

        ("URL+subject Instagram link",
         r'''
6t(1K3Zpn4Be1A\3?U_$@j!N\1,9t,0KLmA3]/T6.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3Zq+-@r,^s@j#9"D/`onF<GC<Df%.@Dg*=<F<G1
6Ch*t^<HD_l/O=#\DKIo^9.`.H9jqaP+D,P4+@0mUEc5Z&%15g@F)tc&AM$JA3ZpOS6UNUh2
*sY^7QE:]/MoCP2_@?^5t!:n1GD-R0L7Ka2*jPoB4>FiF)PqKDImoR%15g$9gpX7ATDj+Df.
TY0eP-h$:A`LFCf?3/Q@"7ANCrUAU&;ME,8rsDEA:7+Cf(nEcYf64`tjY/N=1H6Z6jaASuTA
<,uDbF(T!(/OaPeDe*R"B0%/TF`2A5A1_b@Bl8$$@VfTb$<SlQ3Gi2=Cb84hASuU(FEoni+`
';"1F@$'0ICd\4]#$F7S-]/Aj'*^=B$Vd4YS4&4\edJ71BS5$>=O'E-"&n06_Va4YfH?DKBo
.B6%Et4YfH9Df%.JAS#[26YnYmG]?Ah6u@3&5A=bOBPD!?1IOr*8o7=L<bkEE=ZnQ/''',

         '{{at|Fri, 09 Dec 2022 10:00:50 +0000}} '
         '[https://www.instagram.com/reel/Cl6fxqKgDmy/ '
         'Leclerc compact loom/how it fold]'

         ),
    ))
    def test(self, name, encoded_msg, expect):
        msg = email_from_bytes(a85decode(encoded_msg))
        self.assertEqual(Robot.entry_for(msg), expect)
