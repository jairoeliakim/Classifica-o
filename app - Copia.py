from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obter dados do formulário
        month = request.form['month']
        occupation = request.form['occupation']
        Monthly_Inhand_Salary = float(request.form['Monthly_Inhand_Salary'])
        Num_Bank_Accounts = float(request.form['Num_Bank_Accounts'])
        Interest_Rate = float(request.form['Interest_Rate'])
        Delay_from_due_date = float(request.form['Delay_from_due_date'])
        Num_Credit_Inquiries = float(request.form['Num_Credit_Inquiries'])
        credit_mix = request.form['credit_mix']
        Credit_Utilization_Ratio = float(request.form['Credit_Utilization_Ratio'])
        Num_Credit_Card = float(request.form['Num_Credit_Card'])
        Payment_of_Min_Amount = request.form['Payment_of_Min_Amount']
        Total_EMI_per_month = float(request.form['Total_EMI_per_month'])
        m_credit_card = float(request.form['m_credit_card'])
        Payment_Behaviour = request.form['Payment_Behaviour']
        Credit_Score = request.form['Credit_Score']

        # Criar DataFrame com dados do usuário
        user_data = {
            'Month': month,
            'Occupation': occupation,
            'Monthly_Inhand_Salary': Monthly_Inhand_Salary,
            'Num_Bank_Accounts': Num_Bank_Accounts,
            'Num_Credit_Card': Num_Credit_Card,
            'Interest_Rate': Interest_Rate,
            'Delay_from_due_date': Delay_from_due_date,
            'Num_Credit_Inquiries': Num_Credit_Inquiries,
            'Credit_Mix': credit_mix,
            'm_credit_card': m_credit_card,
            'Credit_Utilization_Ratio': Credit_Utilization_Ratio,
            'Payment_of_Min_Amount': Payment_of_Min_Amount,
            'Total_EMI_per_month': Total_EMI_per_month,
            'Payment_Behaviour': Payment_Behaviour,
            'Credit_Score': Credit_Score
        }

        # Criar DataFrame com dados do usuário
        user_df = pd.DataFrame(user_data, index=[0])

        # Aplicar funções de classificação
        user_df['CreditClassification'] = user_df.apply(classify_credit, axis=1)
        user_df['DelayClassification'] = user_df.apply(classify_delay, axis=1)
        user_df['CombinedClassification'] = user_df.apply(classify_combined, axis=1)

        # Exibir o resultado da classificação
        result = user_df[['CreditClassification', 'DelayClassification', 'CombinedClassification']].to_dict(orient='records')[0]
        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

def classify_credit(row):
    # Adicione sua lógica de classificação adicional aqui, se necessário
    if row['m_credit_card'] <= 1.828 or row['CreditMix'] <= 1.828:
        return 'padrão'
    elif 1.828 < row['m_credit_card'] >= 5.579 or 1.828 < row['CreditMix'] >= 5.579:
        return 'bom'
    else:
        return 'ruim'

def classify_delay(row):
    # Adicione sua lógica de classificação adicional aqui, se necessário
    if 1.223 <= row['Delay'] <= 1.504 or 1.504 <= row['Delay'] <= 1.828:
        return 'padrão'
    elif 1.504 <= row['Delay'] <= 1.828 or 1.828 <= row['Delay'] <= 2.151:
        return 'ruim'
    else:
        return 'bom'

def classify_combined(row):
    # Adicione sua lógica de classificação combinada adicional aqui, se necessário
    if 1.223 <= row['Delay'] <= 1.504 and row['Interest'] >= 0 and row['m_credit_card'] < row['Delay']:
        return 'Bom'
    elif 1.504 <= row['Delay'] <= 1.828 and row['Interest'] >= 0 and row['m_credit_card'] <= row['Delay']:
        return 'Padrão'
    elif row['Delay'] > 1.828 and row['Interest'] >= 0 and row['m_credit_card'] >= row['Delay']:
        return 'Ruim'
    else:
        return 'Not Classified'

if __name__ == '__main__':
    app.run(debug=True)
