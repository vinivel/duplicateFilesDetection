# Gerenciador de Arquivos Duplicados
## Descrição
Este é um programa desenvolvido em Python com interface gráfica para verificar, identificar e gerenciar arquivos duplicados em uma pasta selecionada. Ele utiliza hash (xxHash) para identificar arquivos duplicados de maneira eficiente, oferecendo opções para movê-los automaticamente ou com base na seleção do usuário.
## Funcionalidades 💡
- **Verificar arquivos duplicados por hash**: O programa calcula os hashes (xxHash) dos arquivos para identificar duplicatas.
- **Exibir duplicatas em forma de lista paginada**: Os resultados são exibidos com paginação, facilitando a navegação entre vários arquivos duplicados.
- **Mover arquivos duplicados automaticamente**: É possível mover duplicatas para uma subpasta chamada `duplicados`.
- **Mover arquivos com base em seleção manual**: O usuário pode marcar os arquivos duplicados desejados e movê-los para uma pasta separada.
- **Interface gráfica amigável**: Construída com o módulo Tkinter para facilitar a interação do usuário.

## Tecnologias utilizadas 🚀
- Python 3.x
- Interface gráfica com **Tkinter**
- Manipulação de arquivos com **os**, **shutil**
- **xxHash** para hashing rápido
- Threads com **multiprocessing.pool.ThreadPool** para processar arquivos em paralelo

## Como usar?
1. **Instale as dependências necessárias**: Certifique-se de ter instalado o módulo `xxhash` na sua máquina:
``` bash
   pip install xxhash
```
1. **Execute o programa**: Basta executar o arquivo Python:
``` bash
   python gerenciador_duplicados.py
```
1. **Selecione a pasta**: Clique no botão "Selecionar Pasta" na interface e selecione a pasta que deseja analisar.
2. **Aguarde o processamento**: O programa analisará os arquivos utilizando hashes para identificar duplicados e mostrará os resultados em uma interface paginada.
3. **Gerencie duplicados**:
    - Você pode mover arquivos automaticamente para uma subpasta chamada `duplicados`.
    - Ou mover arquivos específicos marcando-os manualmente na interface.

## Estrutura do Código 🛠
### Principais funções do programa:
1. **`calcular_xxhash_completo(file_path)`**: Calcula o hash completo de um arquivo utilizando o algoritmo xxHash para identificar duplicatas eficientemente.
2. **`obter_data_criacao_pasta(filepath)`**: Obtém a data de criação da pasta que contém o arquivo.

### Classe principal:
A lógica principal está encapsulada na classe `AppDuplicados`.
**Componentes principais**:
- **Interface gráfica**:
    - Criada com Tkinter, inclui barra de progresso, botões de navegação, e seleção de arquivos duplicados.

- **Paginação**:
    - A classe suporta paginação para melhor exibição de arquivos duplicados encontrados.

- **Funções de ação**:
    - Verificar duplicados
    - Mover duplicados automaticamente
    - Mover duplicados manualmente com base na seleção.

**Principais métodos**:
- `verificar_duplicados()`: Faz a análise dos arquivos para encontrar duplicados.
- `mover_duplicados_por_pasta()`: Move duplicatas automaticamente baseando-se na data de criação da pasta.
- `mover_arquivos()`: Move arquivos manualmente, conforme seleção do usuário.
- `exibir_pagina()`: Exibe os resultados em uma lista paginada.

## Exemplo de execução
Interface principal ao executar o programa:
1. **Tela inicial**:
    - Botão para selecionar a pasta a ser analisada.
    - Barra de progresso para indicar processamento.

2. **Resultados**: Exibição de duplicados em formato paginado com checkboxes para facilitar a seleção.
3. **Opções para mover duplicados**:
    - Baseado em seleção manual.
    - Baseado em data de criação da pasta, automaticamente.

## Melhorias futuras ✨
- Adicionar opção para excluir arquivos duplicados diretamente da interface.
- Suporte para exportar os resultados em CSV ou JSON.
- Suporte para análise recursiva mais avançada (configurações personalizáveis).
- Melhor feedback visual, como indicadores do progresso do hash em tempo real.

## Licença 📜
Este projeto é open-source e está licenciado sob a licença [MIT]().
