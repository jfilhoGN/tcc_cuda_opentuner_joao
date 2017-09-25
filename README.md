Trabalho de Conclusão de Curso
---

**Título:** Ajuste nas dimensões de kernels para dispositivos aceleradores (GPUs) com base na análise de características arquiteturais e na utilização de ferramenta de Autotuning.

**Resumo:** Atualmente há uma lacuna de desempenho entre Unidade Central de Processamento (CPU) e Unidade de Processamento Gráfico (GPU), esta lacuna fez com que desenvolvedores tenham o interesse pela realização de aplicações que exploram o trabalho conjunto entre CPUs e GPUs. Contudo para realizar essas aplicações os desenvolvedores encontram desafios desde transformar código legado para sistemas *multicores* a encontrar configuração ideal para a arquitetura que está utilizando. Desta forma, este trabalho tem como objetivo analisar por meio de ferramentas de *auto-tuning* de software de maneira a extrair o melhor desempenho para dispositivos aceleradores *GPU*. Com a melhor configuração encontrada ou padrões de configurações pretende-se criar um módulo para a ferramenta *PoLLy* do *LLVM* que transforme um código com laços aninhados em um *kernel* ajustado conforme esses padrões. Para alcançar esse objetivo será utilizado conjunto de algoritmos da família *ParSec*, *Polybech* e *Rodinia* que terão seus *kernels* testados por ferramentas de *auto-tuning* para encontrar através de métricas qual a melhor configuração para a arquitetura utilizada. Os primeiros resultados sugerem que o meio mais eficiente para se encontrar a melhor configuração para a arquitetura é utilizando ferramentas de *auto-tuning*, pois para determinados tamanhos torna-se inviável a escolha da configuração por meio de busca exaustiva ou por escolhas aleatórias.

**Aluno:** João Martins de Queiroz Filho

**Orientador:** Prof. Dr. Rogério Aparecido Gonçalves

Diretórios.
---

**[benchmarks](benchmarks/):** diretório contendo todos os experimentos realizados para o Trabalho de Conclusão de Curso

**[experimentos](experimentos/):** pasta que contém primeiros experimentos bem como algoritmo para checar as dimensões *checkDimension.cu*

**[opentuner](opentuner/):** pasta com o código-fonte da ferramenta de *auto-tuning* [Opentuner](http://opentuner.org/)

**[pattern_IA](pattern_IA/):** contém gráficos, scripts para gerar resultados e detectar padrões de configuração.

**[results](results/):** contém os resultados obtidos dos *benchmarks* em formato *.csv* e a melhor configuração em *.json*

**[wscad_tests](wscad_tests/):** contém os algoritmos, gráficos bem como resultados dos experimentos para o evento *WSCAD*. 
