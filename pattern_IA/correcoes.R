mypath <- "/home/jfilho/Documentos/Git/tcc_cuda_opentuner_joao/results/gtx780/gemm-gld_efficiency/gemm-gld_efficiency-160.csv"

dados <- read.csv(mypath, header = T, sep = ",")
is.data.frame(dados)
head(dados)
str(dados)
summary(dados)

# adiciona interacao entre g e b
dados <- transform(dados, 
                   g=interaction(gx,gy,gz),
                   b=interaction(bx,by,bz))

# limpa os níveis não utilizados
dados <- droplevels(dados)

library(lattice)

# x11()
png(filename = "~/Documentos/Git/tcc_cuda_opentuner_joao/pattern_IA/gld_780.png", 
    width = 1600, height = 600)
xyplot(gld_efficiency ~ b, data = dados, 
       xlab = "Configurações",
       ylab = "Resultados gerados pela métrica gld_efficiency",
       as.table = TRUE, jitter.x = TRUE, jitter.y = TRUE,
       scales = list(y = list(cex = 1),
                     x = list(cex = 0.7, rot = 90))
       # layout = c(22,20) 
)
dev.off()