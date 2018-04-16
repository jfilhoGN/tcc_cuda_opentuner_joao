import MySQLdb

db = MySQLdb.connect(host="localhost",
	user="webgpu",
	passwd="webgpu123",
	db="comparacao_grid_grid")

def comparacao_grid_grid():
	print "grid_grid"
	arquivo_grid_grid = open('/home/joao/Documentos/tcc_cuda_opentuner_joao/pattern_IA/testes/comparacao_grid_grid_mysql.csv','w')
	cursor = db.cursor()
	cursor.execute("Select A.gx,A.gy,A.gz, B.gx,B.gy,B.gz, B.smefficiency from A as A, A as B where (A.gx = B.gx and A.gy = B.gy and A.gz = B.gz) or (A.gy = B.gx and A.gz = B.gy and A.gx = B.gz) or (A.gz = B.gx and A.gx = B.gy and A.gy = B.gz) order by B.smefficiency")
	numlinhas = int(cursor.rowcount)
	arquivo_grid_grid.write("gx,gy,gz,gx,gy,gz,smefficiency\n")
	for x in range(0,numlinhas):
		row = cursor.fetchone()
		linha = str(row)
		linha = linha.replace("L","").replace("(","").replace(")","").replace(" ","")
		arquivo_grid_grid.write(linha+"\n")

def comparacao_bloco_bloco():
	print "bloco_bloco"
	arquivo_bloco_bloco = open('/home/joao/Documentos/tcc_cuda_opentuner_joao/pattern_IA/testes/comparacao_bloco_bloco_mysql.csv','w')
	cursor = db.cursor()
	cursor.execute("Select A.bx,A.byy,A.bz, B.bx,B.byy,B.bz, B.smefficiency from A as A, A as B where (A.bx = B.bx and A.byy = B.byy and A.bz = B.bz) or (A.byy = B.bx and A.bz = B.byy and A.bx = B.bz) or (A.bz = B.bx and A.bx = B.byy and A.byy = B.bz) order by B.smefficiency")
	numlinhas = int(cursor.rowcount)
	arquivo_bloco_bloco.write("bx,by,bz,bx,by,bz,smefficiency\n")
	for x in range(0,numlinhas):
		row = cursor.fetchone()
		linha = str(row)
		linha = linha.replace("L","").replace("(","").replace(")","").replace(" ","")
		arquivo_bloco_bloco.write(linha+"\n")

def comparacao_grid_bloco():
	print "grid_bloco"
	arquivo_grid_bloco = open('/home/joao/Documentos/tcc_cuda_opentuner_joao/pattern_IA/testes/comparacao_grid_bloco_mysql.csv','w')
	cursor = db.cursor()
	cursor.execute("Select A.gx,A.gy,A.gz, B.bx,B.byy,B.bz, B.smefficiency from A as A, A as B where (A.gx = B.bx and A.gy = B.byy and A.gz = B.bz) or (A.gy = B.bx and A.gz = B.byy and A.gx = B.bz) or (A.gz = B.bx and A.gx = B.byy and A.gy = B.bz) order by B.smefficiency")
	numlinhas = int(cursor.rowcount)
	arquivo_grid_bloco.write("gx,gy,gz,bx,by,bz,smefficiency\n")
	for x in range(0,numlinhas):
		row = cursor.fetchone()
		linha = str(row)
		linha = linha.replace("L","").replace("(","").replace(")","").replace(" ","")
		arquivo_grid_bloco.write(linha+"\n")

if __name__ == '__main__':
	#comparacao_grid_grid()
	#comparacao_bloco_bloco()
	#comparacao_grid_bloco()

