import pandas as pd
from sklearn.linear_model import LinearRegression

def main():
    # Exemplo de fluxo de treinamento
    # Substitua 'data/train.csv' pelo caminho real dos seus dados
    df = pd.read_csv('data/train.csv')
    X = df.drop('target', axis=1)
    y = df['target']

    model = LinearRegression()
    model.fit(X, y)
    print("Modelo treinado com coeficientes:", model.coef_)

if __name__ == '__main__':
    main()
