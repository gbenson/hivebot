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

        ("URL+subject generic link, with markup",
         r'''
6t(1K3ZqCEALnrY1E](s@j!N\1,9t,1HI?N3]&c<.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3ZpRM<E)F>3'U8);f?Ma?Z0akATD-@2*tAY7VQ4
MDfp/5EcXB$6sjG4DI6mlDKBr;ARAke?YspqBO>144WlmP<E)F>3'U8)F'gX]='n*G3'BVa4
[Ck]1LFQtH"CE)4Yf#\1.>PLBOtO84WlmP<E)F>3'U8)D/XH+?Ys^lATDZO6S^ej0MH1uCNF
cB?WL`SDa-B-4[2qG7P-Sa;*T#,9is8/0JGXW1-IoWFD,*)?V+UIF(J]hEaa05?X[D^F`^tF
0NUCm6XO>AF*),6B4!eh1-IoZ1-[oE4[2qG7P-Sa;*R'(1.=,]?X[;eARTUdBl79hCh7*uEb
T#tFEq54ATD.#DJ=2U1.,DeAm]aqBk(g`8RF\F+?_qh<(8H!5>aXY@<Q3hAoDg4?Y"(sFCeu
i@<-:/DId*kH!b6'F`V+W1.>PLF`MA6DJ*<pAnGCl5<U,P5?1ZP/N>sl5A4V8Bl8$(Ec,H1?
Z^3nF('6'?Y+%b@rua*@qg%1?Z:%(@UW_^H!b9,DEUED4ZG,Y3B;1gE^)]04[2qG7P-Sa;*S
W#Ch[s4Bk(LZF`^u!F),K-B4#q&F`Li.Ec6,8A7]dgAoD]sFD,5mCghEsF$Df14[2qG7P-Sa
;*T.c1.,DcDfTDrAS,Og@qfLlFC/m'A7]RaD..]sF('6'?[6R4?ZU.&ARB:mDIn)V1.=Dj%1
6*VATB@gB4Yt&3Zq'I3?V%)Bl"o(DfQsdDIdd+Bk.Y[9kABe@:s.'8OPT^4>8ZM6nq(d6nL>
O1I3TL75ZhP3C5GW/MfCI6UX4076*.m1I,S^ASuR-DD#g<F?U-@9hA&J/QQG'F(oQ13Zp.00
F\@VDf0Z.DKII0H#R=U+EV1>F>%TL@;0U@%144fBOPq&ATU(XFCm*a%15I@DKKH-F=gI4@;^
-uATB@kDI[TqBl7QE+E;OBFCeu7E,oZ1FCAWpAISuK/PA*@@;0O08RuCMFD5iB3ZoS^4Y\WE
->u%$-?4)i:f9_O8Q[<O4]FjP<$lQI0eb:.EBR&m:.5U!%16cjFDu:^0/%NnG<I]MFD,5uF^
]<$BjkmB1.>\kD(faEDIn)H1,(I=04\X(0/579A8c%#/R^5HATW$1AM&%GAM%b;Eb-h6Ccr4
7ARfh&Bk(k!GqF,O@;[Z*/Tc.fE,Tr3E\2ETAH''',

         '{{at|Tue, 13 Dec 2022 13:46:47 +0000}} '
         'https://www.theguardian.com/money/2022/dec/13/does-a-kettle-u'
         'se-more-electricity-than-a-tv-power-use Some older [WiFi rout'
         'ers] can consume as much as 18W (£53 a year). The more modern'
         ' Linksys Velop MX5300 that I use draws about 10W, costing £29'
         '.78 a year in electricity per unit, of which I have four dott'
         'ed around my house. Turning off the internet to save electric'
         'ity probably isn’t realistic but asking your provider for the'
         ' latest, more efficient model may save you some money.'

         ),

        ("URL+body generic link",
         r'''
6t(1K3Zq.8DCcnb1*Atr@j!N\1,9t-1-.0L3\WK8.kiY20F\@YEc5eU+@fj\Gp#FbDKB`6+?
X:FEd9o_@V'FuDf.1FATU*F$<)(VC1Ums3Znk=<HD_l/O=#\DKIo^9.`.H9jqaP+D,P4+@0m
UEc5Z&%15g@F)tc&AM$JA3ZpO=5rCD`0LS5Z2F]MZ/Mo.=3%[-L6q/ae3(>_m7RKX%3(,\jB
4>FiF)PqKDImoR%15g$9gpX7ATDj+Df.TY0eP-h$:A`LFCf?3/Q@"7ANCrUAU&;ME,8rsDEA
:7+Cf(nEcYf64`tjY/N=1H6Z6jaASuTA<,uDbF(T!(/OaPeDe*R"B0%/TF`2A5A1_b@Bl8$$
@VfTb$<SlQ3Gi2=Cb84hASuU(FEoni+`':u0Jk+p4YS4&F$3>t77KjN->#D?79EM9E'5p12^
WN-:/=VR%13OOBQS?8F#ks-GB\6o1.?:uAS6-oEb&lmDETaD@rH3;@rH4$ASuU(F(TH(AM5e
m1,:LnARdAJ1,!'RFD52uDff]'F"Ls9B6,Xf%16QbBlmctDCoR?@rH7.ASu3nDI[60F*2G@C
j@URBOu"'ATKF4$4R>H6#:U\/6r\lDf03+Bl7Q+A8-+*F`;G:Df-\>D]in*DKTQ"@ruj6Bl7
Q7+E1b0FD56-Cgh@#Gp$g=+@BgVDIFYN75@"c0KhEP+EqL5@q\"7$6Wqh@qB^(FD,5.E,ol<
E+NO$+E(j7@3B6+B4W2QDg#i*+?`.K4ZG,Y3C@A&BlkJA@<Q3F75@"c0KhEa+CT=6BlkJ+@U
X.b4Uha:DK?q@ATMs6Bk)7!Df0V=Bl5&8BOr;u@:NjkDe:,6BOr;^D/!L#Df-\@@<-'jDKI!
a75@"c0KhEP+CT;%+CT)&+Dbb-ASaL=$@*b9D]i_%G%De3DJs$#/T5MLAS,Oc@rucT1.<<bB
Or;pB4W3(Aftf*@rH7.ASu3nDI[6/+DG^9F(fK4F=\PKF!,[@FD)e>4Uha>+D,P4+CQC:BPD
9o+F.O?4YfG''',

         '{{at|Mon, 12 Dec 2022 22:27:07 +0000}} '
         'https://www.theguardian.com/commentisfree/2022/dec/12/antibio'
         'tics-eggs-britain-inconvenience-supply-shelves-'

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
