"""Fasi 2-6 (1971-1998): tutte le testate di Spider-Man alternate per mese di copertina, testi in IT/EN."""
import json, re, os
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))

def M(y, m): return y * 12 + (m - 1)
def T(it, en): return {'it': it, 'en': en}

# ---------- date di copertina ----------
def asm_date(n):
    if n <= 300: return M(1963,10) + (n - 5)
    special = {301:(1988,6),302:(1988,7),303:(1988,8),304:(1988,9),305:(1988,9),306:(1988,10),307:(1988,10),
        308:(1988,11),309:(1988,11),310:(1988,12),311:(1989,1),312:(1989,2),313:(1989,3),314:(1989,4),315:(1989,5),
        316:(1989,6),317:(1989,7),318:(1989,8),319:(1989,9),320:(1989,9),321:(1989,10),322:(1989,10),323:(1989,11),
        324:(1989,11),325:(1989,11),326:(1989,12),327:(1989,12),328:(1990,1),
        334:(1990,7),335:(1990,7),336:(1990,8),337:(1990,8),338:(1990,9),339:(1990,9),340:(1990,10),341:(1990,11),
        342:(1990,12),343:(1991,1),351:(1991,9),352:(1991,10),353:(1991,11),354:(1991,11),355:(1991,12),356:(1991,12),
        357:(1992,1),358:(1992,1),359:(1992,2),360:(1992,3),
        368:(1992,11),369:(1992,11),370:(1992,12),371:(1992,12),372:(1993,1),373:(1993,1),
        439:(1998,10),440:(1998,10),441:(1998,11)}
    if n in special: return M(*special[n])
    if 329 <= n <= 333: return M(1990,2) + (n - 329)
    if 344 <= n <= 350: return M(1991,2) + (n - 344)
    if 361 <= n <= 367: return M(1992,4) + (n - 361)
    if 374 <= n <= 393: return M(1993,2) + (n - 374)
    if 419 <= n <= 424: return M(1997,1) + (n - 419)
    if 425 <= n <= 438: return M(1997,8) + (n - 425)
    raise ValueError(n)

def spec_date(n):
    if n <= 154: return M(1976,12) + (n - 1)
    s = {155:(1989,9),156:(1989,10),157:(1989,10),158:(1989,11),159:(1989,12)}
    if n in s: return M(*s[n])
    if 160 <= n <= 216: return M(1990,1) + (n - 160)
    if 241 <= n <= 246: return M(1997,1) + (n - 241)
    if 247 <= n <= 261: return M(1997,8) + (n - 247)
    return {262: M(1998,10), 263: M(1998,11)}[n]

def mtu_date(n):
    early = {1:(1972,3),2:(1972,5),3:(1972,7),4:(1972,9),5:(1972,11),6:(1973,1),7:(1973,3)}
    return M(*early[n]) if n in early else M(1973,4) + (n - 8)

def web_date(n):
    if n <= 55: return M(1985,4) + (n - 1)
    s = {56:(1989,11),57:(1989,11),58:(1989,12),59:(1989,12)}
    return M(*s[n]) if n in s else M(1990,1) + (n - 60)

def sm_date(n):
    if n <= 50: return M(1990,8) + (n - 1)
    if 76 <= n <= 81: return M(1997,1) + (n - 76)
    if 82 <= n <= 95: return M(1997,8) + (n - 82)
    return {96: M(1998,10), 97: M(1998,10), 98: M(1998,11)}[n]

def sens_date(n):
    if 12 <= n <= 17: return M(1997,1) + (n - 12)
    if 18 <= n <= 31: return M(1997,8) + (n - 18)
    return {32: M(1998,10), 33: M(1998,11)}[n]

SMU = {1:(1993,5),2:(1993,8),3:(1993,11),4:(1994,2),5:(1994,5),6:(1994,8),
       15:(1997,2),16:(1997,5),17:(1997,8),18:(1997,11),19:(1998,2),20:(1998,5),21:(1998,8),22:(1998,11)}

items = []
def add(id, n, s, date, kind=None, key=False, tip=None, rot=None):
    items.append(dict(id=id, n=n, s=s, date=date, kind=kind, key=key, tip=tip, rot=rot))

# ---------- serie regolari ----------
KEY_ASM = {101,121,122,129,149,194,200,229,230,238,252,289,300,316,334,344,361,375,400,418,441}
for n in list(range(101, 394)) + list(range(419, 442)):
    add(f'asm{n}', f'#{n}', 'asm', asm_date(n), key=n in KEY_ASM)
