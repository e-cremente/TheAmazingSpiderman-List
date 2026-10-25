"""Fasi 7-11 (1999-2026): tutte le testate di Peter Parker alternate per mese di uscita, eventi in ordine esatto."""
import json, re, os
S = os.path.dirname(os.path.abspath(__file__))

def M(s):
    y, m = map(int, s.split('-')); return y * 12 + (m - 1)
def T(it, en): return {'it': it, 'en': en}

items = {}          # id -> item
order_hint = []     # per stabilità
def add(iid, n, s, date, kind=None, key=False, tip=None, full=None, rot=None, ser=None, num=None):
    assert iid not in items, iid
    items[iid] = dict(id=iid, n=n, s=s, date=date, kind=kind, key=key, tip=tip, full=full, rot=rot, ser=ser, num=num)
    order_hint.append(iid)

def interp(anchors, n):
    a = sorted(anchors)
    for (n0, d0), (n1, d1) in zip(a, a[1:]):
        if n0 <= n <= n1:
            return d0 if n1 == n0 else d0 + (d1 - d0) * (n - n0) / (n1 - n0)
    raise ValueError(n)

def series(pre, tok, s, nums, anchors, kind=None, keys=(), tips=None, full=None):
    an = [(k, M(v)) for k, v in anchors]
    for n in nums:
        add(f'{pre}{n}', f'{tok} {n}', s, interp(an, n), kind=kind, key=n in keys,
            tip=(tips or {}).get(n), full=(full.format(n=n) if full else None), ser=pre, num=n)

# ---------------- Amazing ----------------
series('a99-', "ASM'99", 'asm', range(1, 59), [(1,'1999-01'),(58,'2003-10')], keys=(30,36),
       tips={30: T('Inizia il ciclo di J. Michael Straczynski', 'J. Michael Straczynski\'s run begins'),
             36: T('Il numero dell\'11 settembre', 'The September 11 issue'),
             38: T('Zia May scopre il segreto di Peter', 'Aunt May learns Peter\'s secret')})
items['a99-38']['key'] = True
def asm_legacy(a, b, anchors, keys=(), tips=None):
    an = [(k, M(v)) for k, v in anchors]
    for n in range(a, b + 1):
        add(f'asm{n}', f'#{n}', 'asm', interp(an, n), key=n in keys, tip=(tips or {}).get(n), ser='asm', num=n)
asm_legacy(500, 545, [(500,'2003-11'),(524,'2005-09'),(529,'2006-02'),(545,'2007-12')], keys=(500,509,532),
           tips={509: T('Inizio di "Sins Past"', 'Start of "Sins Past"'), 532: T('Civil War: Peter si smaschera', 'Civil War: Peter unmasks')})
asm_legacy(546, 647, [(546,'2008-01'),(647,'2010-11')], keys=(546,600,634),
           tips={546: T('Brand New Day: tre uscite al mese', 'Brand New Day: three issues a month'), 634: T('Inizio di "Grim Hunt"', 'Start of "Grim Hunt"')})
asm_legacy(648, 700, [(648,'2010-11'),(700,'2012-12')], keys=(648,682,698,700),
           tips={648: T('Big Time, inizia Dan Slott da solo', 'Big Time, Dan Slott goes solo'), 682: T('Inizio di "Ends of the Earth"', 'Start of "Ends of the Earth"'),
                 698: T('Inizio di "Dying Wish"', 'Start of "Dying Wish"'), 700: T('Fine del volume storico', 'The end of the original volume')})
for n, d in (('654.1','2011-02'),('679.1','2012-02'),('699.1','2012-12')):
    add('asm' + n.replace('.', 'p'), '#' + n, 'asm', M(d) + .5)
for i in range(1, 6): add(f'asm700p{i}', f'#700.{i}', 'asm', M('2013-12') + i * .3)
for n, d in (("'99",'1999-08'),('2000','2000-08'),('2001','2001-08')):
    add('ann' + n.strip("'"), f'Annual {n}', 'asm', M(d), kind='ess', rot=9)
series('ssm', 'SSM', 'misc', range(1, 32), [(1,'2013-01'),(31,'2014-05')], kind='ess', keys=(1,27),
       tips={1: T('Otto Octavius nel corpo di Peter', 'Otto Octavius in Peter\'s body'), 27: T('Inizio di "Goblin Nation"', 'Start of "Goblin Nation"')})
