#install.packages("vegan")
#install.packages("psych")
require(vegan)
require(psych)
dados <- read.csv("/home/jfilhogn/Documentos/Git/tcc_cuda_opentuner_joao/pattern_IA/testes_GEMM/gemm-smefficiency/gemm-smefficiency-512.csv",header = T)
is.data.frame(dados)
round(apply(dados,2,var),2)
prc.dados <- prcomp(dados); prc.dados
screeplot(prc.dados)
summary(prc.dados)
biplot(prc.dados)
prc.dados$x
fa.parallel(dados, fa="pc")
pca.dados <- principal(dados, nfactors=2, n.obs=24,rotate='none', scores=TRUE)
