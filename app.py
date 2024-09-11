from flask import Flask, render_template, request

app = Flask(__name__)

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

            # Lógica de tratativa para classificação
            # validação de crédito sem definição
            if credit_mix == '_':
                if Interest_Rate > 0.0034:
                    result = "Poor"
                elif Interest_Rate <= 0.0034:
                    if Payment_of_Min_Amount == "no":
                        if Num_Credit_Card <= 0.0017:
                            result = "Good"
                        else:
                            result = "Standard"
                    else:
                        result = "Standard"

            elif occupation in ["Lawyer", "Architect", "Accountant", "Scientist"] and Payment_Behaviour in ["Low_spent_Large_value_payments", "High_spent_Large_value_payments"]:
                result = "Standard"
            elif occupation in ["Developer", "Doctor", "Entrepreneur", "Engineer", "Writer", "Media_Manager", "Manager", "Journalist"] and Payment_Behaviour == "High_spent_Small_value":
                if Credit_Utilization_Ratio <= 0.6535:
                    result = "Standard"
                else:
                    result = "Good"
            elif occupation in ["Mechanic", "Musician", "Teacher"]:
                result = "Standard"
                if Interest_Rate > 0.0034:
                    result = "Poor"
                elif Interest_Rate <= 0.0034:
                    if Delay_from_due_date <= 32.5:
                        result = "Standard"
                    elif Delay_from_due_date > 32.5:
                        result = "Poor"
                    elif Interest_Rate <= 0.002 and Num_Credit_Card > 0.0017 and Delay_from_due_date <= 16.5 and Num_Bank_Accounts > 0.0036:
                        result = "Standard"
                    elif Interest_Rate <= 0.002 and Num_Credit_Card <= 0.0017:
                        if Payment_Behaviour in ['High_spent_Small_value_payments', 'Low_spent_Medium_value_payments', '!@9#%8', 'Low_spent_Small_value_payments']:
                            result = "Good"
                            if Payment_Behaviour == 'Low_spent_Medium_value_payments' and Credit_Utilization_Ratio > 0.6279:
                                result = "Poor"
                        else:
                            result = "Standard"

            # validação de crédito bom
            elif credit_mix == "Good":
                if Delay_from_due_date <= 15.5:
                    result = "Good"
                    if Num_Credit_Card >= 0.0037:
                        result = "Standard"
                        if Num_Bank_Accounts > 0.0036:
                            result = "Good"
                            if occupation == 'Engineer' and Total_EMI_per_month >= 0.0012:
                                result = 'Standard'
                            elif occupation == 'Architect' and Payment_Behaviour == 'High_spent_Small_value_payments':
                                result = 'Standard'
                            elif occupation == 'Mechanic' and Interest_Rate <= 0.0009:
                                result = 'Standard'
                            elif occupation == 'Musician' and Total_EMI_per_month <= 0.0017:
                                result = 'Poor'
                            elif occupation == 'Teacher' and Interest_Rate <= 0.0008:
                                result = 'Poor'
                                if Num_Credit_Inquiries <= 0.0006:
                                    result = "Standard"
                            elif occupation in ['Doctor', 'Scientist']:
                                result = 'Poor'
                                if Total_EMI_per_month > 4.82E-5:
                                    result = "Good"
                                    if Total_EMI_per_month > 0.0011:
                                        result = 'Standard'
                            elif occupation == 'Writer' and Payment_Behaviour in ['High_spent_Small_value_payments', 'Low_spent_Small_value_payments', 'High_spent_Large_value_payments']:
                                result = 'Standard'
                            else:
                                result = "Good"
                elif Delay_from_due_date > 15.5:
                    if Num_Bank_Accounts <= 0.0036:
                        result = "Poor"
                    elif Num_Bank_Accounts > 0.0036:
                        result = "Good"

            # validação credito padrão
            elif credit_mix == 'Standard':
                if Interest_Rate > 0.0034:
                    result = "Poor"
                elif Interest_Rate <= 0.0034:
                    if Delay_from_due_date > 42.5:
                        result = "Poor"
                    elif Num_Bank_Accounts > 0.044:
                        result = "Standard"
                    elif Payment_Behaviour != "!@9#%8" and Payment_Behaviour != "Low_spent_Small_value_payments":
                        result = "Poor"
                    elif Delay_from_due_date > 35.5 and selected_month == 'April':
                        result = "Poor"
                    elif Delay_from_due_date > 34.5 and selected_month == 'January':
                        result = "Poor"
                    elif Delay_from_due_date > 35.5 and selected_month in ['February', 'July']:
                        result = "Poor"
                    elif Delay_from_due_date > 36.5 and selected_month == 'March':
                        result = "Poor"
                    elif Delay_from_due_date > 37.5 and selected_month == 'April':
                        result = "Poor"
                    elif Delay_from_due_date > 38.5 and selected_month == 'May':
                        result = "Poor"
                    elif Delay_from_due_date > 39.5 and selected_month == 'August':
                        result = "Poor"
                    elif Delay_from_due_date > 40.5 and selected_month == 'August':
                        result = "Poor"

            # validação de crédito Ruim
            elif credit_mix == "bad":
                result = "Poor"
                if Total_EMI_per_month > 0.002:
                    result = "Poor"
                elif Total_EMI_per_month <= 0.002:
                    result = "Poor"

            if occupation == "_" and (Payment_Behaviour == "Low_spent_Small_value_payments" or Payment_Behaviour == "High_spent_medium_value_payments") and Delay_from_due_date <= 34.5:
                result = "Standard"
            elif occupation == "Musician" and Payment_Behaviour == "!@9#%8":
                result = "Standard"
            elif occupation == "Musician" and Payment_Behaviour == "High_spent_medium_value_payments":
                result = "Standard"
            elif selected_month == "March" and occupation == "Media_Manager" and Total_EMI_per_month >= 0.0035:
                result = "Standard"
            elif occupation == "Accountant" and Payment_Behaviour == "Low_spent_small_value_payments" and Total_EMI_per_month <= 0.0031 and Num_Credit_Inquiries > 0.0029 and Delay_from_due_date <= 56.5 and Interest_Rate > 0.0028:
                result = "Standard"




        except Exception as e:
            print(f"Erro ao processar o formulário: {e}")

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
