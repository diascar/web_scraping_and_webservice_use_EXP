import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import seaborn as sns

url = requests.get("https://www.promocaogames.com.br/")

page = BeautifulSoup(url.text, 'html5lib')

games = defaultdict(list)

for table in page.findAll('table'):
	cells = table.findAll('td')
	i = 0
	while i < len(cells) - 7:
		val = float(cells[i+1].text.split()[1].replace(',', '.')) if len(cells[i + 1].text.split()) > 1 else np.nan
		games[cells[i].text].append(val)
		i += 7

# evitando que um dataframe com valores de diferentes tamanhos
games = dict([(k,pd.Series(v)) for k, v in games.items()])

df = pd.DataFrame(games)

df = df.transpose().reset_index()
col_map = {"index": "game"}

for i in range(1, df.shape[1]):
	col_map.update({df.columns[i]: f'preco{i}'})
	
df.rename(columns = col_map, inplace = True)

# eliminando linhas de preco1 com dados faltantes
ndf = df[['game', 'preco1']].dropna()
ndf = ndf.set_index(['game'])

# plotando o preço de alguns jogos

s = ndf.sample(6)
colors = ["#f4ecf7", "#f9ebea", "#f3e5f5", "#DAF7A6", "#FFC300", "#FF5733"]
plt.barh(s.index, s.preco1, color = colors)
plt.show()

# histograma de preços
# bins - deciles

bins = Counter(ndf['preco1'].apply(lambda x: x // 10 *10))

plt.bar(bins.keys(), bins.values(), width = 8)
plt.xlabel('range of prices')
plt.ylabel('frequency')
plt.show()

# mais simples usando plt.hist()
plt.hist(ndf.preco1, edgecolor = '#f4ecf7', bins = 30)
plt.show()

# mais simples usando o seaborn
sns.histplot(data = ndf)
plt.show()
