# Análise de Carteiras de Ações com Base em ROE e Magic Formula

Este projeto tem como objetivo criar uma carteira de ações com base nos 10 papéis com maior **ROE (Return on Equity)** e compará-la com o desempenho do **IBOVESPA** e da estratégia **Magic Formula** de Joel Greenblatt no período de **01 de abril de 2023** até **25 de setembro de 2024**. Adicionalmente, o projeto inclui análises gráficas e simulações avançadas para complementar as análises iniciais.

## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Metodologia](#metodologia)
- [Resultados Esperados](#resultados-esperados)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Descrição do Projeto

O projeto é composto por dois scripts principais:

1. **`main.py`**: Realiza a seleção das ações, montagem das carteiras baseadas em ROE e na Magic Formula, e compara o desempenho das carteiras com o IBOVESPA.

2. **`plot.py`**: Complementa o `main.py` adicionando análises gráficas e simulações avançadas, incluindo:

   - Plotagem do histórico de preços das ações selecionadas.
   - Plotagem dos retornos diários das ações.
   - Cálculo e visualização da matriz de correlação dos retornos.
   - Simulação de portfólios aleatórios e identificação do portfólio com o maior Índice de Sharpe.
   - Cálculo e plotagem da fronteira eficiente de Markowitz.
   - Visualização da evolução do patrimônio investido nas carteiras.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `requests`
  - `python-dotenv`
  - `scipy`

## Instalação

1. **Clone o repositório ou copie os arquivos para um diretório local**.

2. **Crie um ambiente virtual** (opcional, mas recomendado):

   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**:

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**:

   ```bash
   pip install pandas numpy matplotlib seaborn requests python-dotenv scipy
   ```

   **Ou utilize o arquivo `requirements.txt`** (se disponível):

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. **Obtenha o Token JWT**:

   Você precisará de um token JWT válido para acessar a API do Laboratório de Finanças. Certifique-se de ter o token de acesso.

2. **Crie um arquivo `.env`** na raiz do projeto e adicione o seu token:

   ```
   TOKEN=seu_token_jwt_aqui
   ```

   Substitua `seu_token_jwt_aqui` pelo seu token real.

3. **Adicione o arquivo `.env` ao seu `.gitignore`** (se aplicável):

   ```
   # .gitignore
   .env
   ```

## Uso

1. **Execute o `main.py`** para realizar a análise inicial das carteiras:

   ```bash
   python main.py
   ```

   O script irá:

   - Obter os dados financeiros das ações na data base especificada (`2024-09-25`).
   - Calcular o rendimento do IBOVESPA no período.
   - Selecionar as top 10 ações por ROE e pela Magic Formula.
   - Calcular os rendimentos das ações selecionadas.
   - Comparar os rendimentos das carteiras com o IBOVESPA.
   - Exibir os resultados no console.

2. **Execute o `plot.py`** para gerar as análises gráficas e simulações avançadas:

   ```bash
   python plot.py
   ```

   O script irá:

   - Plotar o histórico de preços das ações selecionadas.
   - Plotar os retornos diários das ações.
   - Calcular e exibir estatísticas descritivas dos retornos.
   - Plotar a matriz de correlação dos retornos.
   - Simular 10.000 portfólios aleatórios.
   - Identificar e plotar o portfólio com o maior Índice de Sharpe.
   - Calcular e plotar a fronteira eficiente de Markowitz.
   - Visualizar a evolução do patrimônio investido na carteira de máximo Sharpe.

## Metodologia

### 1. Coleta de Dados

- **Planilhão**: Obtém dados financeiros das empresas na data base de **25/09/2024**.
- **Preços Históricos**: Obtém os preços ajustados das ações selecionadas e do IBOVESPA para o período de **25/09/2023** a **25/09/2024**.

### 2. Seleção de Ações

- **Carteira ROE**:
  - Seleciona as 10 ações com os maiores valores de ROE.
  - Remove duplicatas, mantendo a ação com maior volume.
- **Carteira Magic Formula**:
  - Exclui setores não aplicáveis (bancos, seguros e financeiros).
  - Calcula o ranking combinado de ROIC e Earning Yield.
  - Seleciona as 10 ações com melhor posição no ranking.

### 3. Análise de Desempenho (`main.py`)

- **Cálculo de Rendimentos**:
  - Calcula o rendimento percentual de cada ação no período.
  - Calcula o rendimento médio das carteiras.
- **Comparação com o IBOVESPA**:
  - Compara o rendimento individual e médio das carteiras com o rendimento do IBOVESPA.
  - Identifica quais ações superaram o índice.

### 4. Análises Gráficas e Simulações (`plot.py`)

- **Plotagem do Histórico de Preços e Retornos**:
  - Visualiza o comportamento das ações ao longo do tempo.
- **Estatísticas Descritivas e Correlação**:
  - Apresenta estatísticas dos retornos e analisa a correlação entre as ações.
- **Simulação de Portfólios Aleatórios**:
  - Simula 10.000 portfólios com alocações aleatórias.
  - Calcula o retorno esperado, volatilidade e Índice de Sharpe de cada portfólio.
- **Otimização do Portfólio**:
  - Identifica o portfólio com o maior Índice de Sharpe.
  - Calcula e plota a fronteira eficiente de Markowitz.
- **Evolução do Patrimônio**:
  - Calcula a evolução do patrimônio investido na carteira de máximo Sharpe.
  - Visualiza a evolução do valor investido em cada ação individualmente.

## Resultados Esperados

O projeto fornecerá:

- **Rendimento do IBOVESPA** no período analisado.
- **Rendimentos individuais** das ações nas carteiras ROE e Magic Formula.
- **Lista de ações** que superaram ou não o IBOVESPA em cada carteira.
- **Rendimento médio** das carteiras.
- **Conclusão** sobre o desempenho das carteiras em relação ao IBOVESPA.
- **Gráficos** que ilustram:
  - Histórico de preços e retornos das ações selecionadas.
  - Matriz de correlação dos retornos.
  - Portfólios simulados e fronteira eficiente.
  - Evolução do patrimônio investido nas carteiras.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é de uso livre para fins educacionais e não possui uma licença específica.

---

**Atenção**: Este script é fornecido para fins educacionais e não constitui recomendação de investimento. Sempre consulte um profissional qualificado antes de tomar decisões financeiras.

## Observações Finais

- **Datas de Análise**: Certifique-se de que as datas definidas nos scripts (`data_base`, `data_inicio` e `data_fim`) correspondem aos dados disponíveis na API e ao período que deseja analisar.
- **Disponibilidade de Dados**: Verifique se a API do Laboratório de Finanças possui dados disponíveis para as datas especificadas. Ajuste as datas se necessário.
- **Personalização**: Sinta-se à vontade para ajustar os parâmetros, adicionar novas análises ou personalizar os gráficos conforme suas necessidades.
- **Interpretação dos Resultados**: Utilize os resultados como uma ferramenta para compreensão e estudo de estratégias de investimento, mas lembre-se das limitações e riscos envolvidos em investimentos reais.


---

Esperamos que este projeto seja útil em seus estudos e análises financeiras. Bom trabalho!