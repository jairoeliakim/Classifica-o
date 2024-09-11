import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Carregar dados do CSV
data = pd.read_csv('train.csv')

# Pré-processamento de dados (exemplo: codificação one-hot para variáveis categóricas)
data = pd.get_dummies(data, columns=['variavel_categorica'])

# Dividir dados em treinamento e teste
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Definir características (features) e alvo (target)
features = data.columns.drop('variavel_alvo')
target = 'variavel_alvo'

# Construir modelo
model = Sequential([
    Dense(128, activation='relu', input_shape=(len(features),)),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Treinar o modelo
model.fit(train_data[features], train_data[target], epochs=10, batch_size=32, validation_data=(test_data[features], test_data[target]))

# Avaliar o modelo
accuracy = model.evaluate(test_data[features], test_data[target])[1]
print(f'Model Accuracy: {accuracy}')

# Salvar o modelo
model.save('seu_credit.h5')
