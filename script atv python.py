import pandas as pd
import matplotlib.pyplot as plt

risco_dict = {'C100': 'Baixo', 'C101': 'Alto', 'C102': 'Médio'}

df = pd.read_csv('transacoes.csv', encoding='latin1')

df['valor'] = df['valor'].fillna(df.groupby('estado_cliente')['valor'].transform('median'))

df['plataforma'] = 'Mobile'

df['data_transacao'] = pd.to_datetime(df['data_transacao']).dt.tz_localize('America/Sao_Paulo')

df['dia_semana'] = df['data_transacao'].dt.day_name()
df['mes'] = df['data_transacao'].dt.month

df = df.drop_duplicates()

filtro_setembro = df[(df['mes'] == 9) & ((df['estado_cliente'] == 'SP') | (df['estado_cliente'] == 'RJ')) & (df['valor'] > 5000)]

df['nivel_risco'] = df['id_cliente'].map(risco_dict)

pivot = pd.pivot_table(df, values='valor', index='mes', columns='nivel_risco', aggfunc='sum', margins=True)

df['z_score'] = df.groupby('estado_cliente')['valor'].transform(lambda x: (x - x.mean()) / x.std())

anomalias = df[df['z_score'] > 2.5]

diario = df.groupby(df['data_transacao'].dt.date)['valor'].sum()
media_movel = diario.rolling(7).mean()

fig, ax = plt.subplots()

ax.plot(diario.index, diario.values, label='Total Diário')
ax.plot(media_movel.index, media_movel.values, label='Média Móvel (7 dias)')

ax.set_ylim(bottom=0)
ax.set_title('Evolução do Valor Total de Transações Diárias')
ax.legend()

plt.show()