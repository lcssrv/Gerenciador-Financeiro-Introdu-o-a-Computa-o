# Gerenciador-Financeiro-Introducao-A-Computacao
Trabalho de Gerenciador Financeiro
======================================================
PROJETO: GERENCIADOR FINANCEIRO PESSOAL
======================================================

1. DESCRIÇÃO DO PROJETO
Aplicação de linha de comando (CLI) desenvolvida em Python para o controle de finanças pessoais. O sistema permite ao usuário registrar receitas e despesas, calcular saldo, visualizar gráficos em ASCII e verificar limites de orçamento por categoria. Todos os dados são salvos de forma persistente em um arquivo de texto (financas.csv).

2. INTEGRANTES DO GRUPO (NOMES COMPLETOS)
- [Lucas Saraiva Silva Coêlho]

3. DIVISÃO DE RESPONSABILIDADES
- [Lucas Saraiva Silva Coêlho]: Desenvolvimento da estrutura base do arquivo e lógicas de CRUD (Fase 1 e 3).
- Implementação dos cálculos matemáticos e geração do Relatório Mensal (Fase 2).
- Criação do menu interativo, gráfico ASCII e validações de input do usuário (Fase 4).


4. BIBLIOTECAS UTILIZADAS
O projeto foi desenvolvido utilizando apenas bibliotecas padrão do Python (não é necessário usar "pip install"):
- csv: Para leitura, escrita e manipulação do banco de dados das movimentações.
- os: Para verificação da existência prévia do arquivo de salvamento.
- datetime: Para capturar a data e hora exatas de cada registro de forma automática.

5. INSTRUÇÕES DE EXECUÇÃO PASSO A PASSO
Passo 1: Certifique-se de ter o Python 3.x instalado em sua máquina.
Passo 2: Baixe e extraia os arquivos do projeto em uma pasta de sua preferência.
Passo 3: Abra o terminal (Prompt de Comando, PowerShell ou terminal do VS Code).
Passo 4: Navegue até a pasta onde o arquivo "projetocompleto.py" está salvo.
Passo 5: Execute o comando abaixo para iniciar o programa:

    python projetocompleto.py

Passo 6: Utilize os números (0 a 6) para navegar pelo menu interativo diretamente no terminal. O arquivo "financas.csv" será criado automaticamente no primeiro uso.
