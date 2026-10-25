# Spider-Man Letture

App web installabile (PWA) con l'ordine di lettura completo di Spider-Man, da Amazing Fantasy #15 a oggi, in italiano e inglese. Funziona offline dopo la prima apertura e salva il progresso sul telefono.

Indirizzo: https://e-cremente.github.io/TheAmazingSpiderman-List/

## Contenuto

- `index.html`, `manifest.webmanifest`, `sw.js`: l'app, **generata** da `sorgenti/aggiorna.py`. Non va modificata a mano.
- `icons/`, `fonts/`: icona e caratteri, tutti in locale.
- `sorgenti/`: dati, generatori e interfaccia. Come aggiornare la lista è spiegato in `sorgenti/ISTRUZIONI.md`.

## Installazione sul telefono

- **Android (Chrome):** apri l'indirizzo, poi menu ⋮ → "Installa app".
- **iPhone (Safari):** apri l'indirizzo, poi Condividi → "Aggiungi alla schermata Home".

Gli aggiornamenti arrivano da soli: apri l'app con la connessione attiva, chiudila e riaprila. Il progresso non si perde.

## Spostare il progresso

Su un dispositivo tocca **Copia backup**, sull'altro **Importa backup** e incolla il codice.
