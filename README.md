# Gestione Spese di Casa

Questo è un piccolo progetto Streamlit per gestire le spese di casa tra due persone, con suddivisione per categoria e gestione dei rimborsi.

## Funzionalità
- Aggiunta di spese per categoria (Affitto, Bolletta luce e gas, Bolletta fibra, Utenze, Altro)
- Selezione di chi ha pagato e chi deve rimborsare
- Storico delle spese
- Bilancio e riepilogo per persona e per categoria
- Persistenza dei dati su file locale (`expenses_data.json`)

## Requisiti
- Python 3.8+
- [Streamlit](https://streamlit.io/)

## Installazione

1. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

2. Avvia l'applicazione Streamlit:
   ```bash
   streamlit run household_expenses.py
   ```

## Estensioni
- Puoi aggiungere nuove categorie modificando la lista `CATEGORIES` nel file `household_expenses.py`.
- Per aggiungere nuove persone, modifica la lista `PEOPLE`.
- I dati sono salvati in `expenses_data.json` nella stessa cartella.

## Note
- L'app salva i dati localmente. Per backup o condivisione, copia il file `expenses_data.json`.