add('ssma1', 'SSM Ann. 1', 'misc', M('2014-03'), kind='ess', rot=9); add('ssma2', 'SSM Ann. 2', 'misc', M('2014-05'), kind='ess', rot=9)
series('a14-', "ASM'14", 'asm', range(1, 19), [(1,'2014-04'),(3,'2014-06'),(16,'2015-04'),(18,'2015-06')], keys=(1,),
       tips={1: T('Peter torna nel suo corpo', 'Peter is back in his own body')})
for i in range(1, 6): add(f'a14-1p{i}', f"ASM'14 1.{i}", 'asm', M('2014-06') + i * .8, tip=T('Learning to Crawl: i primi giorni da eroe', 'Learning to Crawl: his first days as a hero'))
for i in range(16, 21): add(f'a14-{i}p1', f"ASM'14 {i}.1", 'asm', M('2015-03') + (i - 16) * .9)
series('a15-', "ASM'15", 'asm', range(1, 33), [(1,'2015-10'),(32,'2017-09')], keys=(1,),
       tips={1: T('Peter alla guida delle Parker Industries', 'Peter runs Parker Industries')})
for i in range(1, 7): add(f'a15-1p{i}', f"ASM'15 1.{i}", 'asm', M('2016-01') + i * .8)
asm_legacy(789, 801, [(789,'2017-10'),(801,'2018-06')], keys=(797,801),
           tips={797: T('"Go Down Swinging", fine del ciclo di Slott', '"Go Down Swinging", the end of Slott\'s run')})
series('a18-', "ASM'18", 'asm', range(1, 94),
       [(1,'2018-07'),(15,'2019-02'),(16,'2019-03'),(23,'2019-06'),(44,'2020-03'),(45,'2020-08'),(49,'2020-09'),(50,'2020-10'),
        (55,'2021-01'),(69,'2021-06'),(70,'2021-06'),(74,'2021-09'),(75,'2021-10'),(93,'2022-03')], keys=(1,16,50,75),
       tips={1: T('Inizia Nick Spencer', 'Nick Spencer begins'), 16: T('Hunted', 'Hunted'), 50: T('Last Remains', 'Last Remains'), 75: T('Beyond: tocca a Ben Reilly', 'Beyond: Ben Reilly takes over')})
for n in (16, 18, 19, 20): add(f'a18-{n}hu', f"ASM'18 {n}.HU", 'asm', 0)
for n in range(50, 55): add(f'a18-{n}lr', f"ASM'18 {n}.LR", 'asm', 0)
for n in (78, 80, 88, 92): add(f'a18-{n}bey', f"ASM'18 {n}.BEY", 'asm', 0)
series('a22-', "ASM'22", 'asm', range(1, 71),
       [(1,'2022-04'),(14,'2022-11'),(18,'2023-01'),(37,'2023-10'),(38,'2023-10'),(39,'2023-12'),(44,'2024-02'),(45,'2024-03'),
        (60,'2024-10'),(61,'2024-11'),(70,'2025-03')], keys=(1,61),
       tips={1: T('Zeb Wells e John Romita Jr.', 'Zeb Wells and John Romita Jr.'), 61: T('Le 8 morti di Spider-Man', 'The 8 Deaths of Spider-Man')})
add('a22-65d', "ASM'22 65.DEATHS", 'asm', M('2025-01') + .5); add('a22-68d', "ASM'22 68.DEATHS", 'asm', M('2025-02') + .5)
series('a25-', "ASM'25", 'asm', range(1, 36), [(1,'2025-04'),(22,'2026-02'),(23,'2026-03'),(27,'2026-04'),(28,'2026-05'),(35,'2026-08')], keys=(1,),
       tips={1: T('Joe Kelly e Pepe Larraz', 'Joe Kelly and Pepe Larraz')})
add('asm1000', '#1000', 'asm', M('2026-09'), key=True, tip=T('Numero celebrativo con storie di autori storici', 'Anniversary issue with stories by classic creators'))
add('asm1001', '#1001', 'asm', M('2026-10'), tip=T('14 ottobre 2026, l\'ultimo uscito', 'October 14, 2026, the latest issue'))
for y in ('2015','2017','2018','2019','2021','2023'): add(f'ann{y}', f'Annual {y}', 'asm', M(f'{y}-08'), kind='ess', rot=9)
add('p9ann', 'Annual 2026', 'asm', M('2026-06'), kind='ess', rot=9)

