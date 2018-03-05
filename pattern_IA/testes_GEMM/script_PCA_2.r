library(pca)
read.csv("/home/joao/Documentos/tcc_cuda_opentuner_joao/pattern_IA/testes_GEMM/gemm-smefficiency/gemm-smefficiency-512.csv",header = T) #load data
head(crimtab) #show sample data
dim(crimtab) #check dimensions
str(crimtab) #show structure of the data
sum(crimtab) 
colnames(crimtab)
apply(crimtab,2,var) #check the variance accross the variables
pca =prcomp(crimtab) #applying principal component analysis on crimtab data
par(mar = rep(2, 4)) #plot to show variable importance
plot(pca) 
'below code changes the directions of the biplot, if we donot include
the below two lines the plot will be mirror image to the below one.'
pca$rotation=-pca$rotation
pca$x=-pca$x
biplot (pca , scale =0) #plot pca components using biplot in 