add('asmm1', '#-1', 'asm', M(1997,7), tip=T('Flashback: Peter prima del morso del ragno', 'Flashback: Peter before the spider bite'))
for n in range(1, 151):
    add(f'mtu{n}', f'MTU {n}', 'mtu', mtu_date(n), key=n==1,
        tip=T('Il primo team-up, con la Torcia Umana', 'The first team-up, with the Human Torch') if n==1 else None)
SPEC_TIP = {1: T('Nasce la seconda serie mensile', 'The second monthly series begins'),
            107: T('Inizio de "La morte di Jean DeWolff" (#107–110)', 'Start of "The Death of Jean DeWolff" (#107–110)'),
            200: T('Morte di Harry Osborn', 'Death of Harry Osborn')}
for n in list(range(1, 217)) + list(range(241, 264)):
    add(f'spec{n}', f'SPEC {n}', 'spec', spec_date(n), key=n in (1,107,200), tip=SPEC_TIP.get(n))
add('specm1', 'SPEC -1', 'spec', M(1997,7))
for n in range(1, 117):
    add(f'web{n}', f'WEB {n}', 'web', web_date(n), key=n==1,
        tip=T('Il simbionte torna all\'attacco', 'The symbiote strikes back') if n==1 else None)
for n in list(range(1, 51)) + list(range(76, 99)):
    add(f'sm{n}', f'SM {n}', 'sm', sm_date(n), key=n==1,
        tip=T('La serie di Todd McFarlane', "Todd McFarlane's series") if n==1 else None)
add('smm1', 'SM -1', 'sm', M(1997,7))
for n,(y,m) in SMU.items(): add(f'smu{n}', f'SMU {n}', 'smu', M(y,m))
for n in range(12, 34): add(f'sens{n}', f'SENS {n}', 'sens', sens_date(n))
add('sensm1', 'SENS -1', 'sens', M(1997,7))
for n in range(1, 8): add(f'mtub{n}', f'MTU² {n}', 'mtu', M(1997,9) + (n - 1))
add('stu6', 'Spider-Man Team-Up #6', 'misc', M(1997,3), kind='opt')
add('stu7', 'Spider-Man Team-Up #7', 'misc', M(1997,6), kind='opt')

# ---------- annual ----------
ASM_ANN = {11:1977,13:1979,14:1980,15:1981,16:1982,17:1983,18:1984,19:1985,20:1986,22:1988,23:1989,
           24:1990,25:1991,26:1992,27:1993,28:1994}
for a,y in ASM_ANN.items(): add(f'ann{a}', f'Annual #{a}', 'asm', M(y,8), kind='ess', rot=9)
add('ann21', 'Annual #21', 'asm', M(1987,9), kind='ess', key=True, rot=9,
    tip=T('Il matrimonio di Peter e Mary Jane', 'The wedding of Peter and Mary Jane'))
for a,y in {1:1979,2:1980,3:1981,4:1984,5:1985,6:1986,7:1987,8:1988,9:1989,10:1990,11:1991,12:1992,13:1993,14:1994}.items():
    add(f'speca{a}', f'SPEC Ann. {a}', 'spec', M(y,8), rot=9)
for a,y in {1:1976,2:1979,3:1980,4:1981,5:1982,6:1983,7:1984}.items():
    add(f'mtua{a}', f'MTU Ann. {a}', 'mtu', M(y,8), rot=9)
for a in range(1, 11): add(f'weba{a}', f'WEB Ann. {a}', 'web', M(1984+a,8), rot=9)

# ---------- fuori serie ----------
add('gssh1', 'Giant-Size Super-Heroes #1', 'misc', M(1974,6), kind='opt', rot=9,
    tip=T('Contro Morbius e l\'Uomo Lupo', 'Against Morbius and Man-Wolf'))
add('gssm', 'Giant-Size Spider-Man #1–6', 'misc', M(1974,7), kind='opt', rot=9,
    tip=T('Team-up in formato gigante, 1974–75', 'Giant-size team-ups, 1974–75'))
add('ann10', 'Annual #10', 'asm', M(1976,8), kind='ess', rot=9)
add('p3sw', 'Secret Wars #1–12', 'misc', M(1984,5), kind='ess', rot=-1,
    tip=T('Il costume nero. Leggilo prima di ASM #252, uscito in anticipo sul finale',
          'The black costume. Read it before ASM #252, which came out before the ending'))
GN = T('Graphic novel', 'Graphic novel')
add('gnhooky', 'Hooky', 'misc', M(1986,1), kind='opt', rot=9, tip=T('Graphic novel del 1986', '1986 graphic novel'))
add('svw', 'Spider-Man vs. Wolverine', 'misc', M(1987,2), kind='ess', key=True, rot=9,
    tip=T('One-shot del 1987: la morte di Ned Leeds', '1987 one-shot: the death of Ned Leeds'))
