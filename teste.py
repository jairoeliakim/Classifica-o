import pandas as pd
from nyoka import PMML44 as pml

# Carregar o modelo PMML

with open('saida.pmml', 'r') as file:
    pmml_str = file.read()

pmml_obj = pml.parse(pmml_str)

# Obter dados do usuário

data = {
    'Month': 12,
    'Occupation': 'Profissional',
    'm_credit_card': 1000,
    'Monthly_Inhand_Salary': 5000,
    'Num_Bank_Accounts': 2,
    'Num_Credit_Card': 1,
    'Interest_Rate': 10,
    'Delay_from_due_date': 0,
    'Num_Credit_Inquiries': 1,
    'Credit_Mix': 'Bom',
    'Credit_Utilization_Ratio': 20,
    'Payment_of_Min_Amount': True,
    'Total_EMI_per_month': 500,
    'Payment_Behaviour': 'Em dia'
}

# Converter valores categóricos para numéricos

label_encoder = LabelEncoder()
for field in data:
    if field in pmml_obj.MiningSchema.MiningField:
        label_encoder.fit(pmml_obj.MiningSchema.MiningField[field].apply(str))
        data[field] = label_encoder.transform([data[field]])[0]

# Criar DataFrame com dados do usuário

df = pd.DataFrame(data, index=[0])

# Fazer a previsão usando o modelo PMML

prediction = pmml_obj.predict(df)

# Exibir o resultado da classificação

print(prediction)