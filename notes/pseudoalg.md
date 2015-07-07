- Em crossover/mutação, a chance de escolher o ponto de troca de sub-árvore deve ser uma distribuição uniforme para todos os nodos da árvore?
- Por que existe um limite de profundidade para a mutação?

Pseudo-algoritmo de PG - Fitness de uma função
==============================================

Parâmetros e preliminares
-------------------------

- Conjunto de terminais: variável x, algumas constantes
- Conjunto de funções: adição, subtração, multiplicação, divisão protegida
- Training set
- Função de fitness: soma do quadrado dos erros para cada caso do conjunto de treinamento (padronizada, contínua)
- Método de seleção: _tournament selection_ (tamanho do torneio a ser calibrado)
- Parâmetros a serem calibrados: tamanho da população, tamanho máximo de um indivíduo (profundidade ou número de nodos), probabilidades de crossover e mutação, número máximo de gerações
- Inicialização da população: _grow_

Funções relevantes
------------------

- Fitness: soma dos quadrados das diferenças entre o resultado esperado e o obtido pelo indivíduo para cada caso do training set.
- Gerador de árvore por grow: gera uma sub-árvore aleatória com limitação de profundidade ou número de nodos (decidir isso)
- Tournament selection: Seleção de indivíduos promissores
- Crossover: cria filho por crossover de dois indivíduos
- Mutação: cria filho por mutação de um indivíduo

Fluxo
-----

1. Gera população inicial por grow;
2. Repete os procedimentos 3 e 4 pelo número determinado de gerações;
3. Avaliar todos os indivíduos
3. Obtém os indivíduos vencedores do torneio, descartando os perdedores;
4. Elitismo
5. Realiza operações de variação entre os vencedores aleatoriamente, de acordo com as probabilidades definidas nos parâmetros para crossover, mutação e reprodução, até gerar uma nova população do tamanho desejado;
6. Retorna o melhor indivíduo da população

Notas e detalhes de implementação
---------------------------------


