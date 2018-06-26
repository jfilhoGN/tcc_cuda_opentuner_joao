Trabalho de Conclusão de Curso
---

**Título:** Ajuste nas dimensões de kernels para dispositivos aceleradores (GPUs) com base na análise de características arquiteturais e na utilização de ferramenta de Autotuning.

**Resumo:** Atualmente há uma lacuna de desempenho entre Unidade Central de Processamento (CPU) e Unidade de Processamento Gráfico (GPU), esta lacuna fez com que desenvolvedores tenham o interesse por aplicações que exploram o trabalho conjunto entre CPUs e GPUs. Contudo para criar essas aplicações os desenvolvedores encontram desafios, desde transformar código legado para sistemas *multicores* até encontrar a configuração ideal para a arquitetura do dispositivo alvo. Desta forma, este trabalho tem como objetivo analisar por meio de ferramentas de *autotuning* de software a escolha de configurações para o arranjo de *threads*, na tentativa de extrair o melhor desempenho para dispositivos aceleradores, neste caso *GPUs*. Para alcançar esse objetivo foi utilizado um subconjunto de algoritmos da família *Polybech, KernelGen* e NVIDIA *CUDA Samples* que tiveram seus *kernels* testados com a ferramenta de *autotuning* OpenTuner. Os *benchmarks* foram executados e resultados de algumas métricas foram coletados utilizando a ferramenta de perfilamento *nvprof* da NVIDIA para a escolha da melhor configuração para cada contexto. Os resultados sugerem que o meio mais eficiente para se encontrar a melhor configuração para a arquitetura é utilizando ferramentas de *autotuning*, pois para determinados tamanhos torna-se inviável a escolha da configuração por meio de busca exaustiva ou por escolhas aleatórias.

**Abstract:** Currently there is a performance gap between the Central Processing Unit (CPU) and the Graphics Processing Unit (GPU), this gap has made developers have an interest in applications that exploit the joint work between CPUs and GPUs.
However, to create such applications developers face challenges ranging from transforming legacy code to multicore systems until they find the optimal configuration for the target device architecture. In this way, this work has as its objective to analyze the choice of configurations for the arrangement of threads. We are using software tools in an attempt to extract the best performance for device accelerators, in this case GPUs.
To achieve this goal a set of algorithms of the Polybench, KernelGen and NVIDIA Samples were used which had their kernels tested with the OpenTuner autotuning tool. Benchmarks were executed and the results of some metrics were collected using nvprof NVIDIA's profiling tool to choose the best configuration for each context.
The results suggest that the most efficient way to find the best configuration for the architecture is to use autotuning tools, because for certain sizes it becomes impracticable to choose the configuration through exhaustive search or random choices.

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