# ---------------- serie parallele (gruppo 2) ----------------
series('ppsm', 'PPSM', 'sm', range(1, 58), [(1,'1999-01'),(57,'2003-08')])
series('sp03-', "SPEC'03", 'spec', range(1, 28), [(1,'2003-09'),(27,'2005-06')])
series('mksm', 'MKSM', 'web', range(1, 23), [(1,'2004-06'),(18,'2005-09'),(22,'2006-03')])
series('sens06-', "SENS'06", 'web', range(23, 42), [(23,'2006-04'),(41,'2007-11')])
series('fnsm', 'FNSM', 'mtu', range(1, 25), [(1,'2005-10'),(24,'2007-10')])
add('fnsma1', 'FNSM Ann. 1', 'mtu', M('2007-07'), rot=9); add('sens06a1', "SENS'06 Ann. 1", 'web', M('2007-07'), rot=9)
series('mtu05-', "MTU'05", 'mtu', range(1, 26), [(1,'2005-01'),(25,'2006-12')])
series('avsm', 'AVSM', 'web', range(1, 23), [(1,'2011-11'),(22,'2013-06')], tips={8: T('Ends of the Earth', 'Ends of the Earth')})
add('avsma1', 'AVSM Ann. 1', 'web', M('2012-08'), rot=9)
series('ssmtu', 'SSMTU', 'misc', range(1, 13), [(1,'2013-07'),(12,'2014-04')])
series('spidey', 'SPIDEY', 'misc', range(1, 13), [(1,'2015-12'),(12,'2016-11')],
       tips={1: T('Ambientata agli inizi della carriera', 'Set early in his career')})
series('smdp', 'SM/DP', 'misc', range(1, 51), [(1,'2016-01'),(50,'2019-05')])
series('ppss', 'PPSS', 'spec', list(range(1, 7)) + list(range(297, 311)), [(1,'2017-07'),(6,'2017-12'),(297,'2018-01'),(310,'2018-09')],
       full='Peter Parker: The Spectacular Spider-Man #{n}')
series('fnsm19-', "FNSM'19", 'mtu', range(1, 15), [(1,'2019-01'),(14,'2019-12')])
series('nssm', 'NSSM', 'misc', range(1, 6), [(1,'2021-03'),(5,'2021-09')])
series('savage', 'SAVAGE', 'misc', range(1, 6), [(1,'2022-02'),(5,'2022-06')])
series('sm22-', "SM'22", 'sm', range(8, 12), [(8,'2023-07'),(11,'2023-10')])
series('ssm24-', "SSM'24", 'misc', range(1, 9), [(1,'2024-01'),(8,'2024-08')])
series('ssmen', 'SSMEN', 'spec', range(1, 16), [(1,'2024-03'),(15,'2025-05')])

# ---------------- antologie (gruppo 3) ----------------
series('webs', 'WEBSPIN', 'misc', range(1, 19), [(1,'1999-01'),(18,'2000-06')], kind='opt')
series('tw', 'TW', 'misc', range(1, 23), [(1,'2001-06'),(22,'2003-03')], kind='opt')
series('smu04-', "SMU'04", 'smu', range(1, 16), [(1,'2004-03'),(15,'2006-07')], kind='opt')
series('smf', 'SMF', 'misc', range(1, 10), [(1,'2007-04'),(9,'2008-06')], kind='opt')
series('asmf', 'ASMF', 'misc', range(1, 9), [(1,'2008-10'),(8,'2009-09')], kind='opt')
series('web09-', "WEB'09", 'misc', range(1, 13), [(1,'2009-12'),(12,'2010-11')], kind='opt')
series('sfoes', 'FOES', 'misc', range(1, 18), [(1,'2013-07'),(17,'2014-11')], kind='opt')
series('mtu19-', "MTU'19", 'mtu', range(1, 7), [(1,'2019-06'),(6,'2019-09')], kind='opt')

# ---------------- miniserie e speciali (singola tessera) ----------------
def one(iid, label, date, kind='opt', tip=None, key=False):
    add(iid, label, 'misc', M(date), kind=kind, tip=tip, key=key, rot=8); items[iid]['g'] = 'minis'
