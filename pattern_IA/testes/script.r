mypath <- "/home/jfilho/Documentos/Git/tcc_cuda_opentuner_joao/pattern_IA/testes/gemm-smefficiency-512-todas-conf-gtx780.csv"

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


## graficos de densidade da variavel smefficiency
with(dados, plot(density(smefficiency), ylim = c(0, 0.1)))
with(dados, hist(smefficiency, add = TRUE, freq = FALSE))

## escala log
with(dados, plot(density(log(smefficiency)), ylim = c(0, 2)))
with(dados, hist(log(smefficiency), add = TRUE, freq = FALSE))


options(max.print = 100000000)

## tables das variaveis g e b
with(dados, table(g))
with(dados, table(b))
with(dados, plot(table(g)))
with(dados, plot(table(b)))


tabg <- as.data.frame(table(dados$g))
tabg <- tabg[order(tabg[,1]),]

tabb <- as.data.frame(table(dados$b))
tabb <- tabb[order(tabb[,2]),]



## usando funcoes da biblioteca lattice
library(lattice)

# x11()
png(filename = "~/Documentos/Git/tcc_cuda_opentuner_joao/pattern_IA/smeffic.png", 
    width = 1600, height = 600)
xyplot(smefficiency ~ b, data = dados, 
       xlab = "Configurações de Blocos",
       ylab = "Porcentagem de Warps Ativos (smefficiency)",
       as.table = TRUE, jitter.x = TRUE, jitter.y = TRUE,
       scales = list(y = list(cex = 1),
                     x = list(cex = 0.7, rot = 90))
       # layout = c(22,20) 
       )
dev.off()


dados$cut.efic <- with(dados, cut(smefficiency, 
                                  breaks = c(0,18, 30, 60, 80, 100)))

with(dados, table(cut.efic))

dados.80.100 <- subset(dados, cut.efic == "(80,100]")
dados.60.80 <- subset(dados, cut.efic == "(60,80]")
dados.30.60 <- subset(dados, cut.efic == "(30,60]")
dados.18.30 <- subset(dados, cut.efic == "(18,30]")
dados.0.18 <- subset(dados, cut.efic == "(0,18]")

str(dados.60.80)

# segundo gráfico

png(filename = "~/Documentos/Git/tcc_cuda_opentuner_joao/pattern_IA/dens_smeffic.png", 
    width =800, height = 600)
par(mar = c(5,4,1,1))
with(dados.80.100, plot(density(smefficiency),
                        xlab = "Proporção de configurações acima de 80%",
                        ylab = "Densidade",
                        main = ""
                        # ylim = c(0, 0.1)
                        ))
dev.off()

with(dados.80.100, hist(smefficiency, add = TRUE, freq = FALSE))

## escala log
with(dados.80.100, plot(density(log(smefficiency)), 
                        # ylim = c(0, 2)
                        ))
with(dados.80.100, hist(log(smefficiency), add = TRUE, freq = FALSE))

# terceiro gráfico

png(filename = "~/Documentos/Git/tcc_cuda_opentuner_joao/pattern_IA/todas_smeffic.png", 
    width = 2500, height = 1200)
xyplot(smefficiency ~ b|g, data = dados.80.100,
       xlab = list(label = "Todas as configurações \nacima de 80%", cex = 1.5),
       ylab = list(label ="Porcentagem de Warps Ativos (smefficiency)",cex = 1.5),
       as.table = TRUE, jitter.x = TRUE, jitter.y = TRUE,
       scales = list(y = list(cex = 1),
                     x = list(cex = 0.9, rot = 90)),
       layout = c(12,9) 
)
dev.off()

## -------------------------Regressao linear-----------------------------------

plot(dados.80.100$g,dados.80.100$smefficiency)

## -------------------------Dendograma-----------------------------------------
install.packages("vegan")
library(vegan)

# calcula a matriz de distância, as ligações, 
# plota o dendrograma e identifica os grupos
dis <- vegdist(dados) 
cluc <- hclust(dis, "complete")
plot(cluc)
rect.hclust(cluc, 3) 

# verifica que objetos foram classificados em cada grupo
grp<-cutree(cluc, 3)
grp

# substitui no dendrograma o nome do objeto pelo número do grupo
plot(cluc, labels = as.character(grp))

# desenha no dendrograma os retângulos de cada grupo e os numera
plot(cluc)
r <- rect.hclust(cluc, 3)
text(cumsum(sapply(r,length)),
     rep(mean(tail(unique(cluc$hei),2)), length(r)),
     paste(unique(grp[cluc$ord])))




## ----------------------------------------------------------------------------
## Pensando ...
teste <- as.data.frame(with(dados, table(g)))
temp <- subset(teste, Freq == 0 )


subset(dados, g == "2048.256.1024")

