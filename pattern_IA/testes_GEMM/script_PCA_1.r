library(vegan)
dados <- read.csv("/home/joao/Documentos/tcc_cuda_opentuner_joao/pattern_IA/testes_GEMM/gemm-smefficiency/gemm-smefficiency-512.csv",header = T)
resultado<-prcomp(dados)
resultado
summary(resultado)
resultado$x
resultado$loadings
biplot(resultado)
screeplot(resultado)
round(apply(dados,2,var),4)  
dadospadronizado<-scale(dados)
prcomp(dadospadronizado)
