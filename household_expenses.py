import streamlit as st
import json
import os
from datetime import date

# File to persist data
DATA_FILE = 'expenses_data.json'

# Categories
CATEGORIES = [
    'Affitto',
    'Bolletta luce e gas',
    'Bolletta fibra',
    'Utenze',
    'Altro',
    'Rimborso'  # Special category for reimbursements
]

# People
PEOPLE = ['Maria', 'Andrea']

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_expense(data, expense):
    data.append(expense)
    save_data(data)

def calculate_balances(data):
    balances = {person: 0 for person in PEOPLE}
    for exp in data:
        amount = float(exp['amount'])
        paid_by = exp['paid_by']
        reimbursed_by = exp['reimbursed_by']
        if exp.get('category') == 'Rimborso':
            # For reimbursements, the reimburser pays the payee directly
            balances[paid_by] -= amount
            balances[reimbursed_by] += amount
        elif paid_by != reimbursed_by:
            # The person who paid is owed half, the other owes half
            balances[paid_by] += amount / 2
            balances[reimbursed_by] -= amount / 2
    return balances

def main():
    st.title('Gestione Spese di Casa')
    st.write('Dividi e gestisci le spese tra due persone, con categorie e rimborsi.')

    data = load_data()

    tabs = st.tabs([
        'Storico e Riepilogo',
        'Aggiungi Spesa',
        'Aggiungi Rimborso'
    ])

    with tabs[0]:
        st.header('Storico spese')
        if data:
            st.dataframe(data)
        else:
            st.info('Nessuna spesa registrata.')

        st.header('Bilancio e riepilogo')
        balances = calculate_balances(data)
        for person, balance in balances.items():
            if balance > 0:
                st.success(f"{person} deve ricevere €{balance:.2f}")
            elif balance < 0:
                st.warning(f"{person} deve rimborsare €{-balance:.2f}")
            else:
                st.info(f"{person} è in pari.")

        st.subheader('Riepilogo per categoria')
        category_totals = {cat: 0 for cat in CATEGORIES}
        for exp in data:
            category_totals[exp['category']] += float(exp['amount'])
        st.table([[cat, f"€{amt:.2f}"] for cat, amt in category_totals.items()])

    with tabs[1]:
        st.header('Aggiungi una spesa')
        with st.form('add_expense_form'):
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox('Categoria', CATEGORIES[:-1])  # Exclude 'Rimborso'
                paid_by = st.selectbox('Pagato da', PEOPLE)
            with col2:
                reimbursed_by = st.selectbox('Rimborsato da', PEOPLE, index=1)
                amount = st.number_input('Importo (€)', min_value=0.0, step=0.01, format='%.2f')
            description = st.text_input('Descrizione (opzionale)')
            expense_date = st.date_input('Data', value=date.today())
            submitted = st.form_submit_button('Aggiungi spesa')
            if submitted:
                if paid_by == reimbursed_by:
                    st.error('Le due persone devono essere diverse.')
                elif amount <= 0:
                    st.error('L\'importo deve essere maggiore di zero.')
                else:
                    expense = {
                        'date': str(expense_date),
                        'category': category,
                        'paid_by': paid_by,
                        'reimbursed_by': reimbursed_by,
                        'amount': amount,
                        'description': description
                    }
                    add_expense(data, expense)
                    st.success('Spesa aggiunta!')
                    st.rerun()

    with tabs[2]:
        st.header('Aggiungi un rimborso')
        with st.form('add_reimbursement_form'):
            col1, col2 = st.columns(2)
            with col1:
                reimbursed = st.selectbox('Chi riceve il rimborso?', PEOPLE, key='reimbursed')
            with col2:
                reimburser = st.selectbox('Chi rimborsa?', PEOPLE, key='reimburser', index=1)
                amount = st.number_input('Importo rimborso (€)', min_value=0.0, step=0.01, format='%.2f', key='reimb_amount')
            description = st.text_input('Descrizione rimborso (opzionale)', key='reimb_desc')
            reimbursement_date = st.date_input('Data rimborso', value=date.today(), key='reimb_date')
            submitted_reimb = st.form_submit_button('Aggiungi rimborso')
            if submitted_reimb:
                if reimburser == reimbursed:
                    st.error('Le due persone devono essere diverse.')
                elif amount <= 0:
                    st.error('L\'importo deve essere maggiore di zero.')
                else:
                    reimbursement = {
                        'date': str(reimbursement_date),
                        'category': 'Rimborso',
                        'paid_by': reimburser,
                        'reimbursed_by': reimbursed,
                        'amount': amount,
                        'description': description
                    }
                    add_expense(data, reimbursement)
                    st.success('Rimborso aggiunto!')
                    st.rerun()

if __name__ == '__main__':
    main()