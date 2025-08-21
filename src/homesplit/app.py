import streamlit as st
from datetime import date

from homesplit import db

# Initialize database and ensure table exists
db.init_db()

# Categories
CATEGORIES = [
    "Affitto",
    "Bolletta luce e gas",
    "Bolletta fibra",
    "Utenze",
    "Altro",
    "Rimborso",  # Special category for reimbursements
]

# Helper to cache list of people


@st.cache_data(ttl=60)
def get_people():
    return db.get_people()


def refresh_people_cache():
    get_people.clear()


def load_data():
    return db.get_all_expenses()


def add_expense(entry):
    db.add_expense(entry)


def calculate_balances(data):
    people = get_people()
    balances = {person: 0 for person in people}
    for exp in data:
        amount = float(exp["amount"])
        paid_by = exp["paid_by"]
        reimbursed_by = exp["reimbursed_by"]
        if exp.get("category") == "Rimborso":
            # For reimbursements, the reimburser pays the payee directly
            balances[paid_by] -= amount
            balances[reimbursed_by] += amount
        elif paid_by != reimbursed_by:
            # The person who paid is owed half, the other owes half
            balances[paid_by] += amount / 2
            balances[reimbursed_by] -= amount / 2
    return balances


def main():
    st.set_page_config(page_title="Gestione Spese di Casa", page_icon="💰", layout="wide")
    st.title("Gestione Spese di Casa")
    st.write("Dividi e gestisci le spese tra due persone, con categorie e rimborsi.")

    data = load_data()

    tabs = st.tabs([
        "Storico e Riepilogo",
        "Aggiungi Spesa",
        "Aggiungi Rimborso",
    ])

    with tabs[0]:
        st.header("Storico spese")
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("Nessuna spesa registrata.")

        st.header("Bilancio e riepilogo")
        balances = calculate_balances(data)
        for person, balance in balances.items():
            if balance > 0:
                st.success(f"{person} deve ricevere €{balance:.2f}")
            elif balance < 0:
                st.warning(f"{person} deve rimborsare €{-balance:.2f}")
            else:
                st.info(f"{person} è in pari.")

        st.subheader("Riepilogo per categoria")
        category_totals = {cat: 0 for cat in CATEGORIES}
        for exp in data:
            category_totals[exp["category"]] += float(exp["amount"])
        st.table([[cat, f"€{amt:.2f}"] for cat, amt in category_totals.items()])

    with tabs[1]:
        st.header("Aggiungi una spesa")
        with st.form("add_expense_form"):
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Categoria", CATEGORIES[:-1])  # Exclude 'Rimborso'
                people = get_people()
                paid_by = st.selectbox("Pagato da", people)
            with col2:
                people = get_people()
                reimbursed_by = st.selectbox("Rimborsato da", people, index=1)
                amount = st.number_input("Importo (€)", min_value=0.0, step=0.01, format="%.2f")
            description = st.text_input("Descrizione (opzionale)")
            expense_date = st.date_input("Data", value=date.today())
            submitted = st.form_submit_button("Aggiungi spesa")
            if submitted:
                if paid_by == reimbursed_by:
                    st.error("Le due persone devono essere diverse.")
                elif amount <= 0:
                    st.error("L'importo deve essere maggiore di zero.")
                else:
                    expense = {
                        "date": str(expense_date),
                        "category": category,
                        "paid_by": paid_by,
                        "reimbursed_by": reimbursed_by,
                        "amount": amount,
                        "description": description,
                    }
                    add_expense(expense)
                    st.success("Spesa aggiunta!")
                    st.rerun()

    with tabs[2]:
        st.header("Aggiungi un rimborso")
        with st.form("add_reimbursement_form"):
            col1, col2 = st.columns(2)
            with col1:
                people = get_people()
                reimbursed = st.selectbox("Chi riceve il rimborso?", people, key="reimbursed")
            with col2:
                people = get_people()
                reimburser = st.selectbox("Chi rimborsa?", people, key="reimburser", index=1)
                amount = st.number_input(
                    "Importo rimborso (€)", min_value=0.0, step=0.01, format="%.2f", key="reimb_amount"
                )
            description = st.text_input("Descrizione rimborso (opzionale)", key="reimb_desc")
            reimbursement_date = st.date_input("Data rimborso", value=date.today(), key="reimb_date")
            submitted_reimb = st.form_submit_button("Aggiungi rimborso")
            if submitted_reimb:
                if reimburser == reimbursed:
                    st.error("Le due persone devono essere diverse.")
                elif amount <= 0:
                    st.error("L'importo deve essere maggiore di zero.")
                else:
                    reimbursement = {
                        "date": str(reimbursement_date),
                        "category": "Rimborso",
                        "paid_by": reimburser,
                        "reimbursed_by": reimbursed,
                        "amount": amount,
                        "description": description,
                    }
                    add_expense(reimbursement)
                    st.success("Rimborso aggiunto!")
                    st.rerun()

# -------- Add Person Sidebar --------

with st.sidebar:
    st.header("Gestione Persone")
    new_person = st.text_input("Nuova persona", placeholder="Nome")
    if st.button("Aggiungi") and new_person:
        db.add_person(new_person.strip())
        st.success(f"{new_person} aggiunto/a.")
        refresh_people_cache()


if __name__ == "__main__":
    main()