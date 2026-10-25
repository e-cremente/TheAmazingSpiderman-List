# Spider-Man Letture

App web installabile (PWA) con l'ordine di lettura di Amazing Spider-Man. Funziona offline dopo la prima apertura e salva il progresso sul telefono.

## Contenuto

- `index.html` — l'app
- `manifest.webmanifest`, `sw.js` — installazione e funzionamento offline
- `icons/`, `fonts/` — icona e caratteri, tutti in locale

## Metterla sul telefono

Il telefono deve aprirla da un indirizzo HTTPS almeno una volta; poi resta installata e funziona senza rete.

### GitHub Pages (consigliato, gratis)

1. Crea un repository pubblico su GitHub (es. `spidey-letture`).
2. Carica il contenuto di questa cartella nella radice del repository.
3. Settings → Pages → Source: "Deploy from a branch", branch `main`, cartella `/ (root)`.
4. Dopo un minuto l'app è su `https://<tuo-utente>.github.io/spidey-letture/`.

### Installazione

- **Android (Chrome):** apri l'indirizzo → menu ⋮ → "Installa app" (o "Aggiungi a schermata Home").
- **iPhone (Safari):** apri l'indirizzo → Condividi → "Aggiungi alla schermata Home".

## Spostare il progresso

Nella pagina su claude.ai tocca **Copia backup**, poi nell'app sul telefono **Importa backup** e incolla il codice.

## Aggiornare la lista

Sostituisci `index.html` e cambia il nome della cache in `sw.js` (`spidey-v2` → `spidey-v3`), così il telefono scarica la versione nuova alla prossima apertura con connessione. Il progresso non si perde.