for i,(iid,n,y) in enumerate([('gnparallel','Parallel Lives',1989),('gnspirits','Spirits of the Earth',1990),('fearitself','Fear Itself',1992)]):
    add(iid, n, 'misc', M(1987,11), kind='opt', rot=10+i,
        tip=T(f'Uscito nel {y}, collocato qui per la storia', f'Published in {y}, placed here by story'))
add('deadlyfoes', 'Deadly Foes of Spider-Man #1–4', 'misc', M(1991,5), kind='opt', rot=9)
add('dustydeath', 'The Way to Dusty Death', 'misc', M(1992,6), kind='opt', rot=9,
    tip=T('Graphic novel con il Dottor Strange', 'Graphic novel with Doctor Strange'))
add('soulhunter', 'Soul of the Hunter', 'misc', M(1992,8), kind='opt', rot=9,
    tip=T('Seguito dell\'ultima caccia di Kraven', "Sequel to Kraven's Last Hunt"))
add('trialvenom', 'The Trial of Venom', 'misc', M(1992,12), kind='opt', rot=9)
add('designer', 'Designer Genes', 'misc', M(1993,8), kind='opt', rot=9,
    tip=T('Con il Punitore e Sabretooth', 'With the Punisher and Sabretooth'))
add('lethalfoes', 'Lethal Foes of Spider-Man #1–4', 'misc', M(1993,9), kind='opt', rot=9)
add('mutantagenda', 'The Mutant Agenda #0–3', 'misc', M(1994,2), kind='opt', rot=9)
add('shadowgames', 'Shadowgames #1–3', 'misc', M(1994,5), kind='opt', rot=9, tip=T('Con X-Factor', 'With X-Factor'))
add('webofdoom', 'Web of Doom #1–3', 'misc', M(1994,8), kind='opt', rot=9)
add('arachnis', 'The Arachnis Project #1–6', 'misc', M(1994,8), kind='opt', rot=10)
add('hoblives', 'Hobgoblin Lives #1–3', 'misc', M(1997,1), kind='ess', key=True, rot=-1,
    tip=T('Si scopre chi era davvero Hobgoblin', 'The true identity of the Hobgoblin'))
add('tothedeath', 'To the Death', 'misc', M(1997,6), kind='opt', rot=9, tip=T('Con Kingpin', 'With the Kingpin'))
add('venomagenda', 'The Venom Agenda', 'misc', M(1998,1), kind='opt', rot=9)
add('mademen', 'Made Men', 'misc', M(1998,8), kind='opt', rot=9)

add('chapterone', 'Chapter One #0–12', 'misc', M(1998,12), kind='opt', rot=9,
    tip=T('Rilettura delle origini di John Byrne, fuori continuity', "John Byrne's retelling of the origin, outside continuity"))

# ---------- crossover: visibili anche in "Solo Amazing" ----------
def part(name_it, name_en, n): return T(f'{name_it}, parte {n}', f'{name_en}, part {n}')
CROSS = {}
for iid,n in (('web31',1),('spec131',3),('web32',4),('spec132',6)): CROSS[iid] = part("L'ultima caccia di Kraven","Kraven's Last Hunt",n)
for iid,n in (('smu1',1),('web101',2),('sm35',4),('spec201',5),('web102',6),('sm36',8),('spec202',9),('web103',10),
              ('sm37',12),('spec203',13),('smu2',14)): CROSS[iid] = part('Maximum Carnage','Maximum Carnage',n)
for iid in ('sm97','spec262'): CROSS[iid] = T('The Gathering of Five', 'The Gathering of Five')
for iid in ('sm98','spec263'): CROSS[iid] = T('The Final Chapter, fine del volume 1', 'The Final Chapter, end of volume 1')
for it in items:
    if it['id'] in CROSS:
        it['kind'] = 'ess'; it['tip'] = CROSS[it['id']]; it['key'] = it['id'] in ('web31','smu1')

