# Análise de Carteiras de Ações com Base em ROE e Magic Formula

Este projeto tem como objetivo criar uma carteira de ações com base nos 10 papéis com maior **ROE (Return on Equity)** e compará-la com o desempenho do **IBOVESPA** e da estratégia **Magic Formula** de Joel Greenblatt no período de **01 de abril de 2023** até **25 de setembro de 2024**.

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

O script em Python realiza as seguintes tarefas:

1. **Coleta de Dados**: Obtém dados financeiros das ações a partir da API do Laboratório de Finanças, filtrando por ROE e outros indicadores conforme necessário.
2. **Montagem da Carteira**:
   - **Carteira ROE**: Seleciona as 10 ações com os maiores valores de ROE.
   - **Carteira Magic Formula**: Aplica a fórmula de Joel Greenblatt, analisando conjuntamente o ROIC e o Earning Yield.
3. **Análise de Desempenho**:
   - Calcula o rendimento das carteiras no período especificado.
   - Compara o desempenho das carteiras com o IBOVESPA.
   - Identifica quais ações superaram ou não o rendimento do índice.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - `pandas`
  - `requests`
  - `python-dotenv`

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
   pip install -r requirements.txt
   ```

   **Caso não tenha um arquivo `requirements.txt`, instale as bibliotecas diretamente**:

   ```bash
   pip install pandas requests python-dotenv
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

   Se você estiver usando o Git, é recomendável adicionar o arquivo `.env` ao `.gitignore` para evitar que o token seja enviado para um repositório remoto.

   ```
   # .gitignore
   .env
   ```

## Uso

1. **Execute o script**:

   ```bash
   python main.py
   ```

2. **Aguarde a execução**:

   O script irá:

   - Obter os dados financeiros das ações na data base especificada.
   - Calcular o rendimento do IBOVESPA no período.
   - Selecionar as top 10 ações por ROE e pela Magic Formula.
   - Calcular os rendimentos das ações selecionadas.
   - Comparar os rendimentos das carteiras com o IBOVESPA.
   - Exibir os resultados no console.

## Metodologia

### 1. Coleta de Dados

- **Planilhão**: Obtém dados financeiros das empresas, como ROE, ROIC, Earning Yield, etc., na data base de 03/04/2023.
- **Preços Históricos**: Obtém os preços ajustados das ações selecionadas e do IBOVESPA para o período de 03/04/2023 a 01/04/2024.

### 2. Seleção de Ações

- **Carteira ROE**:
  - Seleciona as 10 ações com os maiores valores de ROE.
  - Remove duplicatas, mantendo a ação com maior volume.
- **Carteira Magic Formula**:
  - Exclui setores não aplicáveis (bancos, seguros e financeiros).
  - Calcula o ranking combinado de ROIC e Earning Yield.
  - Seleciona as 10 ações com melhor posição no ranking.

### 3. Análise de Desempenho

- **Cálculo de Rendimentos**:
  - Calcula o rendimento percentual de cada ação no período.
  - Calcula o rendimento médio das carteiras.
- **Comparação com o IBOVESPA**:
  - Compara o rendimento individual e médio das carteiras com o rendimento do IBOVESPA.
  - Identifica quais ações superaram o índice.

## Resultados Esperados

O script irá fornecer:

- **Rendimento do IBOVESPA** no período analisado.
- **Rendimentos individuais** das ações nas carteiras ROE e Magic Formula.
- **Lista de ações** que superaram ou não o IBOVESPA em cada carteira.
- **Rendimento médio** das carteiras.
- **Conclusão** sobre o desempenho das carteiras em relação ao IBOVESPA.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é de uso livre para fins educacionais e não possui uma licença específica.

---

**Atenção**: Este script é fornecido para fins educacionais e não constitui recomendação de investimento. Sempre consulte um profissional qualificado antes de tomar decisões financeiras.