for iid, label, date in [
    ('deathdestiny','Death and Destiny #1–3','2000-08'),('revgg','Revenge of the Green Goblin #1–3','2000-10'),
    ('mysmanif','The Mysterio Manifesto #1–3','2001-01'),('ddsm01','Daredevil/Spider-Man #1–4','2001-01'),('lifeline','Lifeline #1–3','2001-04'),
    ('quality','Quality of Life #1–4','2002-07'),('getkraven','Get Kraven #1–6','2002-08'),
    ('sweetcharity','Sweet Charity','2002-08'),('smdd02','Spider-Man/Daredevil','2002-10'),('smwolv03','Spider-Man/Wolverine #1–4','2003-08'),
    ('negexp','Negative Exposure #1–5','2003-12'),('outreach','Out of Reach #1–5','2004-01'),('yearone','Doctor Octopus: Year One #1–5','2004-08'),
    ('smht','Spider-Man/Human Torch #1–5','2005-03'),('tuspecial','Spider-Man Team-Up Special','2005-05'),('breakout','Breakout #1–5','2005-06'),
    ('smfam05','Spider-Man Family (2005)','2005-10'),('arana','Spider-Man & Araña Special','2006-05'),('smfam06','Spider-Man Family (2006)','2006-10'),
    ('bbrall','Black and Blue and Read All Over','2006-11'),('smff07','Spider-Man and the Fantastic Four #1–4','2007-06'),
    ('swingshift','Swing Shift','2008-02'),('asmextra','ASM: Extra! #1–3','2008-09'),('siasm','Secret Invasion: ASM #1–3','2008-10'),
    ('xmsm','X-Men/Spider-Man #1–4','2009-01'),('fear09','Spider-Man: Fear Itself','2009-03'),('bahia','Bahía de los Muertos','2009-05'),
    ('shorthall','Short Halloween','2009-07'),('chemrom','A Chemical Romance','2009-11'),('drlist','Dark Reign: The List','2010-01'),
    ('smsw10','Spider-Man: Secret Wars #1–4','2010-04'),('peterparker10','Peter Parker #1–5','2010-05'),('siegesm','Siege: Spider-Man','2010-06'),
    ('originhunter','Origin of the Hunter','2010-06'),('fever','Fever #1–3','2010-06'),('manyloves','The Many Loves of Spider-Man','2010-07'),
    ('astsmw','Astonishing Spider-Man & Wolverine #1–6','2010-07'),('wwhulks','World War Hulks: Spider-Man vs. Thor #1–2','2010-09'),
    ('smff10','Spider-Man/Fantastic Four #1–4','2010-09'),('backquack','Back in Quack','2010-11'),('shadowland','Shadowland: Spider-Man','2010-11'),
    ('smvamp','Spider-Man vs. Vampires','2010-12'),('fearsm11','Fear Itself: Spider-Man #1–3','2011-07'),('eote','ASM: Ends of the Earth','2012-07'),
    ('mksm2013','Marvel Knights: Spider-Man #1–5','2013-12'),('whoami','ASM: Who Am I? #1–4','2014-05'),('familybiz','ASM: Family Business','2014-06'),
    ('smxm','Spider-Man and the X-Men #1–6','2014-12'),('rvows','Renew Your Vows #1–5','2015-06'),('spiderfly','ASM & Silk: The Spider(fly) Effect #1–4','2016-05'),
    ('cw2asm','Civil War II: ASM #1–4','2016-08'),('wakanda','ASM: Wakanda Forever','2018-06'),('typhoid','Typhoid Fever: Spider-Man','2018-12'),
    ('reptilian','Reptilian Rage','2019-06'),('symbsm','Symbiote Spider-Man #1–5','2019-06'),('realms','Spider-Man & the League of Realms #1–3','2019-07'),
    ('selfimprove','Sensational Spider-Man: Self-Improvement','2019-08'),('goingbig','ASM: Going Big','2019-09'),('fullcircle','ASM: Full Circle','2019-10'),
    ('dailybugle','ASM: The Daily Bugle #1–2','2020-01'),('symbkib','Symbiote Spider-Man: King in Black #1–5','2020-11'),
    ('snapshots','Marvels Snapshots: Spider-Man','2020-12'),('kibsm','King in Black: Spider-Man','2021-03'),('manthing','Curse of the Man-Thing','2021-04'),
    ('crossroads','Symbiote Spider-Man: Crossroads #1–5','2021-07'),('spinetingle','Spine-Tingling Spider-Man #0–4','2021-10'),
    ('dodssm','Death of Doctor Strange: Spider-Man','2021-12'),('darkhold','Darkhold: Spider-Man','2021-12'),('murderworld','Murderworld: Spider-Man','2022-12'),
    ('deadlyneigh','Deadly Neighborhood Spider-Man #1–5','2022-12'),('losthunt','The Lost Hunt #1–5','2023-01'),('unforgiven','Spider-Man: Unforgiven','2023-05'),
    ('webs24','Web of Spider-Man (2024)','2024-03'),('shadowgg','Shadow of the Green Goblin #1–4','2024-04'),('blacksuit','Black Suit & Blood #1–4','2024-08'),
    ('versity','Spider-Versity #1–5','2026-04')]:
    one(iid, label, date)
