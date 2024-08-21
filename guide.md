# Projeto Rastreador de criptomoedas

Crie um programa em Python que rastreia os preços do Bitcoin usando uma API de mercado
de criptomoedas (por exemplo, CoinGecko ou CoinMarketCap) e que, ao iniciar pede para o
usuário enviar um e-mail quando ele cair abaixo de um certo valor(ex: abaixo de 300mil), esse
valor deve ser determinado pelo usuário no início do programa. Sempre que o valor cair abaixo
do valor esperado, enviar um relatório por e-mail informando o valor encontrado.

# Quais tecnologias usar ?

- requests
- email
- loadenv
- json

# Passo a passo

# pegar a api e fazer o get nela
# pegar o id do bitcoin
# pegar o valor
# pegar o input do usuario(valor do bitcoin que deseja)
# pegar o email do usuario
  - perguntar se o email esta correto
   - caso nao, perguntar o email novamente
# se o valor do bitcoin cair abaixo do que o usuario informou
  - enviar um relatorio informando o valor
# se nao
  - informa o valor atual
# agendar automação
  - agendar de 10 em 10 min
    - perguntar se o usuario irar querer agendar a automação ou cancelar
