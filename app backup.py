from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Carregar o conjunto de dados de treinamento a partir de um arquivo CSV, excluindo as colunas 'ID' e 'Customer_ID'
df = pd.read_csv("train.csv", low_memory=False, usecols=lambda col: col not in ['ID', 'Customer_ID', 'Name', 'Age', 'SSN', 'Num_of_Loan'])

# Examinar os tipos de dados e encontrar a coluna problemática
print(df.dtypes)

# Converter a coluna 'Credit_Score' para números, ignorando erros
#df['Credit_Score'] = pd.to_numeric(df['Credit_Score'], errors='coerce')

# Separar as colunas de recursos (X) e a coluna alvo (y)
y_train = df['Credit_Score']
X_train = df.drop('Credit_Score', axis=1)

# Antes de treinar o modelo, converter colunas categóricas em variáveis dummy
categorical_cols = ['Month', 'Occupation', 'Type_of_Loan', 'Credit_Mix', 'Payment_Behaviour']
X_train_encoded = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True)

# Tratar 'Num_of_Loan' convertendo valores não numéricos para zero
if 'Num_of_Loan' in X_train_encoded.columns:
    X_train_encoded['Num_of_Loan'] = pd.to_numeric(X_train_encoded['Num_of_Loan'].astype(str).str.replace('_', '').str.replace(',', ''), errors='coerce').fillna(0)

# Tratar 'Num_of_Loan' convertendo valores não numéricos para zero
if 'Num_of_Delayed_Payment' in X_train_encoded.columns:
    X_train_encoded['Num_of_Delayed_Payment'] = pd.to_numeric(X_train_encoded['Num_of_Delayed_Payment'].astype(str).str.replace('_', '').str.replace(',', ''), errors='coerce').fillna(0)

# Converter todas as colunas para numérico, substituindo valores não numéricos por zero
X_train_encoded = X_train_encoded.apply(pd.to_numeric, errors='coerce').fillna(0)

# Tratar colunas com sublinhado no final
columns_with_underscore = ['Annual_Income', 'Num_of_Loan', 'Changed_Credit_Limit', 'Outstanding_Debt', 'Credit_History_Age', 'Amount_invested_monthly', 'Monthly_Balance', 'Credit_Score']

# Imprimir nome das colunas antes do processamento
print("Colunas antes do processamento:")
print(X_train_encoded.columns)

# Processar colunas com sublinhado no final
for col in columns_with_underscore:
    # Verificar se a coluna está presente no DataFrame
    if col in X_train_encoded.columns:
        X_train_encoded[col] = pd.to_numeric(X_train_encoded[col].astype(str).str.replace('_', '').str.replace(',', ''), errors='coerce')
        
# Verificar se a coluna 'Num_of_Loan' está presente antes de tentar modificá-la
if 'Num_of_Loan' in X_train_encoded.columns:
    X_train_encoded['Num_of_Loan'] = X_train_encoded['Num_of_Loan'].str.replace('_', '').astype(float, errors='coerce').fillna(0)

# Imprimir nome das colunas após o processamento
print("Colunas após o processamento:")
print(X_train_encoded.columns)

# Criar e treinar o modelo de árvore de decisão (treinamento ocorre aqui)
tree_model = DecisionTreeClassifier()
# Substituir NaNs em y_train por 0
y_train = y_train.fillna(0)

tree_model.fit(X_train_encoded, y_train)

# Lista de meses para criar variáveis dummy
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Lista de ocupações para criar variáveis dummy
occupations = ['Scientist', 'Teacher', 'Engineer', 'Entrepreneur', 'Developer', 'Lawyer', 'Media_Manager', 'Doctor', 'Journalist', 'Manager', 'Accountant', 'Musician', 'Mechanic', 'Writer', 'Architect']

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None  # Inicialize result como None

    if request.method == 'POST':
        try:
            # Obter dados do formulário
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
            Payment_Behaviour = request.form['Payment_Behaviour']
            selected_month = request.form['month']

            # Adicionar mensagens de depuração para imprimir entradas do usuário
            print(f"Occupation: {occupation}")
            print(f"Monthly_Inhand_Salary: {Monthly_Inhand_Salary}")
            print(f"Num_Bank_Accounts: {Num_Bank_Accounts}")
            print(f"Interest_Rate: {Interest_Rate}")
            # Adicionar mensagens de depuração para imprimir outros campos

            # Criar DataFrame com dados do usuário
            user_data = {
                'credit_mix': credit_mix,
                'Delay_from_due_date': Delay_from_due_date,
                'Interest_Rate': Interest_Rate,
                'Num_Credit_Inquiries': Num_Credit_Inquiries,
                'Num_Bank_Accounts': Num_Bank_Accounts,
                'Num_Credit_Card': Num_Credit_Card,
                'Total_EMI_per_month': Total_EMI_per_month,
                'Credit_Utilization_Ratio': Credit_Utilization_Ratio,
                'Monthly_Inhand_Salary': Monthly_Inhand_Salary,
                'Payment_of_Min_Amount': Payment_of_Min_Amount,
                'Payment_Behaviour': Payment_Behaviour,
                'month': selected_month,
                'occupation': occupation
            }

            # Adicionar variáveis dummy para meses e ocupações
            user_data.update({f'month_{month}': 1 if selected_month == month else 0 for month in months})
            user_data.update({f'occupation_{job}': 1 if occupation == job else 0 for job in occupations})

            # Criar DataFrame com dados do usuário
            user_df = pd.DataFrame(user_data, index=[0])

            # Converter as colunas 'month', 'occupation', 'credit_mix' e 'Payment_Behaviour' em variáveis dummy
            user_df = pd.get_dummies(user_df, columns=['credit_mix', 'Payment_Behaviour'], drop_first=True)

            # Fazer previsão usando o modelo de árvore de decisão
            prediction = tree_model.predict(user_df)

            # Adicionar mensagem de depuração para imprimir a previsão
            print(f"Prediction: {prediction}")

            # Exibir o resultado da classificação
            result = {'CreditClassification': prediction[0], 'OriginalCreditScore': y_train.iloc[75]}

        except ValueError as e:
            error_message = f"Erro: {str(e)}"
            result = {'CreditClassification': 'Erro de entrada', 'OriginalCreditScore': y_train.iloc[75]}
            return render_template('index.html', result=result, error_message=error_message)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