for iid, label, date, tip in [
    ('blue','Spider-Man: Blue #1–6','2002-07',T('Peter ricorda Gwen Stacy','Peter remembers Gwen Stacy')),
    ('evilmen','Black Cat: The Evil That Men Do #1–6','2002-08',T('Completata solo nel 2006','Only completed in 2006')),
    ('fallenson','Fallen Son: Spider-Man','2007-07',T('Dopo la morte di Capitan America','After the death of Captain America'))]:
    one(iid, label, date, tip=tip)
items['blue']['key'] = True
RETELL = T('Rilettura delle origini, fuori continuity', 'Retelling of the origin, outside continuity')
one('withgreatpower', 'With Great Power #1–5', '2008-03', tip=RETELL)
one('clonesaga09', 'Spider-Man: The Clone Saga #1–6', '2009-11',
    tip=T('La Saga del Clone come era stata pensata in origine, fuori continuity', 'The Clone Saga as originally planned, outside continuity'))
one('seasonone', 'Spider-Man: Season One', '2012-03', tip=RETELL)
for iid, label, date in [('sinsprelude','Sins Rising Prelude','2020-07'),('sinsnorman','The Sins of Norman Osborn','2020-09'),
                         ('kingsransom','Giant-Size ASM: King\'s Ransom','2021-05'),('chameleon','Giant-Size ASM: Chameleon Conspiracy','2021-08')]:
    one(iid, label, date, kind='ess')
series('cw', 'CW', 'misc', range(1, 8), [(1,'2006-05'),(7,'2007-01')], kind='ess', full='Civil War #{n}', keys=(1,))

# ---------------- eventi: ordine esatto ----------------
def ev_item(spec):
    """spec: id esistente oppure (id, label, kind, full)"""
    if isinstance(spec, str): return items.pop(spec)
    iid, label, kind, *rest = spec
    return dict(id=iid, n=label, s='misc', date=0, kind=kind, key=False, tip=None, full=rest[0] if rest else None, rot=None)
events = []
def event(name, date, specs, key_first=True):
    lst = [ev_item(s) for s in specs]
    for i, it in enumerate(lst):
        it['date'] = M(date); it['frac'] = -0.5 + i * 1e-4; it['rot'] = 0
        if not it.get('tip'): it['tip'] = name
    events.extend(lst)

event('The Other', '2005-10', ['fnsm1','mksm19','asm525','fnsm2','mksm20','asm526','fnsm3','mksm21','asm527','fnsm4','mksm22','asm528'])
for i in ('fnsm1','mksm19','fnsm2','mksm20','fnsm3','mksm21','fnsm4','mksm22'): pass
event('One More Day', '2007-11', ['asm544','fnsm24','sens06-41','asm545'])
op = 'opt'
event('Spider-Island', '2011-08', [('siinfested','Spider-Island: Infested',op),('sibugle','Spider-Island Daily Bugle',op),'asm665','asm666','asm667',
    ('sicd1','Spider-Island: Cloak & Dagger #1',op),('sidhkf1','Spider-Island: Deadly Hands of Kung Fu #1',op),'asm668',('sifoes','Spider-Island: Deadly Foes',op),
    ('sigirl1','Spider-Island: Amazing Spider-Girl #1',op),('sigirl2','Spider-Island: Amazing Spider-Girl #2',op),('venom6','Venom #6',op,'Venom (2011) #6'),
    ('sinyc','Spider-Island: I Love New York City',op),('sievil','Spider-Island: Emergence of Evil',op),'asm669',('sicd2','Spider-Island: Cloak & Dagger #2',op),
    ('sicd3','Spider-Island: Cloak & Dagger #3',op),('siavengers','Spider-Island: Avengers',op),('bp524','Black Panther #524',op),('herc7','Herc #7',op),('herc8','Herc #8',op),
    ('siwoman','Spider-Island: Spider-Woman',op),'asm670',('venom7','Venom #7',op,'Venom (2011) #7'),('sidhkf2','Spider-Island: Deadly Hands of Kung Fu #2',op),
    ('sidhkf3','Spider-Island: Deadly Hands of Kung Fu #3',op),('sihfh','Spider-Island: Heroes for Hire',op),'asm671',('venom8','Venom #8',op,'Venom (2011) #8'),
    'asm672',('sigirl3','Spider-Island: Amazing Spider-Girl #3',op),'asm673'])
