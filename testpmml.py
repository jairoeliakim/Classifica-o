import pandas as pd
import os

from nyoka import PMML44 as pml
from sklearn.preprocessing import LabelEncoder

# Carregar o modelo PMML
pmml_path = os.path.abspath('rh.pmml')
with open(pmml_path, 'r') as file:
    pmml_str = file.read()
pmml_obj = pml.parse(pmml_str)

# Dados de exemplo para teste
m_credit_card = 1000.0
credit_mix = 'Good'
delay = 5.0
interest = 0.05
month = 'January'

# Converter valores categóricos para numéricos
label_encoder = LabelEncoder()
user_data = {
    'Month': month,
    'Occupation': '_______',
    'Monthly_Inhand_Salary': m_credit_card,
    'Num_Bank_Accounts': 0.0,
    'Num_Credit_Card': 0.0,
    'Interest_Rate': interest,
    'Delay_from_due_date': delay,
    'Num_Credit_Inquiries': 0.0,
    'Credit_Mix': credit_mix,
    'Credit_Utilization_Ratio': 0.0,
    'Payment_of_Min_Amount': 'NM',
    'Total_EMI_per_month': 0.0,
    'Payment_Behaviour': 'High_spent_Small_value_payments'
}

for field in user_data:
    if field in pmml_obj.MiningSchema.MiningField:
        label_encoder.fit(pmml_obj.MiningSchema.MiningField[field].apply(str))
        user_data[field] = label_encoder.transform([user_data[field]])[0]
    else:
        print(f"Campo {field} não encontrado no esquema de mineração.")

# Criar DataFrame com dados do usuário
user_df = pd.DataFrame(user_data, index=[0])

# Fazer a previsão usando o modelo PMML
prediction = pmml_obj.predict(user_df)

# Exibir o resultado da classificação
result = prediction.to_dict(orient='records')[0]
print(result)
