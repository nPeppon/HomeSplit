# Gestione Spese di Casa

Applicazione **Streamlit** per gestire e suddividere le spese domestiche in maniera semplice.
Da oggi i dati non sono più salvati in un file JSON, ma in un database **PostgreSQL** versionato con **Alembic**.

---

## Funzionalità principali
- Aggiunta di spese per categoria (Affitto, Utenze, ecc.)
- Aggiunta di **nuove persone dinamicamente** dal pannello laterale
- Storico delle spese con riepilogo per persona e per categoria
- Bilancio in tempo reale di chi deve a chi
- Schema database gestito da _migrations_ Alembic (nessuna DDL hard-coded nel codice)

---

## Avvio rapido con Docker Compose
1. Spostati nella cartella del progetto:
   ```bash
   cd ~/HomeSplit
   ```
2. Costruisci le immagini, avvia Postgres, applica le migration ed esegui l'app:
   ```bash
   docker compose --profile migrate up -d --build
   ```
3. Apri il browser su <http://localhost:8502> (o la porta configurata in `STREAMLIT_PORT`).

### Variabili d'ambiente utili
Puoi creare un file `.env` accanto a `compose.yaml` per sovrascrivere i valori di default.

| Variabile | Default | Descrizione |
|-----------|---------|-------------|
| `PGUSER` | homesplit | utente Postgres |
| `PGPASSWORD` | homesplit | password Postgres |
| `PGDATABASE` | homesplit | database Postgres |
| `PGPORT` | 5434 | porta host esposta |
| `PGDATA_PATH` | ../postgres/HomeSplit/pgdata | volume dati |
| `STREAMLIT_PORT` | 8502 | porta host per l'interfaccia web |
| `DATABASE_URL` | postgresql://... | stringa connessione, se vuoi personalizzarla completamente |

---

## Sviluppo locale (senza Docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]     # oppure `pip install -e .` se non hai extras
# export DATABASE_URL="postgresql://user:pwd@127.0.0.1:5432/homesplit"
alembic upgrade head      # applica lo schema
streamlit run -m homesplit.app
```

---

## Gestione migrazioni Alembic
Creare una nuova migration dopo aver modificato lo schema (SQL o SQLAlchemy):
```bash
alembic revision --autogenerate -m "aggiungi colonna created_at"
```

Applicare le migrazioni:
```bash
alembic upgrade head
```

Le versioni sono salvate in `migrations/versions/` e vengono eseguite automaticamente dal
servizio `migrations` del `docker compose` (profilo `migrate`).

---

## Struttura del progetto
```
HomeSplit/
├─ src/homesplit/        # codice applicativo
│   ├─ app.py            # interfaccia Streamlit
│   └─ db.py             # helper DB (solo query, niente DDL)
├─ migrations/           # migrazioni Alembic
│   ├─ env.py
│   └─ versions/
├─ compose.yaml          # orchestrazione app + db (+ migrations)
├─ Dockerfile            # build immagine applicazione
├─ pyproject.toml        # metadati e dipendenze
└─ README.md             # questo file
```

Buon tracking delle spese! 💸