E = 'ess'
event('Spider-Verse', '2014-07', ['a14-4','a14-5','a14-6',('ssm32','SSM 32',E,'Superior Spider-Man #32'),('esv1','Edge of Spider-Verse #1',op),('ssm33','SSM 33',E,'Superior Spider-Man #33'),
    ('esv2','Edge of Spider-Verse #2',op),('esv3','Edge of Spider-Verse #3',op),('esv4','Edge of Spider-Verse #4',op),'a14-7',('esv5','Edge of Spider-Verse #5',op),
    ('sm2099-5','Spider-Man 2099 #5',op),'a14-8','a14-9',('sv1','Spider-Verse #1',op),('svtu1','Spider-Verse Team-Up #1',op),'a14-10',('ss1','Scarlet Spiders #1',op),
    ('sw1','Spider-Woman #1',op),('sm2099-6','Spider-Man 2099 #6',op),'a14-11',('svtu2','Spider-Verse Team-Up #2',op),('ss2','Scarlet Spiders #2',op),('sw2','Spider-Woman #2',op),
    ('sv2','Spider-Verse #2',op),'a14-12',('sm2099-7','Spider-Man 2099 #7',op),('ss3','Scarlet Spiders #3',op),'a14-13',('sw3','Spider-Woman #3',op),
    ('svtu3','Spider-Verse Team-Up #3',op),('sm2099-8','Spider-Man 2099 #8',op),'a14-14',('sw4','Spider-Woman #4',op),'a14-15'])
items_cc = ['a15-19',('cc1','Clone Conspiracy #1',E),'a15-20',('cc2','Clone Conspiracy #2',E),'a15-21',('silk14','Silk #14',op),('cc3','Clone Conspiracy #3',E),'a15-22',
    ('silk15','Silk #15',op),('cc4','Clone Conspiracy #4',E),'a15-23',('silk16','Silk #16',op),('prowler1','Prowler #1',op),('prowler2','Prowler #2',op),('prowler3','Prowler #3',op),
    ('prowler4','Prowler #4',op),('cc5','Clone Conspiracy #5',E),'a15-24',('silk17','Silk #17',op),('prowler5','Prowler #5',op),('ccomega','Clone Conspiracy: Omega',E)]
event('Dead No More: The Clone Conspiracy', '2016-10', items_cc)
event('Venom Inc.', '2017-12', [('vincalpha','Venom Inc. Alpha',E),'asm792',('venom159','Venom #159',E),'asm793',('venom160','Venom #160',E),('vincomega','Venom Inc. Omega',E)])
event('Spider-Geddon', '2018-10', [('esg1','Edge of Spider-Geddon #1',op),('esg2','Edge of Spider-Geddon #2',op),('esg3','Edge of Spider-Geddon #3',op),('esg4','Edge of Spider-Geddon #4',op),
    ('sg0','Spider-Geddon #0',E),('supocto','Superior Octopus',op),('sg1','Spider-Geddon #1',E),('sg2','Spider-Geddon #2',E),
    ('ppss311','PPSS 311',E,'Peter Parker: The Spectacular Spider-Man #311'),('ppss312','PPSS 312',E,'Peter Parker: The Spectacular Spider-Man #312'),
    ('ghost1','Ghost-Spider #1',op),('sgirls1','Spider-Girls #1',op),('sforce1','Spider-Force #1',op),('vault1','Vault of Spiders #1',op),('sg3','Spider-Geddon #3',E),
    ('vault2','Vault of Spiders #2',op),('sforce2','Spider-Force #2',op),('sg4','Spider-Geddon #4',E),('ghost2','Ghost-Spider #2',op),('sgirls2','Spider-Girls #2',op),
    ('sforce3','Spider-Force #3',op),('ghost3','Ghost-Spider #3',op),('sgirls3','Spider-Girls #3',op),
    ('ppss313','PPSS 313',E,'Peter Parker: The Spectacular Spider-Man #313'),('sg5','Spider-Geddon #5',E)])