# ---------- Saga del Clone: ordine esatto ----------
CLONE = """[Power and Responsibility] WEB #117, ASM #394, SM #51, SPEC #217, [The Lost Years] Lost Years #1, Lost Years #2, Lost Years #3, [The Exile Returns] WEB #118, SMU #7, SM #52, WEB #119, SM #53, [Back From The Edge] ASM #395, SPEC #218, ASM #396, SPEC #219, [Web of Life] WEB #120, SM #54, WEB #121, SM #55, [Web of Death] ASM #397, SPEC #220, ASM #398, SPEC #221, [Friends and Enemies] Friends and Enemies #1–4, Power of Terror #1–4, [Funeral For an Octopus] Funeral for an Octopus #1, Funeral for an Octopus #2, Funeral for an Octopus #3, SMU #8, [Smoke and Mirrors] WEB #122, ASM #399, SM #56, [The Clone Journal] Clone Journal #1, [Players and Pawns] SPEC #222, WEB #123, [Planet of the Symbiotes] Amazing Super Special #1, Spider-Man Super Special #1, Venom Super Special #1, Spectacular Super Special #1, Web Super Special #1, [The Parker Legacy] ASM #400, SM #57, SPEC #223, [The Mark of Kaine] WEB #124, ASM #401, SM #58, SPEC #224, SMU #9, WEB #125, [Crossfire] ASM #402, SM #59, SPEC #225, [The Trial of Peter Parker] WEB #126, ASM #403, SM #60, SPEC #226, [The Jackal Files] Jackal Files #1, [Maximum Clonage] New Warriors #61, Maximum Clonage Alpha #1, WEB #127, ASM #404, SM #61, SPEC #227, Maximum Clonage Omega #1, New Warriors #62, [Exiled] WEB #128, ASM #405, SM #62, SMU #10, [Time Bomb] SPEC #228, WEB #129, New Warriors #63, New Warriors #64, [The Greatest Responsibility] ASM #406, SM #63, Spider-Man Team-Up #1, SPEC #229, [After The Greatest Responsibility] Parker Years #1, New Warriors #65, Scarlet Spider Unlimited #1, [Virtual Mortality] Web of Scarlet Spider #1, Amazing Scarlet Spider #1, Scarlet Spider #1, Spectacular Scarlet Spider #1, [Cyberwar] Web of Scarlet Spider #2, Amazing Scarlet Spider #2, Green Goblin #3, Scarlet Spider #2, Spectacular Scarlet Spider #2, [After Cyberwar] New Warriors #66, SENS #0, ASM #407, SM #64, [Nightmare in Scarlet] Web of Scarlet Spider #3, New Warriors #67, Web of Scarlet Spider #4, [After Nightmare in Scarlet] SPEC #230, Family Plot #1, Family Plot #2, [Along Came a Spider] Venom: Along Came a Spider #1, Venom: Along Came a Spider #2, Venom: Along Came a Spider #3, Venom: Along Came a Spider #4, [Media Blizzard] SENS #1, ASM #408, SM #65, [The Final Adventure] Holiday Special 1995 #1, Final Adventure #1, Final Adventure #2, Final Adventure #3, Final Adventure #4, SMU #11, Spider-Man Team-Up #2, [The Return of Kaine] SPEC #231, SENS #2, ASM #409, SM #66, SPEC #232, [Web of Carnage] SENS #3, ASM #410, SM #67, SPEC #233, [Blood Brothers] SENS #4, ASM #411, SM #68, SPEC #234, SENS #5, ASM #412, [After Blood Brothers] SMU #12, SM #69, Spider-Man Team-Up #3, SENS #6, Legacy of Evil #1, [The Redemption] Redemption #1, Redemption #2, Redemption #3, Redemption #4, [After the Redemption] ASM #413, Daredevil #354, SM #70, SPEC #235, SPEC #236, SENS #7, ASM #414, SM #71, SPEC #237, SMU #13, Spider-Man Team-Up #4, SENS #8, [Onslaught] ASM #415, SM #72, [After Onslaught] SENS #9, SENS #10, ASM #416, SPEC #238, SPEC #239, Annual '96 #0, SM #73, SM #74, ASM #417, SMU #14, Spider-Man Team-Up #5, [Revelations] SPEC #240, SENS #11, ASM #418, SM #75, [Loose ends] Osborn Journal #1, Dead Man's Hand #1, 101 Ways to End the Clone Saga #1"""
SERIES = {'ASM':'asm','SPEC':'spec','WEB':'web','SM':'sm','SMU':'smu','SENS':'sens'}
CORE_X = {'Maximum Clonage Alpha','Maximum Clonage Omega','Web of Scarlet Spider','Amazing Scarlet Spider',
          'Scarlet Spider','Spectacular Scarlet Spider','Scarlet Spider Unlimited'}
