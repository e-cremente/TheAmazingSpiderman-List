# Come aggiornare la lista

Questa cartella contiene tutto quello che serve per rigenerare la lista. L'app nella radice del repository (`index.html`, `sw.js`, `manifest.webmanifest`) **non va modificata a mano**: si ricostruisce da qui.

## File

| File | Cosa contiene |
|---|---|
| `genera_1971_1998.py` | Fasi 2–6: tutte le testate dal 1971 al 1998, alternate per mese di copertina, più la Saga del Clone in ordine esatto |
| `genera_1999_oggi.py` | Fasi 7–11: tutte le testate dal 1999 a oggi, alternate per mese di uscita, più gli eventi in ordine esatto |
| `modello.html` | Interfaccia, testi IT/EN, fasi 0–1 scritte a mano, nomi delle serie per il menu "Vista" |
| `aggiorna.py` | Esegue i due generatori, unisce tutto, crea `pagina-claude.html` e ricostruisce l'app nella radice |
| `fasi.json`, `pagina-claude.html` | Risultati generati, da non modificare a mano |
| `icona.py` | Disegna le icone dell'app |

## Procedura

1. Modifica i dati (vedi sotto).
2. Esegui `python3 sorgenti/aggiorna.py`. Si ferma con un errore se trova id duplicati.
3. Fai commit e push: GitHub Pages pubblica l'app e il telefono la scarica alla prima apertura con connessione. Il nome della cache cambia da solo.
4. Ripubblica `sorgenti/pagina-claude.html` sulla pagina di Claude: https://claude.ai/artifact/4wdGWbj7B2PbZSJKnNd9Vs

## Aggiungere uscite in `genera_1999_oggi.py`

- **Nuovi numeri di Amazing.** Dopo il vol. 7 #35 la serie è passata alla numerazione storica (#1000, #1001…). Aggiungi i nuovi con `add('asm1002', '#1002', 'asm', M('2026-11'))`, oppure con `asm_legacy(1002, N, [(1002,'AAAA-MM'), (N,'AAAA-MM')])` per più numeri insieme.
- **Altri numeri di una serie esistente.** Allunga il `range(...)` della sua chiamata `series(...)` e aggiungi un'ancora `(numero, 'AAAA-MM')` per l'ultimo.
- **Nuova serie regolare di Peter Parker.** Aggiungi `series('prefisso', 'SIGLA', colore, range(1, N+1), [(1,'AAAA-MM'), (N,'AAAA-MM')])`. Poi:
  - in `GRULES` aggiungi la regola che assegna gli id alla sua pagina;
  - in `modello.html` aggiungi la sigla a `PREFIX` e il nome a `SERIES_NAMES`.
- **Miniserie, one-shot, graphic novel.** Usa una tessera unica: `one('id', 'Titolo #1–5', 'AAAA-MM', tip=T('nota IT', 'note EN'))`. Finiscono nella pagina "Miniserie, speciali e graphic novel".
- **Evento o crossover.** Usa `event('Nome', 'AAAA-MM', [...])` con l'ordine di lettura esatto. Nell'elenco puoi mettere:
  - gli id già esistenti;
  - tuple `('id', 'Etichetta', 'ess' | 'opt', 'Nome completo')` per gli albi nuovi.

## Regole

- **Date.** Fino al 1998 si usa il mese di copertina, dal 1999 il mese di uscita in edicola.
- **Id.** Ogni id è unico e **non va mai cambiato**: il progresso salvato sui telefoni usa gli id.
- **Tipi di albo.**
  - `opt` (tratteggiato): facoltativo, cioè antologie, miniserie, tie-in con altri eroi, riletture fuori continuity.
  - `ess`: compare anche nella vista "Amazing + crossover".
  - Superior Spider-Man (2013) è `ess` perché prende il posto di Amazing.
- **Esclusi:** ristampe, universi alternativi (Ultimate, Life Story, Reign…), altri Spider-eroi (Miles Morales, Spider-Gwen, Venom…), fumetti per bambini, crossover con altri editori, albi promozionali.
- **Colori.** `asm` bianco, `spec` verde acqua, `mtu` ocra, `web` viola, `sm` verde, `misc`/`smu`/`sens`/`scar`/`ut` grigio-blu.