event('Hunted', '2019-03', ['a18-16','a18-16hu','a18-17','a18-18','a18-18hu','a18-19','a18-19hu','a18-20','a18-20hu','a18-21','a18-22','a18-23'])
event('Last Remains', '2020-10', [x for n in range(50, 55) for x in (f'a18-{n}', f'a18-{n}lr')] + ['a18-55'])
event('Sinister War', '2021-07', [('sw-1','Sinister War #1',E),'a18-71',('sw-2','Sinister War #2',E),('sw-3','Sinister War #3',E),'a18-72',('sw-4','Sinister War #4',E),'a18-73'])
event('Beyond', '2021-10', ['a18-75','a18-76','a18-77','a18-78','a18-78bey','a18-79','a18-80','a18-80bey','a18-81','a18-82','a18-83','a18-84','a18-85',
    ('devilsreignsm','Devil\'s Reign: Spider-Man',op),'a18-86','a18-87',('mjbcbeyond','Mary Jane & Black Cat: Beyond',op),'a18-88','a18-88bey',
    'a18-89','a18-90','a18-91','a18-92','a18-92bey','a18-93'])
event('End of the Spider-Verse', '2022-08', [(f'esv22-{n}', f'Edge of Spider-Verse #{n}', op, f'Edge of Spider-Verse (2022) #{n}') for n in range(1, 6)] +
      [(f'sm22-{n}', f"SM'22 {n}", E, f'Spider-Man (2022) #{n}') for n in range(1, 8)])
event('Dark Web', '2022-11', [('fcbd22','FCBD 2022: Spider-Man/Venom',op),('venom21-13','Venom #13',op,'Venom (2021) #13'),'a22-14',('darkweb1','Dark Web #1',E),'a22-15',
    ('dwxm1','Dark Web: X-Men #1',op),('gg2','Gold Goblin #2',op),('dwmm1','Dark Web: Ms. Marvel #1',op),('mjbc1','Mary Jane & Black Cat #1',op),'a22-16',
    ('dwxm2','Dark Web: X-Men #2',op),('venom21-14','Venom #14',op,'Venom (2021) #14'),('gg3','Gold Goblin #3',op),'a22-17',('dwmm2','Dark Web: Ms. Marvel #2',op),
    ('mjbc2','Mary Jane & Black Cat #2',op),('venom21-15','Venom #15',op,'Venom (2021) #15'),('dwxm3','Dark Web: X-Men #3',op),'a22-18',
    ('venom21-16','Venom #16',op,'Venom (2021) #16'),('dwfinale','Dark Web Finale',E)])
event('Gang War', '2023-11', [('gwfirst','Gang War: First Strike',E),('lcgw1','Luke Cage: Gang War #1',op),('mm12','Miles Morales #12',op),('swoman23-1','Spider-Woman #1',op),
    'a22-39',('lcgw2','Luke Cage: Gang War #2',op),('mm13','Miles Morales #13',op),('ddgw1','Daredevil: Gang War #1',op),'a22-40',('swoman23-2','Spider-Woman #2',op),
    ('mm14','Miles Morales #14',op),('dhkfgw1','Deadly Hands of Kung Fu: Gang War #1',op),'a22-41',('lcgw3','Luke Cage: Gang War #3',op),('ddgw2','Daredevil: Gang War #2',op),
    ('mm15','Miles Morales #15',op),'a22-42',('jackpot1','Jackpot #1',op),('swoman23-3','Spider-Woman #3',op),('dhkfgw2','Deadly Hands of Kung Fu: Gang War #2',op),
    ('ddgw3','Daredevil: Gang War #3',op),'a22-43',('mm16','Miles Morales #16',op),('dhkfgw3','Deadly Hands of Kung Fu: Gang War #3',op),('lcgw4','Luke Cage: Gang War #4',op),
    ('swoman23-4','Spider-Woman #4',op),('mm17','Miles Morales #17',op),('ddgw4','Daredevil: Gang War #4',op),'a22-44'])
event('Death Spiral', '2026-02', [('ds1','Death Spiral #1',E,'Amazing Spider-Man/Venom: Death Spiral #1'),'a25-23',('venom255','Venom #255',E),'a25-24','a25-25',
    ('venom256','Venom #256',E),'a25-26',('venom257','Venom #257',E),'a25-27',('dsbody','Death Spiral: Body Count',E,'Amazing Spider-Man/Venom: Death Spiral Body Count #1')])