clone, arc, seen = [], None, set()
for tok in re.split(r',\s*', CLONE):
    tok = tok.strip()
    m = re.match(r'\[(.+?)\]\s*(.*)', tok)
    if m: arc, tok = m.group(1), m.group(2)
    name, num = tok.rsplit(' #', 1)
    if name in SERIES:
        s = SERIES[name]; iid = f'{s}{num}'
        label = f'#{num}' if s == 'asm' else f'{name} {num}'
        kind = None if s == 'asm' else 'ess'
    elif name == "Annual '96":
        s, iid, label, kind = 'asm', 'ann96', "Annual '96", 'ess'
    else:
        slug = re.sub(r'[^a-z0-9]+', '', name.lower())
        s = 'scar' if 'Scarlet' in name else 'misc'
        iid = f'{slug}{re.sub(r"[^0-9]", "", num)}'
        label = f'{name} #{num}'
        if name in ('New Warriors','Daredevil','Green Goblin'): label = f'{name} {num}'
        if name.endswith('1995'): label = name
        if name.startswith('101 Ways'): label = '101 Ways #1'
        kind = 'ess' if name in CORE_X else 'opt'
    if iid in seen: continue
    seen.add(iid)
    clone.append(dict(id=iid, n=label, s=s, kind=kind, key=iid in ('web117','asm400','spec240','asm418'), tip=arc))
CLONE_TIP = {'web117': T('Power and Responsibility: torna Ben Reilly', 'Power and Responsibility: Ben Reilly returns'),
             'asm400': T('The Parker Legacy: la morte di zia May', 'The Parker Legacy: the death of Aunt May'),
             'asm418': T('Revelations: fine della Saga del Clone', 'Revelations: the end of the Clone Saga')}
for it in clone:
    if it['id'] in CLONE_TIP: it['tip'] = CLONE_TIP[it['id']]
    elif it['id'] in ('friendsandenemies14','powerofterror14','legacyofevil1'): it['tip'] = None

# ---------- ordinamento ----------
def rot(it):
    if it['rot'] is not None: return it['rot']
    d = it['date']
    if d >= M(1997,1): order = ['sens','asm','sm','spec','mtu','smu','misc']
    elif d >= M(1985,4): order = ['web','asm','sm','spec','mtu','smu','misc']
    else: order = ['asm','spec','mtu','misc']
    return order.index(it['s'])
groups = defaultdict(list)
for it in items:
    if it['rot'] is None: groups[(it['s'], it['date'])].append(it)
for g in groups.values():
    g.sort(key=lambda x: -1 if '-1' in x['n'] else int(re.sub(r'\D', '', x['n']) or 0))
    for i, it in enumerate(g): it['frac'] = i / len(g)
for it in items: it.setdefault('frac', 0 if it['rot'] is None else (-1 if it['rot'] < 0 else 0.99))
items.sort(key=lambda it: (it['date'], it['frac'], rot(it)))

def sl(lo, hi): return [it for it in items if lo <= it['date'] <= hi]
def gfor(it):
    s, iid = it['s'], it['id']
    simple = {'asm':'asm','spec':'spec76','web':'web85','sm':'sm90','smu':'smu93','sens':'sens96','scar':'scarlet'}
    if s in simple: return simple[s]
    if s == 'mtu': return 'mtu97' if iid.startswith('mtub') else 'mtu72'
    if iid == 'p3sw': return 'events'
    if iid.startswith(('stu','spidermanteamup')): return 'stu95'
    if iid.startswith(('newwarriors','greengoblin','daredevil','venomalongcameaspider')): return 'events'
    return 'minis'
def clean(lst):
    out = []
    for it in lst:
        d = {k: it[k] for k in ('id','n','s')}
        d['g'] = gfor(it)
        if it.get('kind'): d['kind'] = it['kind']
        if it.get('key'): d['key'] = 1
        if it.get('tip'): d['tip'] = it['tip']
        out.append(d)
    return out
data = {'p2': clean(sl(M(1971,10), M(1980,1))), 'p3': clean(sl(M(1980,2), M(1988,5))),
        'p4': clean(sl(M(1988,6), M(1994,9))), 'p5': clean(clone), 'p6': clean(sl(M(1997,1), M(1998,12)))}
ids = [x['id'] for v in data.values() for x in v]
dups = {i for i in ids if ids.count(i) > 1}
assert not dups, dups
json.dump(data, open(os.path.join(HERE, 'fasi.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print({k: len(v) for k, v in data.items()})
def show(k, a, b): print(' | '.join(x['n'] for x in data[k][a:b]))
def around(k, iid, a=-4, b=5):
    i = [j for j,x in enumerate(data[k]) if x['id']==iid][0]; show(k, i+a, i+b)
around('p3','gnhooky'); around('p3','svw'); around('p3','gnparallel',-4,6); around('p5','friendsandenemies14',-2,4)
around('p6','hoblives',-2,4); around('p6','mtub1',-2,4)
