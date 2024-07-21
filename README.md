# Projeto de Reprodução e Análise de Algoritmos de Ordenação

Este repositório contém o código, os resultados e a análise de um estudo comparativo entre algoritmos de ordenação tradicionais e algoritmos propostos em um artigo científico. Nosso objetivo foi reproduzir os resultados do artigo, comparar os algoritmos Corsort e Multizip Sort com algoritmos tradicionais como Heap Sort, Shell Sort e Merge Sort, e documentar o processo.

## Estrutura do Repositório

- `verify_performance_profiles.py`: Script para executar e verificar os algoritmos Corsort e Multizip Sort.
- `verify_performance_profiles_tradicional.py`: Script para executar e verificar os algoritmos Heap Sort, Shell Sort e Merge Sort.
- `plot_performance_profiles.py`: Script para gerar gráficos de performance profiles a partir dos resultados dos experimentos.
- `data/`: Diretório contendo os arquivos CSV com os resultados dos experimentos.
- `images/`: Diretório contendo os gráficos gerados pelos scripts de plotagem.

## Requisitos

- Python 3.x
- Bibliotecas:
  - matplotlib
  - pandas
  - numpy
  - loguru

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```