EVENT_KEY = {'fnsm1','asm544','siinfested','a14-9','cc1','vincalpha','sg1','a18-16','a18-50','sw-1','a18-75','sm22-1','darkweb1','gwfirst','ds1'}
for it in events:
    if it['id'] in EVENT_KEY: it['key'] = True
    if it['s'] != 'asm' and it['kind'] is None: it['kind'] = 'ess'   # numeri delle altre serie dentro un crossover

# ---------------- coerenza serie/eventi ----------------
pool = list(items.values())
for it in pool + events:
    it['date'] = it['date'] if it['date'] else 0
for e in events:
    if not e.get('ser'): continue
    for it in pool:
        if it.get('ser') != e['ser'] or it['num'] is None: continue
        if it['num'] < e['num'] and it['date'] >= e['date']:
            it['date'] = e['date'] - 0.01; it['rot'] = -1
        elif it['num'] > e['num'] and it['date'] < e['date'] + 1:
            # dopo il blocco: stesso mese ma in coda
            if it['date'] < e['date']: it['date'] = e['date'] + 0.95
# ---------------- ordinamento ----------------
ROT = ['asm','misc','sm','spec','web','mtu','smu']
pool = list(items.values())
for it in pool:
    it['frac'] = (it['date'] % 1) if it['rot'] is None else (-0.9 if it['rot'] == -1 else 0.9)
    it['date'] = int(it['date'])
    it['r'] = it['rot'] if it['rot'] is not None else ROT.index(it['s'])
for it in events: it['r'] = 0
everything = sorted(pool + events, key=lambda it: (it['date'], it['frac'], it['r']))

def sl(lo, hi): return [it for it in everything if M(lo) <= it['date'] <= M(hi)]
GRULES = [(r'^(a99|a14|a15|a18|a22|a25)-','asm'),(r'^asm\d','asm'),(r'^ann','asm'),(r'^p9ann$','asm'),
    (r'^ssm24-','ssm24'),(r'^ssmtu','ssmtu'),(r'^ssmen','ssmen'),(r'^ssma','ssm'),(r'^ssm\d','ssm'),(r'^ppsm','ppsm'),(r'^ppss','ppss'),
    (r'^sp03-','sp03'),(r'^sens06','mksm'),(r'^mksm\d','mksm'),(r'^fnsm19-','fnsm19'),(r'^fnsm','fnsm'),(r'^mtu05-','mtu05'),(r'^mtu19-','mtu19'),
    (r'^avsm','avsm'),(r'^spidey\d','spidey'),(r'^smdp','smdp'),(r'^nssm','nssm'),(r'^savage\d','savage'),(r'^sm22-','sm22'),
    (r'^webs\d','webspin'),(r'^tw\d','tw'),(r'^smu04-','smu04'),(r'^smf\d','smf'),(r'^asmf','asmf'),(r'^web09-','web09'),(r'^sfoes','foes'),(r'^cw\d','events')]
def gfor(it):
    if it.get('g'): return it['g']
    for rx, g in GRULES:
        if re.match(rx, it['id']): return g
    return 'events'
def clean(lst):
    out = []
    for it in lst:
        d = {k: it[k] for k in ('id','n','s')}
        d['g'] = gfor(it)
        for k in ('kind','tip','full'):
            if it.get(k): d[k] = it[k]
        if it.get('key'): d['key'] = 1
        out.append(d)
    return out
data = json.load(open(os.path.join(S, 'fasi.json'), encoding='utf-8'))
for k in ('p7','p8','p9','p10','p11'): data.pop(k, None)
data.update({'p7': clean(sl('1999-01','2007-12')), 'p8': clean(sl('2008-01','2012-12')), 'p9': clean(sl('2013-01','2018-06')),
             'p10': clean(sl('2018-07','2025-03')), 'p11': clean(sl('2025-04','2099-12'))})
ids = [x['id'] for v in data.values() for x in v]
d = {i for i in ids if ids.count(i) > 1}; assert not d, d
json.dump(data, open(os.path.join(S, 'fasi.json'), 'w'), ensure_ascii=False)
print({k: len(v) for k, v in data.items()}, 'tot', len(ids))
def around(k, iid, a=-3, b=6):
    L = data[k]; i = [j for j, x in enumerate(L) if x['id'] == iid][0]
    print(k, ' | '.join(x['n'] for x in L[max(0, i + a):i + b]))
around('p7','fnsm1'); around('p7','asm544'); around('p8','asm700'); around('p9','ssm1',-2,4); around('p9','a14-1')
around('p10','a18-16'); around('p11','asm1000',-4,3)
