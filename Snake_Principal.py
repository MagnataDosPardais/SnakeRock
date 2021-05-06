#Jogo da cobrinha programado com pygame.
#Por Marco Antônio Zerbielli Bee;
#Produzido de 24/01/2021 - 02/03/2021;
#Instituto Federal Catarinense: Campus Concórdia - Turma 1F;
#Professor: Tiago Mazzutti.


import pygame		#Inclui a biblioteca "pygame" (Controla a GUI, Som , Captura de teclas e outros eventos);
import random		#Inclui a biblioteca "random" (Gera valores pseudo-aleatórios);
import json			#Inclui a biblioteca "json" (Gerencia o banco de dados, com salvamentos e saída de valores);

pygame.init()			#Inicia a classe geral do pygame;
pygame.font.init()	#Inicia o sistema de fontes do pygame;
pygame.mixer.init()	#Inicia o sistema de som do pygame;

with open("Database.json", "r") as x:	#Abre o documento do banco de dados (JSON) no modo leitura;
	Data = json.load(x)						#Salva todos os dados na variável "Data";
	DataI = Data["Itens"]					#Salva todos os dados referentes aos itens na variável "DataI";
	DataS = Data["GameSaves"]				#Salva todos os dados referentes aos recordes e placares na variável "DataS";
	DataM = Data["Musics"]					#Salva todos os dados referentes às Músicas na variável "DataM";
#^Faz a leitura dos dados salvos no Banco de dados;

Dimentions = ((780, 660))																#Salva as dimensões da tela (em pixels);
Window = pygame.display.set_mode(Dimentions)										#Informa ao pygame a abertura da GUI;
Title = pygame.display.set_caption("Snake-Rock")								#Informa ao pygame o nome da aba;
pygame.display.set_icon(pygame.image.load("IMAGES/Guitarra_pixel.png"))	#Informa ao pygame o ícone da aba;

TimePlayed = ""								#String que contém um modo formatado do tempo jogado;
SecondsPlayed = 0								#Segundos jogados;
MinutesPlayed = 0								#Minutos jogados;
HoursPlayed = 0								#Horas jogadas (Porque esse jogo é demorado pra caral...);
GameSpeed = 50									#Delay de execução do jogo;
Score = 0										#Placar da partida;
ScoreRecord = DataS["Record"][0]			#Recebe o récorde em pontos salvo no Banco de Dados;
TimeScoreRecord = DataS["Record"][1]	#Recebe o récorde em tempo salvo no Banco de Dados;
Coins = DataS["Coins"]						#Recebe as moedas acumuladas salvas no Banco de Dados;
Backpack = [DataI["Zawarudo"],DataI["Buraco de minhoca"],DataI["Encantamento de Fortuna"],DataI["Pocao de Crescimento"],DataI["Escudo"],DataI["Ressurreicao"]]
#^"Mochila" que guarda todos os itens comprados salvas no Banco de Dados;
MusicUnlockedList = DataM["List"]		#Recebe a lista com as suas músicas desbloqueadas salvas no Banco de Dados;
SumonFood = [0,0,20]							#Recebe uma lista de valores referentes ao aparecimento da comida;
#^[Permissão para se fazer ressurgir uma nova comida, ação anterior da comida, ação atual da comida];
NewMusicUnlocked = -1						#Recebe o valor [índice] de uma música desbloqueada pela coleta do disco;
Retry = 0										#Rebebe a certificação que o jogador perdeu e permite a abertura de um novo layer;
WinLayout = 0									#Rebebe a certificação que o jogador venceu (o que é IMPOSSÍVEL) e permite a abertura de um novo layer;
Menu = 1											#Rebebe a certificação que o jogador quer ir para o menu inicial e permite a abertura dste layer;
SelectMenu = 0									#Rebebe o valor referente à qual sub-layer o jogador deseja entrar;
#^(0 == Jogo, 1 == Customizar, 2 == Loja, 3 == Opções (Configurações), 4 == Créditos/Cheat Zone, 5 == Sair);

BgColor = ((0,0,0))											#Recebe a cor de fundo do jogo (rgb);
SnakeColor = ((100,100,100))								#Recebe a cor da cobra (rgb);
SnakeHeadColor = ((0,0,0))									#Recebe a cor da cabeça da cobra (rgb);
SnakeBody = [(380, 340), (380, 360), (380, 380)]	#Recebe as coordenadas dos quadrados (canto superior esquerdo) que compõe a cobra;
SnakeDraw = pygame.Surface((20, 20))					#Define um objeto genérico com tamanho de 20px X 20px, representando um quadro da cobra;
SnakeDraw.fill(SnakeColor)									#Pinta esse objeto segundo a cor da cobra;

DirMovement = 1			#Define a direção do movimento da cobra;
Zawarudo = [1, 0, 0]		#Define os valores necessários para o funcionamento da parada temporal;
#^[Direção que a cobra estava andando, valores usados para alinhar a execução simultânea de som e imagem do efeito];
Invulnerability = 0		#Define o uso (gastar) do escudo;
InvulnerabilityFix = 0	#Define o uso ilimitado da invulnerabilidade (via cheat);
NewRecord = 0				#Define quando o jogador quebrou seu récorde;
UseItem = [None,None]	#Inventário usado na partida;
#^Existem dois tipos de item {rápidos == ativados com uma tecla}, {fixos == efeitos constantes ou automáticos com durabilidade contínua (ou até sua ativação) durante a partida}; 
CoinSummonRange = 0		#Define a probabilidade de surgirem diferentes itens (Comida/moedas/discos);
SnakeReborn = 0			#Define o uso (gastar) da ressurreição;

FoodCoordinates = (0, 0)				#Define as novas coordenadas onde surgira a comida;
FoodDraw = pygame.Surface((20, 20))	#Define um objeto genérico com tamanho de 20px X 20px, representando a comida; 
FoodDraw.fill((150, 0, 0))				#Pinta esse objeto de vermelho-escuro;

KeyboardPauseMusic = 0	#Define o bloqueio da parte teclado usada para trocar de música; 
KeyboardPauseStore = 0	#Define o bloqueio da parte teclado usada para comprar/vender um item;
PauseGame = 0				#Define o pausamento do jogo;

AtualizateData = 0	#Permite ao programa ler o Banco de Dados;
InputCheat = []		#Lista de caracteres usados para ferificar o êxito de um cheat;
#^Usado para facilitar na apresentação do trabalho, não trapaceie, ISSO É FEIO ((╬◣﹏◢))!

#Salva todas as cores padrão inclusas no sistema:
SysColors = [0,0,0,0,0,0,0,0,0]
SysColors[0] = ("Null", (60,60,60))	
SysColors[1] = ("Branco", (255,255,255))
SysColors[2] = ("Vermelho", (255,0,0))
SysColors[3] = ("Verde", (0,255,0))
SysColors[4] = ("Azul", (0,0,255))
SysColors[5] = ("Amarelo", (255,255,0))
SysColors[6] = ("Ciano", (0,255,255))
SysColors[7] = ("Rosa", (255,0,255))
SysColors[8] = ("Preto", (0,0,0))
#------------------------------------------------

#Salva todas as variáveis usadas para a customização:
SelectCustom = 0				#Recebe um valor referente à qual coisa o jogador quer customizar;
#^[0 == Corpo da cobra, 1 == Cabeça da cobra, 2 == Cor de fundo];
SelectCustomSnake = 1		#Seleciona o índice da cor que será usada no corpo da cobra;
SelectCustomSnakeHead = 0	#Seleciona o índice da cor que será usada na cabeça da cobra;
SelectCustomBg = 8			#Seleciona o índice da cor que será usada no plano de fundo;
#---------------------------------------------------

#Salva todas as variáveis usadas para a customização:
SelectOptions = 0				#Recebe um valor referente à qual coisa o jogador quer modificar;
SelectOptionsGrid = 0		#Seleciona o tipo de grade usada para delimitar o cenário;
SelectOptionsTime = False	#Permite ao jogador ver o tempo da partida;
SelectOptionsScore = True	#Permite ao jogador ver sua pontuação;
SelectOptionsSound = 50		#Recebe a entrada com o volume do som;
SelectOptionsMusic = 10		#Recebe a entrada com o volume da música;
#---------------------------------------------------

#Salva todos os sons e efeitos sonóros usados no decorrer do jogo:
SoundPlaylist = [0,0,0,0,0,0,0,0]
SoundPlaylist[0] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/Do_You_Lose.mp3")
SoundPlaylist[1] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/High_Score.mp3")
SoundPlaylist[2] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/Lets_Go.mp3")
SoundPlaylist[3] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/Player_1_Get_Ready.mp3")
SoundPlaylist[4] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/ZA_WARUDO.mp3")
SoundPlaylist[5] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/Coin_Sound_Effect.mp3")
SoundPlaylist[6] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/Cash_Register_Sound_Effect.mp3")
SoundPlaylist[7] = pygame.mixer.Sound("GELADEIRA_ELETROLUX/Reborn_Sound.mp3")
SoundPlaylist[0].set_volume(SelectOptionsSound / 100)
SoundPlaylist[1].set_volume(SelectOptionsSound / 100)
SoundPlaylist[2].set_volume(SelectOptionsSound / 100)
SoundPlaylist[3].set_volume(SelectOptionsSound / 100)
SoundPlaylist[3].set_volume(SelectOptionsSound / 100)
SoundPlaylist[4].set_volume(SelectOptionsSound / 100)
SoundPlaylist[5].set_volume(SelectOptionsSound / 100)
SoundPlaylist[6].set_volume(SelectOptionsSound / 100)
SoundPlaylist[7].set_volume(SelectOptionsSound / 100)
#-----------------------------------------------------------------

NewPlaylistIndex = 0		#Índice da música atual;
LastPlaylistIndex = -1	#Índice da música anterior;

#Salva todos as músicas disponíveis do jogo:
MusicPlaylist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MusicPlaylist[0] = ("SOUNDTRACK/2-Minutes-To-Midnight.mp3", "2 Minutes To Midnight - Iron Maiden")
MusicPlaylist[1] = ("SOUNDTRACK/Another-Brick-In-The-Wall.mp3", "Another Brick In The Wall - Pink Floyd")
MusicPlaylist[2] = ("SOUNDTRACK/Are-You-Gonna-Go-My-Way.mp3", "Are You Gonna Go My Way - Lenny Kravitz")
MusicPlaylist[3] = ("SOUNDTRACK/Black-Night.mp3", "Black Night - Deep Purple")
MusicPlaylist[4] = ("SOUNDTRACK/Burn.mp3", "Burn - Deep Purple")
MusicPlaylist[5] = ("SOUNDTRACK/Carry-On.mp3", "Carry On - Angra")
MusicPlaylist[6] = ("SOUNDTRACK/Carry-On-Wayward-Son.mp3", "Carry On Wayward Son - Kansas")
MusicPlaylist[7] = ("SOUNDTRACK/Crazy-Train.mp3", "Crazy Train - Ozzy Osbourne")
MusicPlaylist[8] = ("SOUNDTRACK/Detroit-Rock-City.mp3", "Detroit Rock City - Kiss")
MusicPlaylist[9] = ("SOUNDTRACK/Dirty-Deeds-Done-Dirt-Cheap.mp3", "Dirty Deeds Done Dirt Cheap - AC/DC")
MusicPlaylist[10] = ("SOUNDTRACK/Dont-Fear-The-Reaper.mp3", "Dont Fear The Reaper - Blue Oyster Cult")
MusicPlaylist[11] = ("SOUNDTRACK/Enter-Sandman.mp3", "Enter Sandman - Metallica")
MusicPlaylist[12] = ("SOUNDTRACK/Hard-Technology.mp3", "Hard Technology - Half-Life 1 (Kelly Bailey)")
MusicPlaylist[13] = ("SOUNDTRACK/Heartbreaker.mp3", "Heartbreaker - Led Zeppelin")
MusicPlaylist[14] = ("SOUNDTRACK/Holy-Diver.mp3", "Holy Diver - Dio")
MusicPlaylist[15] = ("SOUNDTRACK/I-Love-Rock-N-Roll.mp3", "I Love Rock 'N Roll - The Arrows")
MusicPlaylist[16] = ("SOUNDTRACK/Immigrant-Song.mp3", "Immigrant Song - Led Zeppelin")
MusicPlaylist[17] = ("SOUNDTRACK/Im-The-One.mp3", "I'm The One - Van Hallen")
MusicPlaylist[18] = ("SOUNDTRACK/Killing-In-The-Name.mp3", "Killing In The Name - Rage Against The Machine")
MusicPlaylist[19] = ("SOUNDTRACK/Layla.mp3", "Layla - Derik And The Dominos")
MusicPlaylist[20] = ("SOUNDTRACK/Master-Of-The-Puppets.mp3", "Master Of The Puppets - Metallica")
MusicPlaylist[21] = ("SOUNDTRACK/Mirror-Mirror.mp3", "Mirror Mirror - Blind Guardian")
MusicPlaylist[22] = ("SOUNDTRACK/More-Than-A-Feeling.mp3", "More Than A Feeling - Boston")
MusicPlaylist[23] = ("SOUNDTRACK/No-One-Like-You.mp3", "No One Like You - Scorpions")
MusicPlaylist[24] = ("SOUNDTRACK/Nova-Era.mp3", "Nova Era - Angra")
MusicPlaylist[25] = ("SOUNDTRACK/Paranoid.mp3", "Paranoid - Black Sabbath")
MusicPlaylist[26] = ("SOUNDTRACK/Perfect-Strangers.mp3", "Perfect Strangers - Deep Purple")
MusicPlaylist[27] = ("SOUNDTRACK/Rainbow-In-The-Dark.mp3", "Rainbow In The Dark - Dio")
MusicPlaylist[28] = ("SOUNDTRACK/Rock-And-Roll.mp3", "Rock And Roll - Led Zeppelin")
MusicPlaylist[29] = ("SOUNDTRACK/Rock-N-Roll-All-Nite.mp3", "Rock 'N Roll All Nite - Kiss")
MusicPlaylist[30] = ("SOUNDTRACK/Spirit-In-The-Sky.mp3", "Spirit In The Sky - Norman Greenbaum")
MusicPlaylist[31] = ("SOUNDTRACK/The-Kids-Arent-Alright.mp3", "The Kids Arent Alright - The Offspring")
MusicPlaylist[32] = ("SOUNDTRACK/The-Trooper.mp3", "The Trooper - Iron Maiden")
MusicPlaylist[33] = ("SOUNDTRACK/Through-The-Fire-And-Flames.mp3", "Through The Fire And Flames - Dragon Force")
MusicPlaylist[34] = ("SOUNDTRACK/Thunderstruck.mp3", "Thunderstruck - AC/DC")
MusicPlaylist[35] = ("SOUNDTRACK/Welcome-To-The-Jungle.mp3", "Welcome To The Jungle - Guns 'N Roses")
pygame.mixer.music.set_volume(SelectOptionsMusic / 100)
#MusicPlaylist[i] = ("Caminho relativo do arquivo", "Música - Compositor")
#------------------------------------------

#Salva todos as imagens utilizadas no jogo{
Galery = [[0,0], [[0,0,0], [0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]]
#Imagens que aparecem durante o jogo:
Galery[0][0] = pygame.image.load(r"IMAGES/JoJo-Effect.png")
Galery[0][1] = pygame.image.load(r"IMAGES/Disc.png")
#------------------------------------

#Imagens dos itens de efeito rápido:
Galery[1][0][0] = (pygame.image.load(r"IMAGES/Zawarudo_face.jpg"), "Zawarudo", 4, 3)
Galery[1][0][1] = (pygame.image.load(r"IMAGES/Buraco_de_minhoca.png"), "Buraco de minhoca", 1, 1)
#Galery[1][<0>][1] =  (Arquivo, Nome, Preço de Compra, Preço de Venda)
#-----------------------------------

#Imagens dos itens de efeito contínuo:
Galery[1][1][0] = (pygame.image.load(r"IMAGES/Livro_encantado.png"), "Encantamento de Fortuna", 5, 3)
Galery[1][1][1] = (pygame.image.load(r"IMAGES/Potion_of_Growth.png"), "Pocao de Crescimento", 3, 2)
Galery[1][1][2] = (pygame.image.load(r"IMAGES/Escudo.png"), "Escudo", 3, 2)
Galery[1][1][3] = (pygame.image.load(r"IMAGES/Monster Reborn.jpg"), "Ressurreicao", 8, 7)
#Galery[1][<1>][1] =  (Arquivo, Nome, Preço de Compra, Preço de Venda)
#------------------------------------

#Imagens dos discos de música da loja:
Galery[1][2][0] = (pygame.image.load(r"DISCS/Powerslave.jpg"), "2 Minutes To Midnight - Iron Maiden","Powerslave - 1984", 1)
Galery[1][2][1] = (pygame.image.load(r"DISCS/The_Wall.jpg"), "Another Brick In The Wall - Pink Floyd","The Wall - 1979", 1)
Galery[1][2][2] = (pygame.image.load(r"DISCS/Are_You_Gonna_Go_My_Way.jpg"), "Are You Gonna Go My Way - Lenny Kravitz", "Are You Gonna Go My Way - 1993", 1)
Galery[1][2][3] = (pygame.image.load(r"DISCS/Deep_Purple_In_Rock.jpg"), "Black Night - Deep Purple", "Deep Purple In Rock - 1970", 1)
Galery[1][2][4] = (pygame.image.load(r"DISCS/Burn.jpg"), "Burn - Deep Purple", "Burn - 1974", 1)
Galery[1][2][5] = (pygame.image.load(r"DISCS/Angels_Cry.jpg"), "Carry On - Angra", "Angels Cry - 1993", 1)
Galery[1][2][6] = (pygame.image.load(r"DISCS/Leftoverture.jpg"), "Carry On My Wayward Son - Kansas", "Leftoverture - 1976", 1)
Galery[1][2][7] = (pygame.image.load(r"DISCS/Blizzard_Of_Ozz.jpg"), "Crazy Train - Ozzy Osbourne", "Blizzard Of Ozz - 1980", 1)
Galery[1][2][8] = (pygame.image.load(r"DISCS/Destroyer.jpg"), "Detroit Rock City - Kiss", "Destroyer - 1974", 1)
Galery[1][2][9] = (pygame.image.load(r"DISCS/Dirty_Deeds_Done_Dirt_Cheap.jpg"), "Dirty Deeds Done Dirt Cheap - AC/DC", "Dirty Deeds Done Dirt Cheap - 1976", 1)
Galery[1][2][10] = (pygame.image.load(r"DISCS/Agents_Of_Fortune.jpg"), "Dont Fear The Reaper - Blue Oyster Cult", "Agents Of Fortune - 1976", 1)
Galery[1][2][11] = (pygame.image.load(r"DISCS/Metallica.jpg"), "Enter Sandman - Metallica", "Metallica (Black Album) - 1991", 1)
Galery[1][2][12] = (pygame.image.load(r"DISCS/Half_Life.jpg"), "Hard Technology - Half-Life 1 (Kelly Bailey)", "Half Life - 1998", 1)
Galery[1][2][13] = (pygame.image.load(r"DISCS/Led_Zeppelin_II.jpg"), "Heartbreaker - Led Zeppelin", "Led Zeppelin II - 1969", 1)
Galery[1][2][14] = (pygame.image.load(r"DISCS/Holy_Diver.jpg"), "Holy Diver - Dio", "Holy Diver - 1983", 1)
Galery[1][2][15] = (pygame.image.load(r"DISCS/First_Hit.jpg"), "I Love Rock 'N Roll - The Arrows", "First Hit - 1976", 1)
Galery[1][2][16] = (pygame.image.load(r"DISCS/Led_Zeppelin_III.jpg"), "Immigrant Song - Led Zeppelin", "Led Zeppelin III - 1970", 1)
Galery[1][2][17] = (pygame.image.load(r"DISCS/Van_Hallen.jpg"), "I'm The One - Van Hallen", "Van Hallen 1978", 1)
Galery[1][2][18] = (pygame.image.load(r"DISCS/Rage_Aganist_The_Machine.jpg"), "Killing In The Name - Rage Against The Machine", "Rage Against The Machine - 1992", 1)
Galery[1][2][19] = (pygame.image.load(r"DISCS/Layla_And_Other_Assorted_Love_Songs.jpg"), "Layla - Derik And The Dominos", "Layla And Other Assorted Love Songs - 1970", 1)
Galery[1][2][20] = (pygame.image.load(r"DISCS/Master_Of_Puppets.jpg"), "Master Of Puppets - Metallica", "Master Of Puppets - 1986", 1)
Galery[1][2][21] = (pygame.image.load(r"DISCS/Nightfall_In_The_Middle_Earth.jpg"), "Mirror Mirror - Blind Guardian", "Nightfall In The Middle Earth - 1998", 1)
Galery[1][2][22] = (pygame.image.load(r"DISCS/Boston.jpg"), "More Than A Feeling - Boston", "Boston - 1976", 1)
Galery[1][2][23] = (pygame.image.load(r"DISCS/Blackout.jpg"), "No One Like You - Scorpions", "Blackout - 1982", 1)
Galery[1][2][24] = (pygame.image.load(r"DISCS/Rebirth.jpg"), "Nova Era - Angra", "Rebirth - 2001", 1)
Galery[1][2][25] = (pygame.image.load(r"DISCS/Paranoid.jpg"), "Paranoid - Black Sabbath", "Paranoid - 1970", 1)
Galery[1][2][26] = (pygame.image.load(r"DISCS/Perfect_Strangers.jpg"), "Perfect Strangers - Deep Purple", "Perfect Strangers - 1984", 1)
Galery[1][2][27] = (pygame.image.load(r"DISCS/Holy_Diver.jpg"), "Rainbow In The Dark - Dio", "Holy Diver - 1983", 1)
Galery[1][2][28] = (pygame.image.load(r"DISCS/Led_Zeppelin_IV.jpg"), "Rock And Roll - Led Zeppelin", "Led Zeppelin IV - 1971", 1)
Galery[1][2][29] = (pygame.image.load(r"DISCS/Dressed_To_Kill.jpg"), "Rock 'N Roll All Nite", "Dressed To Kill - 1975", 1)
Galery[1][2][30] = (pygame.image.load(r"DISCS/Spirit_In_The_Sky.jpg"), "Spirit In The Sky - Norman Greenbaum", "Spirit In The Sky - 1969", 1)
Galery[1][2][31] = (pygame.image.load(r"DISCS/Americana.jpg"), "The Kids Arent Alright - The Offspring", "Americana - 1998", 1)
Galery[1][2][32] = (pygame.image.load(r"DISCS/Piece_Of_Mind.jpg"), "The Trooper - Iron Maiden", "Piece Of Mind - 1983", 1)
Galery[1][2][33] = (pygame.image.load(r"DISCS/Inhuman_Rampage.jpg"), "Through The Fire And Flames - Dragon Force", "Inhuman Rampage - 2005", 1)
Galery[1][2][34] = (pygame.image.load(r"DISCS/The_Razors_Edge.jpg"), "Thunderstruck - AC/DC", "The Razors Edge - 1990", 1)
Galery[1][2][35] = (pygame.image.load(r"DISCS/Appetite_For_Destruction.jpg"), "Welcome To The Jungle - Guns 'N Roses", "Appetite For Destruction - 1987", 1)
#Galery[1][<2>][1] =  (Arquivo, Nome, Artista - Ano, Preço de Compra)
#------------------------------------
#-----------------------------------------}

#Seções da loja{
SelectStoreColumn = [0,0,0]

#Seletores de índice:
StoreIndexSection = 0	#Índice da seção (itens rápidos, itens contínuos, músicas);
StoreIndexItem = 0		#Índice dos itens (itens rápidos --> (Zawarudo, Buraco de minhoca));
#--------------------

#Seção de itens rápidos:
SelectStoreColumn[0] = [Galery[1][0][0],Galery[1][0][1]]
#----------------------

#Seção de itens contínuos:
SelectStoreColumn[1] = [Galery[1][1][0],Galery[1][1][1],Galery[1][1][2],Galery[1][1][3]]
#------------------------

#Seção de músicas:
SelectStoreColumn[2] = [
Galery[1][2][0],Galery[1][2][1],Galery[1][2][2],Galery[1][2][3],Galery[1][2][4],Galery[1][2][5],
Galery[1][2][6],Galery[1][2][7],Galery[1][2][8],Galery[1][2][9],Galery[1][2][10],Galery[1][2][11],
Galery[1][2][12],Galery[1][2][13],Galery[1][2][14],Galery[1][2][15],Galery[1][2][16],Galery[1][2][17],
Galery[1][2][18],Galery[1][2][19],Galery[1][2][20],Galery[1][2][21],Galery[1][2][22],Galery[1][2][23],
Galery[1][2][24],Galery[1][2][25],Galery[1][2][26],Galery[1][2][27],Galery[1][2][28],Galery[1][2][29],
Galery[1][2][30],Galery[1][2][31],Galery[1][2][32],Galery[1][2][33],Galery[1][2][34], Galery[1][2][35]]
#-----------------
#--------------}

#Função de atualização do banco de dados:
def UpdateData(reset, section, var, val):
	#Carrega e classifica os dados:
	with open("Database.json", "r") as x:
		Data = json.load(x)
		DataI = Data["Itens"]
		DataS = Data["GameSaves"]
		DataM = Data["Musics"]
	#-----------------------------
	
	#Recupera os dedos do jogo:
	ScoreRecord = DataS["Record"][0]
	TimeScoreRecord = DataS["Record"][1]
	Coins = DataS["Coins"]
	Backpack = [DataI["Zawarudo"],DataI["Buraco de minhoca"],DataI["Encantamento de Fortuna"],DataI["Pocao de Crescimento"],DataI["Escudo"],DataI["Ressurreicao"]]
	MusicUnlockedList = DataM["List"]
	#--------------------------

	#Se for dada a ordem de reiniciar:
	if reset:
		#Verifica a seção da variável que vai ser apagada;
		if section == "GameSaves" or section == "all":
			#Verifica qual variável vai ser apagada;
			if var == "ScoreRecord" or var == "all":
				ScoreRecord = 0
			if var == "TimeScoreRecord" or var == "all":
				TimeScoreRecord = "0:0'0.00"
			if var == "Coins" or var == "all":
				Coins = 0
		if section == "Itens" or section == "all":
			if var == "Zawarudo" or var == "all":
				Backpack[0] = 0
			if var == "Buraco de minhoca" or var == "all":
				Backpack[1] = 0
			if var == "Encantamento de Fortuna" or var == "all":
				Backpack[2] = 0
			if var == "Pocao de Crescimento" or var == "all":
				Backpack[3] = 0
			if var == "Escudo" or var == "all":
				Backpack[4] = 0
			if var == "Ressurreicao" or var == "all":
				Backpack[5] = 0
		if section == "Musics" or section == "all":
			if var == "MusicUnlockedList" or var == "all":
				MusicUnlockedList = [0,1,2,4,6,7,8,11,12,14,22,28,30,31,34]
	#---------------------------------

	#Se for dada a ordem de atualizar:
	if not(reset):
		#Verifica qual variável vai receber determinado valor;
		if var == "ScoreRecord":
			ScoreRecord = val
		if var == "TimeScoreRecord":
			TimeScoreRecord = val
		if var == "Coins":
			Coins = Coins + val
		if var == "Zawarudo" or var == "all": 
			Backpack[0] = Backpack[0] + val
		if var == "Buraco de minhoca" or var == "all": 
			Backpack[1] = Backpack[1] + val
		if var == "Encantamento de Fortuna" or var == "all": 
			Backpack[2] = Backpack[2] + val
		if var == "Pocao de Crescimento" or var == "all":
			Backpack[3] = Backpack[3] + val
		if var == "Escudo" or var == "all":
			Backpack[4] = Backpack[4] + val
		if var == "Ressurreicao" or var == "all":
			Backpack[5] = Backpack[5] + val
		if var == "MusicUnlockedList": 
			MusicUnlockedList.append(val)
	#---------------------------------

	#Salva os valores em seus respectivos grupos{
	#Salva o grupo dos itens:
	Itens = {
		"Zawarudo": Backpack[0],
		"Buraco de minhoca": Backpack[1],
		"Encantamento de Fortuna": Backpack[2],
		"Pocao de Crescimento": Backpack[3],
		"Escudo": Backpack[4],
		"Ressurreicao": Backpack[5]
	}
	#------------------------

	#Salva o grupo dos récordes do jogador:
	GameSaves = {
		"Record": ((ScoreRecord, TimeScoreRecord)),
		"Coins": Coins
	}
	#--------------------------------------


	Musics = {
		"List": MusicUnlockedList
	}
	#-------------------------------------------}

	#Reúne todos os grupos num só, que será escrito:
	AllData = {
		"Itens": Itens,
		"GameSaves": GameSaves,
		"Musics": Musics
	}
	#-----------------------------------------------

	#Reescreve o banco de dados:
	with open("Database.json", "w") as x:	#Abre o documento do banco de dados (JSON) no modo escrita;
		json.dump(AllData, x, sort_keys=True, indent=3, separators=(",",":"))
		#^Escreve o grupo de dados em: (Ordem Alfabética, identação de 3 espaços, separados por ":" e ",");
	#---------------------------

#Função usada para ler o nome da tecla pressionada pelo jogador:
def ReadKey():
	key = None
	while not(key):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			#^Evento defechamento de tela;
			if event.type == pygame.KEYDOWN:
				return pygame.key.name(event.key)	#Retorna o nome da tecla;
#---------------------------------------------------------------

while True:	#Abre um Loop Constante (Cerca de 4 milisegundos para dar o loop);
	if AtualizateData:								#Se (Permissão para a atualiazção das variáveis) == True:
		with open("Database.json", "r") as x:	#Atualiza as variáveis lendo do banco de dados;
			Data = json.load(x)
			DataI = Data["Itens"]
			DataS = Data["GameSaves"]
			DataM = Data["Musics"]
		ScoreRecord = DataS["Record"][0]
		TimeScoreRecord = DataS["Record"][1]
		Coins = DataS["Coins"]
		Backpack = [DataI["Zawarudo"],DataI["Buraco de minhoca"],DataI["Encantamento de Fortuna"],DataI["Pocao de Crescimento"],DataI["Escudo"],DataI["Ressurreicao"]]
		MusicUnlockedList = DataM["List"]
		AtualizateData = 0							#Nega a permissão ao programa ler o Banco de Dados;

	Key = pygame.key.get_pressed()				#Recebe uma lista com o índice das teclas pressionadas;
	
	#Bloco de troca de música:
	if (Key[ord("x")] or Key[ord(".")]) and KeyboardPauseMusic == 0 and Zawarudo[0] != 0:	#Se teclas "x" ou "." forem pressionadas, o teclado possuír a permissão para executar e isso não está acontecendo em uma parada temporal:
		NewPlaylistIndex = NewPlaylistIndex + 1				#Passa para a próxima música da lista;
		while not(NewPlaylistIndex in MusicUnlockedList):	#Se o jogador não possír a próxima música:
			NewPlaylistIndex = NewPlaylistIndex + 1			#Avança para a próxima;
			if NewPlaylistIndex > 35:								#Se o programa chegar na última música:
				NewPlaylistIndex = 0									#O ciclo retorna à primeira música;
		pygame.mixer.music.load(MusicPlaylist[NewPlaylistIndex][0])	#Carrega a nova música;
		pygame.mixer.music.play(1)									#Toca ela uma vez;
		LastPlaylistIndex = NewPlaylistIndex					#Atualiza o valor da última música;
		KeyboardPauseMusic = 1										#Bloqueia o teclado (para que o usuário troque apenas uma música por clique);
	
	if (Key[ord("z")] or Key[ord(",")]) and KeyboardPauseMusic == 0 and Zawarudo[0] != 0:	#Se teclas "z" ou "," forem pressionadas, o teclado possuír a permissão para executar e isso não está acontecendo em uma parada temporal:
		NewPlaylistIndex = NewPlaylistIndex - 1				#Passa para a música anterior da lista;
		while not(NewPlaylistIndex in MusicUnlockedList):	#Se o jogador não possír a música anterior:
			NewPlaylistIndex = NewPlaylistIndex - 1			#Retorna para a anterior;
			if NewPlaylistIndex < 0:								#Se o programa chegar na primeira música:
				NewPlaylistIndex = 35								#O ciclo retorna à última música;
		pygame.mixer.music.load(MusicPlaylist[NewPlaylistIndex][0])	#Carrega a nova música;
		pygame.mixer.music.play(1)									#Toca ela uma vez;
		LastPlaylistIndex = NewPlaylistIndex					#Atualiza o valor da última música;
		KeyboardPauseMusic = 1										#Bloqueia o teclado (para que o usuário troque apenas uma música por clique);

	if Key[ord("z")] == 0 and Key[ord(",")] == 0 and Key[ord("x")] == 0 and Key[ord(".")] == 0: #Se nenhuma das teclas usadas para passar de música estiver pressionada:
		KeyboardPauseMusic = 0	#Desloqueia o teclado;

	if pygame.mixer.music.get_busy() == 0:											#Se nenhuma música estiver tocando (uma música acabou):
		NewPlaylistIndex = random.randint(0, 35)									#A nova música recebe um índice aleatório;
		if NewPlaylistIndex != LastPlaylistIndex:									#Se este índice for diferente do anterior:
			if NewPlaylistIndex in MusicUnlockedList:								#E estiver incluso na sua lista de músicas desbloqueadas:
				pygame.mixer.music.load(MusicPlaylist[NewPlaylistIndex][0])	#Carrega a nova música;
				pygame.mixer.music.play(1)												#Toca ela uma vez;
		LastPlaylistIndex = NewPlaylistIndex										#Atualiza o valor da última música;
	#-------------------------
	
	#Menu inicial:
	if Menu == 1:	#Se o jogador ordenar a abertura deste layer:
		#Definições iniciais de variáveis e uso de itens:
		FoodCoordinates = ((random.randint(0,760)//20 * 20), ((random.randint(20,640))//20 * 20)) #Já vai carregando a posição da comida;
		SnakeBody = [(380, 340), (380, 360), (380, 380)]														#Define o corpo da cobra (tamanho 3);
		DirMovement = 1																									#Define a direção do movimento como: cima;
		
		if (UseItem[1] == "Pocao de Crescimento") and (DataI[UseItem[1]] > 0):			#Se a "Pocao de Crescimento" estiver equipada:
			SnakeBody = [(380, 340), (380, 360), (380, 380), (380, 400), 
							 (380, 420), (380, 440), (380, 460), (380, 480), 
							 (380, 500), (380, 520), (380, 540), (380, 560)]					#Redefine o corpo da cobra (tamanho 12)
		Invulnerability = 0																				#Sua invulnerabilidade é negada;
		if (UseItem[1] == "Escudo") and (DataI[UseItem[1]] > 0):								#Se o "Escudo" estiver equipado:
			Invulnerability = 1																			#Sua invulnerabiliade é validada;
		CoinSummonRange = 150																			#Determina o alcance da probabilidade de aparecer uma comida especial (Moedas e Discos);
		if (UseItem[1] == "Encantamento de Fortuna") and (DataI[UseItem[1]] > 0):		#Se o "Encantamento de Fortuna" estiver equipado:
			CoinSummonRange = CoinSummonRange / 2													#Divide pala metade a dificuldade de aparecer uma comida especial;
		SnakeReborn = 0																					#Sua ressurreição é negada;
		if (UseItem[1] == "Ressurreicao") and (DataI[UseItem[1]] > 0):						#Se a "Ressurreição" estiver equipada:
			SnakeReborn = 1																				#Sua ressurreição é validada;
		#------------------------------------------------

		#Leitura de Eventos:
		for event in pygame.event.get():												#Verifica todos os eventos que estão acontecendo:
			if event.type == pygame.QUIT:												#Se o jogador apertar para sair ("x" no canto superior da tela);
				pygame.quit()																#Fecha o pygame;
				exit(0)																		#Encerra a execução do python;
			if event.type == pygame.KEYDOWN:											#Se uma tecla for pressionada:
				if event.key == pygame.K_UP or event.key == pygame.K_w:		#E esta tecla for "Seta pra cima" ou "w":
					SelectMenu = SelectMenu - 1										#Altera (sobe) o valor da variável seletora de layers;
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:	#E esta tecla for "Seta pra baixo" ou "s":
					SelectMenu = SelectMenu + 1										#Altera (desce) o valor da variável seletora de layers;
				if event.key == pygame.K_SPACE:										#E esta tecla for "Espaço":
					Menu = 0																	#Sai do menu inicial;
					if SelectMenu == 0:													#Se a ação escolhida foi jogar:
						SoundPlaylist[2].play()											#Tocar som "Lets GO!";
						pygame.time.delay(200)											#Aguarda 2/10 de segundo;
			if SelectMenu < 0:															#Se o menu ficar menor que seu alcance:
				SelectMenu = 5																#Ele dá o giro e recebe o valor máximo;
			if SelectMenu > 5:															#Se o menu ficar maior que seu alcance:
				SelectMenu = 0																#Ele dá o giro e recebe o valor mínimo;
		#-------------------

		#Parte gráfica (O que aparecerá na tela para o jogador){
		#Título do jogo:
		Window.fill((0,0,0))													#Pinta o fundo de Preto (Cor fixa do fundo);
		FontSys = pygame.font.SysFont("Stencil", 120)				#Recebe a fonte "Stencil" tamanho 120;
		Font = FontSys.render("Snake-Rock", 5, (SysColors[1][1]))#O texto recebe a string "Snake-Rock", cor branca;
		Window.blit(Font,(30,150))											#Escreve essa string na tela;
		#---------------

		#Opções de seleção:
		FontSys = pygame.font.SysFont("Stencil", 30)								#Recebe a fonte "Stencil" tamanho 30;
		Font = FontSys.render("Mete ficha!", 1, (SysColors[1][1]))			#O texto recebe a string "Mete ficha!", cor branca;
		if SelectMenu == 0:																#Se o seletor marcar esta opção:
			Font = FontSys.render("Mete ficha!", 1, ((SysColors[2][1])))	#A cor do texto se altera para vermelho;
		Window.blit(Font,(300,350))													#Escreve essa string na tela;
		
		Font = FontSys.render("Customizar", 1, (SysColors[1][1]))		#O texto recebe a string "Customizar", cor branca;
		if SelectMenu == 1:															#Se o seletor marcar esta opção:
			Font = FontSys.render("Customizar", 1, ((SysColors[2][1])))	#A cor do texto se altera para vermelho;
		Window.blit(Font,(300,400))												#Escreve essa string na tela;

		Font = FontSys.render("Loja", 1, (SysColors[1][1]))		#O texto recebe a string "Loja", cor branca;
		if SelectMenu == 2:													#Se o seletor marcar esta opção:
			Font = FontSys.render("Loja", 1, ((SysColors[2][1])))	#A cor do texto se altera para vermelho;
		Window.blit(Font,(360,450))										#Escreve essa string na tela;

		Font = FontSys.render("Opções", 1, (SysColors[1][1]))			#O texto recebe a string "Opções", cor branca;
		if SelectMenu == 3:														#Se o seletor marcar esta opção:
			Font = FontSys.render("Opções", 1, ((SysColors[2][1])))	#A cor do texto se altera para vermelho;
		Window.blit(Font,(340,500))											#Escreve essa string na tela;

		Font = FontSys.render("Créditos", 1, (SysColors[1][1]))			#O texto recebe a string "Créditos", cor branca;
		if SelectMenu == 4:															#Se o seletor marcar esta opção:
			Font = FontSys.render("Créditos", 1, ((SysColors[2][1])))	#A cor do texto se altera para vermelho;
		Window.blit(Font,(320,550))												#Escreve essa string na tela;

		Font = FontSys.render("Sair", 1, (SysColors[1][1]))		#O texto recebe a string "Sair", cor branca;
		if SelectMenu == 5:													#Se o seletor marcar esta opção:
			Font = FontSys.render("Sair", 1, ((SysColors[2][1])))	#A cor do texto se altera para vermelho;
		Window.blit(Font,(360,600))										#Escreve essa string na tela;
		#------------------
	#------------------------------------------------------}

	#O jogo em si:
	if SelectMenu == 0 and Menu == 0 and Retry == 0 and PauseGame == 0 and WinLayout == 0:
	#^Se o jogador ordenar a abertura deste layer, o jogador não está no menu, o jogador ainda não perdeu, o jogo não está pausado e o jogador ainda não venceu a partida:
		Window.fill(BgColor)			#Pinta o fundo com a cor escolhida pelo jogador;
		SnakeDraw.fill(SnakeColor)	#Preenche a cobra com a cor escolhida pelo jogador;
		
		#Leitura de eventos:
		for event in pygame.event.get():	#Verifica todos os eventos que estão acontecendo:
			#Sair do jogo:
			if event.type == pygame.QUIT:	#Se o jogador apertar para sair ("x" no canto superior da tela):
				pygame.quit()					#Fecha a execução do pygame;
				exit(0)							#Encerra o pyton;
			#-------------

			#Pause e itens rápidos:
			if event.type == pygame.KEYDOWN:		#Se uma tecla for pressionada:
				if event.key == pygame.K_SPACE:	#E esta tecla for "Espaço":
					PauseGame = 1						#Concede a permissão para pausar o jogo
					SoundPlaylist[3].play()			#Tocar som "Player 1, get ready..."
				
				elif event.key == pygame.K_h:		#E esta tecla for "h":
					if (UseItem[0] == "Buraco de minhoca") and (DataI[UseItem[0]] > 0):	#Se o item "Buraco de minhoca" estiver equipado e o jogador possuir pelo menos 1:
						SumonFood[1] = SumonFood[2]								#Recebe o valor da ação do item anterior;
						SumonFood[2] = random.randint(1, CoinSummonRange)	#Sorteia uma nova nova comida dentro do alconce imposto;
						SumonFood[0] = 1												#Autoriza o ciclo a realocar a comida;
						FoodDraw.fill((150,0,0))		#Pinta a comida de vermelho;
						if SumonFood[2] == 1:			#Se o valor sorteado for igual a 1:
							FoodDraw.fill((255,75,0))	#Pinta a comida de laranja;
						while SumonFood[0]:								#Enquanto for autorizada o realocamento da comida;
							for i in range(len(SnakeBody)-1):		#Passa por todas as partes do corpo da cobra:
								if FoodCoordinates == SnakeBody[i]:	#Se o novo local da comida já estiver ocupado pela cobra:
									FoodCoordinates = ((random.randint(0,760)//20 * 20), ((random.randint(20,640))//20 * 20))
									#^Sorteia um énuplo com (x, y) para a nova posição com valores inteiros múltiplos de 20;
								else:						#Caso o contrário (local livre):
									SumonFood[0] = 0	#Desautoria o realocamento e mantém o último valor sorteado;
						AtualizateData = 1										#Autoriza ao programa ler o Banco de Dados;
						UpdateData(0, "Itens", "Buraco de minhoca", -1)	#Desconta o item "Buraco de minhoca" usado, diretamente no banco de dados;

					if (UseItem[0] == "Zawarudo") and (DataI[UseItem[0]] > 0):	#Se o item "Zawarudo" estiver equipado e o jogador possuir pelo menos 1:
						pygame.mixer.music.pause()											#Pausa a música;
						Zawarudo[0] = 0														#Define que foi iniciada a parada temporal;
						Zawarudo[1] = 1														#Autoriza o uso da imagem de efeito;
						AtualizateData = 1													#Autoriza o programa ler o Banco de Dados;
						UpdateData(0, "Itens", "Zawarudo", -1)							#Desconta o item "Zawarudo" usado, diretamente no banco de dados;
			#----------------------
		#------------------
		
		#Detecção de eventos (Vitória e Récorde):
		if len(SnakeBody) >= 1248 or Key[ord("u")]:	#Se o corpo da cobra ocupar todo o tabuleiro (ou a tecla "u for pressionada", para mostrar a tela final na apresentação): 
			WinLayout = 1										#Decreta a vitória ao jogador;

		if (Score > 0) and ((Score > ScoreRecord) or (Score == ScoreRecord and TimePlayed < TimeScoreRecord)):	#Se a pontouação do jogador for > 0 e, seu placar é maior que o anterior ou igual com um tempo menor:
			UpdateData(0, "GameSaves", "ScoreRecord", Score)																		#Salva o novo récorde no banco de dados;
			UpdateData(0, "GameSaves", "TimeScoreRecord", TimePlayed)															#Salva o tempo deste récorde no banco de dados;
			AtualizateData = 1																												#Autoriza o programa ler o Banco de Dados;
			if not(NewRecord):																												#Se o jogador bateu o récorde nessa comida:
				SoundPlaylist[1].play()																										#Tocar som "HIGH SCORE!";
				NewRecord = not(NewRecord)																									#Nega que o som seja tocado novamente;
				#^Para o áudio ser usado quando o jogador bater o récorde anterior, e não a cada comida ganha acima do récorde anterior (ia ficar chato ouvir um áudio a cada comida);
		#----------------------------------------

		Key = pygame.key.get_pressed()	#Recebe uma lista com o índice das teclas pressionadas;
		if (Key[ord("w")] or Key[pygame.K_UP]) and not(Key[ord("s")]) and DirMovement != 2 and Zawarudo[0] != 2:
		#^Se a tecla "w" ou "seta pra cima", a tecla "s" não está sendo pressionada, a cobra não está se movimentando para baixo e na parada temporal, a cobra não estava indo para baixo;
			DirMovement = 1	#Direção do movimento = cima;
			Zawarudo[0] = 1	#Desabilita o uso do item "Zawarudo";
			if SelectOptionsMusic != 0:	#Se o volume da música não for 0:
				pygame.mixer.music.unpause()	#Despausa a música;
		elif (Key[ord("s")] or Key[pygame.K_DOWN]) and not(Key[ord("w")]) and DirMovement != 1 and Zawarudo[0] != 1:
			DirMovement = 2	#Direção do movimento = baixo;
			Zawarudo[0] = 2	#Desabilita o uso do item "Zawarudo";
			if SelectOptionsMusic != 0:	#Se o volume da música não for 0:
				pygame.mixer.music.unpause()	#Despausa a música;
		elif (Key[ord("a")] or Key[pygame.K_LEFT]) and not(Key[ord("d")]) and DirMovement != 4 and Zawarudo[0] != 4:
			DirMovement = 3	#Direção do movimento = esquerda;
			Zawarudo[0] = 3	#Desabilita o uso do item "Zawarudo";
			if SelectOptionsMusic != 0:	#Se o volume da música não for 0:
				pygame.mixer.music.unpause()	#Despausa a música;
		elif (Key[ord("d")] or Key[pygame.K_RIGHT]) and not(Key[ord("a")]) and DirMovement != 3 and Zawarudo[0] != 3:
			DirMovement = 4	#Direção do movimento = esquerda;
			Zawarudo[0] = 4	#Desabilita o uso do item "Zawarudo";
			if SelectOptionsMusic != 0:	#Se o volume da música não for 0:
				pygame.mixer.music.unpause()	#Despausa a música;
				
		if (SnakeBody[0] == FoodCoordinates):	#Se a cobra pegar uma comida:
			SumonFood[1] = SumonFood[2]			#Recebe o valor da ação do item anterior;
			SumonFood[2] = random.randint(1, CoinSummonRange)	#Sorteia uma nova nova comida dentro do alconce imposto;
			SumonFood[0] = 1												#Autoriza o ciclo a realocar a comida;
			FoodCoordinates = ((random.randint(0,760)//20 * 20), ((random.randint(20,640))//20 * 20))
			FoodDraw.fill((150,0,0))							#Pinta a comida de vermelho;
			if SumonFood[2] >= 2 and SumonFood[2] <= 11:	#Se o valor sorteado for entre 2 e 11:
				FoodDraw.fill((255,75,0))						#Pinta a comida de laranja;
			elif SumonFood[2] == 1:								#Se o valor sorteado for 1:
				FoodDraw.fill(BgColor)							#Pinta a comida da cor do fundo;

			while SumonFood[0]:								#Enquanto for autorizada o realocamento da comida;
				for i in range(len(SnakeBody)-1):		#Passa por todas as partes do corpo da cobra:
					if FoodCoordinates == SnakeBody[i]:	#Se o novo local da comida já estiver ocupado pela cobra:
						FoodCoordinates = ((random.randint(0,760)//20 * 20), ((random.randint(20,640))//20 * 20))
						#^Sorteia um énuplo com (x, y) para a nova posição com valores inteiros múltiplos de 20;
						break										#Enterrompe o ciclo (laço for);
					else:											#Se o novo local da comida estiver livre:
						SumonFood[0] = 0						#Enterrompe o ciclo a realocar a comida;
			if SumonFood[1] >= 2 and SumonFood[1] <= 11:	#Se o valor anterior da comida for entre 2 e 11:
				AtualizateData = 1								#Autoriza o programa ler o Banco de Dados;
				UpdateData(0, "GameSaves", "Coins", 1)		#Contabiliza mais uma moeda no banco de dados;
				SoundPlaylist[5].play()							#Tocar áudio "Som de moeda do Super Mário";
			elif SumonFood[1] == 1:								#Se o valor anterior da comida for 1:
				if len(MusicUnlockedList) > 35:				#Se o jogador tiver todas as músicas:
					UpdateData(0, "GameSaves", "Coins", 10)	#Contabiliza mais dez moeda no banco de dados;
				else:													#Se o jogador não tiver todas as músicas:
					NewMusicUnlocked = random.randint(0, 35)	#Sorteia um novo índice para selecionar uma música;
					while (NewMusicUnlocked in MusicUnlockedList):	#Enquanto o jogador já possuír a música sorteada: 
						NewMusicUnlocked = random.randint(0, 35)	#Sorteia um novo índice para selecionar uma música;
					AtualizateData = 1							#Autoriza o programa ler o Banco de Dados;
					UpdateData(0, "Musics", "MusicUnlockedList", NewMusicUnlocked)	#Adiciona o novo índice no banco de dados;
					NewMusicUnlocked = -1						#Zera o valor da variável;
				SoundPlaylist[5].play()							#Tocar áudio "Som de moeda do Super Mário";
			else:														#Caso contrario (Comida vermelha comum):
				SnakeBody.append((-40,-40))					#A cobra ganha mais um bloco de tamanho;
				Score = Score + 1									#Somar 1 ponto ao placar;
		if not(InvulnerabilityFix):							#Se o código de invulnerabilidade estiver desativado;
			for i in range(1, len(SnakeBody)):				#Verifica todo o corpo da cobra (exceto sua cabeça):
				if (SnakeBody[i][0] == SnakeBody[0][0]) and (SnakeBody[i][1] == SnakeBody[0][1]):	#Se a cabeça da cobraestiver por cima de uma outra parte do corpo:
					if SnakeReborn:																	#Se o jogador tiver a permissão de renascer;
						SoundPlaylist[7].play()														#Tocar som "Coral Angelical";
						pygame.time.delay(2500)														#Aguarda 2.5 segundos;
						SnakeBody = [(380, 340), (380, 360), (380, 380), (380, 400), 
										 (380, 420), (380, 440), (380, 460), (380, 480), 
										 (380, 500), (380, 520), (380, 540), (380, 560),
										 (380, 580), (380, 600), (360, 600), (340, 600),
										 (340, 580), (340, 560), (340, 540), (340, 520),]	#O copo da cobra é definido com tamanho 20;
						pygame.time.delay(800)														#Aguarda 8/10 de segundo;
						SnakeReborn = not(SnakeReborn)											#Seu renascimento é negado;
						AtualizateData = 1															#Autoriza o programa ler o Banco de Dados;
						UpdateData(0, "Itens", UseItem[1], -1)									#Subtrai em um o item usado no banco de dados;
						break																				#Interrompe a verificação do o corpo;
					elif Invulnerability:															#Se o jogador tiver a permissão de usar o escudo:
						Invulnerability = not(Invulnerability)									#Seu escudo é negado;
						AtualizateData = 1															#Autoriza o programa ler o Banco de Dados;
						UpdateData(0, "Itens", UseItem[1], -1)									#Subtrai em um o item usado no banco de dados;
					elif not(SnakeReborn) or not(Invulnerability):							#Se o jogador não tiver nem a ressurreição ou escudo:
						Score = 0																		#Zera o placar;
						Retry = 1																		#Define que o jogador deve entrar no layer de derrota;
						if UseItem[1] != "Escudo" and UseItem[1] != "Ressurreicao":		#Se o item fixo usado não for (escudo e resurreição):
							UpdateData(0, "Itens", UseItem[1], -1)								#Subtrai em um o item usado no banco de dados;
						SoundPlaylist[0].play()														#Tocar som "Do you lose...";
						pygame.time.delay(600)														#Aguarda 6/10 de segundo;
		
		if Key[pygame.K_ESCAPE]:	#Se atecla "ESC" for pressionada:
			Score = 0					#Zera o placar;
			Retry = 1					#Define que o jogador deve entrar no layer de derrota;
			SoundPlaylist[0].play()	#Tocar som "Do you lose...";
			if UseItem[1] != None and (UseItem[1] != "Escudo" and UseItem[1] != "Ressurreicao"):	#Se o item fixo usado não for (escudo e resurreição):
				if DataI[UseItem[1]] > 0:																				#E o jogador pussuir pelo menos 1 do item:
					AtualizateData = 1																					#Autoriza o programa ler o Banco de Dados;
					UpdateData(0, "Itens", UseItem[1], -1)															#Subtrai em um o item usado no banco de dados;
			pygame.time.delay(600)																						#Aguarda 6/10 de segundo;

		if Zawarudo[0] != 0:														#Se o tempo não estiver parado (Zawarudo):
			for i in range(len(SnakeBody) - 1, 0, -1):					#Verifica todo o corpo da cobra (exceto sua cabeça):
				SnakeBody[i] = (SnakeBody[i-1][0], SnakeBody[i-1][1])	#Faz com que o bloco de trás receba as coordenadas do bloco da frente;

		if DirMovement == 1 and Zawarudo[0] != 0:							#Se a cobra estiver se movimentando para (cima):
			SnakeBody[0] = (SnakeBody[0][0], SnakeBody[0][1] - 20)	#A cabeça tem seu eixo y subtraído em 20px;
		if DirMovement == 2 and Zawarudo[0] != 0:							#Se a cobra estiver se movimentando para (baixo):
			SnakeBody[0] = (SnakeBody[0][0], SnakeBody[0][1] + 20)	#A cabeça tem seu eixo y somado em 20px;
		if DirMovement == 3 and Zawarudo[0] != 0:							#Se a cobra estiver se movimentando para (esquerda):
			SnakeBody[0] = (SnakeBody[0][0] - 20, SnakeBody[0][1])	#A cabeça tem seu eixo x subtraído em 20px;
		if DirMovement == 4 and Zawarudo[0] != 0:							#Se a cobra estiver se movimentando para (direita):
			SnakeBody[0] = (SnakeBody[0][0] + 20, SnakeBody[0][1])	#A cabeça tem seu eixo x somado em 20px;

		if SnakeBody[0][0] <= -10:						#Se a coordenada x da cabeça for inferior à -10px:
			SnakeBody[0] = (760, SnakeBody[0][1])	#O eixo x recebe o valor da borda direita;
		elif SnakeBody[0][0] >= 780:					#Se a coordenada x da cabeça for superior à 780px:
			SnakeBody[0] = (0, SnakeBody[0][1])		#O eixo y recebe o valor da borda esquerda;
		elif SnakeBody[0][1] <= 10:					#Se a coordenada y da cabeça for inferior à 10px:
			SnakeBody[0] = (SnakeBody[0][0], 640)	#O eixo y recebe o valor da borda direita;
		elif SnakeBody[0][1] >= 660:					#Se a coordenada y da cabeça for inferior à 660px:
			SnakeBody[0] = (SnakeBody[0][0], 20)	#O eixo y recebe o valor da borda esquerda;

		if SelectOptionsGrid == 1:													#Se a grade estiver no formato 1:
			if SumonFood[2] == 1:													#Se a comida for o disco:
				Window.blit(Galery[0][1], (FoodCoordinates))					#Imprime a imagem do disco na tela, nas coordenadas sorteadas;
			else:																			#Se a comida não for o disco:
				Window.blit(FoodDraw, FoodCoordinates)							#Imprime a comida na tela, nas coordenadas sorteadas;
			for x in range(0, 800, 20):											#Verifica todos os pixes na vertical a cada 20px, começando do 0:
				pygame.draw.line(Window, (80, 80, 80), (x, 0), (x, 800))	#Desenha uma linha cinza na horizontal;
			for y in range(0, 800, 20):											#Verifica todos os pixes na horizontal a cada 20px, começando do 0:
				pygame.draw.line(Window, (80, 80, 80), (0, y), (800, y))	#Desenha uma linha cinza na vertical;
		elif SelectOptionsGrid == 2:												#Se a grade estiver no formato 2:
			for x in range(-10, 800, 20):											#Verifica todos os pixes na vertical a cada 20px, começando do -10:
				pygame.draw.line(Window, (80, 80, 80), (x, 0), (x, 800))	#Desenha uma linha cinza na vertical;
			for y in range(-10, 800, 20):											#Verifica todos os pixes na horizontal a cada 20px, começando do 0:
				pygame.draw.line(Window, (80, 80, 80), (0, y), (800, y))	#Desenha uma linha cinza na horizontal;
			if SumonFood[2] == 1:													#Se a comida for o disco:
				Window.blit(Galery[0][1], (FoodCoordinates))					#Imprime a imagem do disco na tela, nas coordenadas sorteadas;
			else:																			#Se a comida não for o disco:
				Window.blit(FoodDraw, FoodCoordinates)							#Imprime a comida na tela, nas coordenadas sorteadas;
		elif SelectOptionsGrid == 0:												#Se a grade estiver no formato 0:
			if SumonFood[2] == 1:													#Se a comida for o disco:
				Window.blit(Galery[0][1], (FoodCoordinates))					#Imprime a imagem do disco na tela, nas coordenadas sorteadas;
			else:																			#Se a comida não for o disco:
				Window.blit(FoodDraw, FoodCoordinates)							#Imprime a comida na tela, nas coordenadas sorteadas;

		for co in SnakeBody:				#Verifica todos os pares ordenados referentes ao corpo da cobra:
			Window.blit(SnakeDraw,co)	#Desenha a parte do corpo da cobra;

		if SelectCustomSnakeHead != 0:																					#Se for indicada a pintura da cabeça:
			pygame.draw.rect(Window, ((SnakeHeadColor)), [SnakeBody[0][0], SnakeBody[0][1], 20, 20])	#Desenha um quadrado sobre a cabeça da cor indicada pelo jogador;
			
		FontSys = pygame.font.SysFont("Stencil", 15)											#Recebe a fonte "Stencil" tamanho 15;
		if SelectCustomBg == 8:																		#Se a cor do fundo for preto:
			pygame.draw.rect(Window, (SysColors[1][1]), [0,0,800,20])					#Desenha um cabeçalho branco de 20px de altura na parte superior da aba;
			if SelectOptionsScore:																	#Se for dada a permissão para mostrar a pontuação:
				Font = FontSys.render("Score: {}".format(Score), 5, ((0,0,0)))			#O texto recebe a string "Score: {placar}", cor preta;
				Window.blit(Font, (10,5))															#Escreve essa string na tela;
			if SelectOptionsTime:																	#Se for dada a permissão para mostrar o tempo:
				Font = FontSys.render("Time: {}".format(TimePlayed), 5, ((0,0,0)))	#O texto recebe a string "Time: {tempo}", cor preta;
				Window.blit(Font, (110,5))															#Escreve essa string na tela;
			if UseItem[0] != None or UseItem[1] != None:										#Se o jogador equipar pelo menos um item:
				if UseItem[0] != None and UseItem[1] != None:								#Se o jogador equipar ambos os itens:
					Font = FontSys.render("{}: {} | {}: {}".format(UseItem[0], DataI[UseItem[0]], UseItem[1], DataI[UseItem[1]]), 5, ((0,0,0)))
					#^O texto recebe uma string contendo o nome e a quantidade de ambos os itens, cor preta;
				elif UseItem[0] == None:															#Se o jogador equiparapenas o item contínuo:
					Font = FontSys.render("{}: {}".format(UseItem[1], DataI[UseItem[1]]), 5, ((0,0,0)))
					#^O texto recebe uma string contendo o nome e a quantidade do item, cor preta;
				elif UseItem[1] == None:															#Se o jogador equiparapenas o item rápido:
					Font = FontSys.render("{}: {}".format(UseItem[0], DataI[UseItem[0]]), 5, ((0,0,0)))
					#^O texto recebe uma string contendo o nome e a quantidade do item, cor preta;
				Window.blit(Font, (770 - pygame.Surface.get_width(Font),5))				#Escreve essa string na tela;

		else:																										#Se a cor do fundo não for preto:
			pygame.draw.rect(Window, (0,0,0), [0,0,800,20])											#Desenha um cabeçalho branco de 20px de altura na parte superior da aba;
			if SelectOptionsScore:																			#Se for dada a permissão para mostrar a pontuação:
				Font = FontSys.render("Score: {}".format(Score), 5, (SysColors[1][1]))		#O texto recebe a string "Score: {placar}", cor preta;
				Window.blit(Font, (10,5))																	#Escreve essa string na tela;
			if SelectOptionsTime:																			#Se for dada a permissão para mostrar o tempo:
				Font = FontSys.render("Time: {}".format(TimePlayed), 5, (SysColors[1][1]))	#O texto recebe a string "Time: {tempo}", cor preta;
				Window.blit(Font, (110,5))																	#Escreve essa string na tela;
			if UseItem[0] != None or UseItem[1] != None:												#Se o jogador equipar pelo menos um item:
				if UseItem[0] != None and UseItem[1] != None:										#Se o jogador equipar ambos os itens:
					Font = FontSys.render("{}: {} | {}: {}".format(UseItem[0], DataI[UseItem[0]], UseItem[1], DataI[UseItem[1]]), 5, (SysColors[1][1]))
					#^O texto recebe uma string contendo o nome e a quantidade de ambos os itens, cor branca;
				elif UseItem[0] == None:																#Se o jogador equipar apenas o item contínuo:
					Font = FontSys.render("{}: {}".format(UseItem[1], DataI[UseItem[1]]), 5, (SysColors[1][1]))
					#^O texto recebe uma string contendo o nome e a quantidade do item, cor branca;
				elif UseItem[1] == None:																#Se o jogador equipar apenas o item rápido:
					Font = FontSys.render("{}: {}".format(UseItem[0], DataI[UseItem[0]]), 5, (SysColors[1][1]))
					#^O texto recebe uma string contendo o nome e a quantidade do item, cor branca;
				Window.blit(Font, (770 - pygame.Surface.get_width(Font),5))					#Escreve essa string na tela;

		if Zawarudo[2]:								#Se for dada a permissão para o áudio do item "zawarudo":
			SoundPlaylist[4].play(0)				#Tocar som "ZA WARUDO!!";
			pygame.time.delay(5000)					#Aguarda 5 segundos
			Zawarudo[1] = 0							#Nega a permissão para a imagem do item "zawarudo":
			Zawarudo[2] = 0							#Nega a permissão para o áudio do item "zawarudo":
		if Zawarudo[1]:								#Se for dada a permissão para a imagem do item "zawarudo":
			Window.blit(Galery[0][0], (0,20))	#Imprime o efeito na tela;
			Zawarudo[2] = 1							#Concede a permissão para ser executado o som;
		
		if Zawarudo[0] != 0: 							#Se o tempo não estiver parado:
			SecondsPlayed = SecondsPlayed + 0.054	#Contabilize mais 0.054 segundos
		if SecondsPlayed >= 60:							#Se os segundos forem maiores que 60:
			MinutesPlayed = MinutesPlayed + 1		#Contabilize mais 1 minuto;
			SecondsPlayed = 0								#Zera os segundos;
		if MinutesPlayed >= 60:							#Se os minutos forem maiores que 60:
			HoursPlayed = HoursPlayed + 1				#Contabilize mais 1 hora;
			MinutesPlayed = 0								#Zera os minutos;

		TimePlayed = "{}:{}'{:.2f}".format(HoursPlayed, MinutesPlayed, SecondsPlayed)	#Formata a string que mostrará o tempo;
		pygame.time.delay(GameSpeed)																	#Aguarda um tempo, para deixar a cobra numa velocidade balanceada;
	#-------------
	
	#Tela de customização de cores:
	if SelectMenu == 1 and Menu == 0:	#Se o jogador ordenar a abertura deste layer e não estiver no menu:
		Window.fill((0,0,0))					#Pinta o fundo de Preto (Cor fixa do fundo);
		for event in pygame.event.get():	#Verifica todos os eventos que estão acontecendo:
			if event.type == pygame.QUIT:	#Se o jogador apertar para sair ("x" no canto superior da tela):
				pygame.quit()					#Fecha a execução do pygame;
				exit(0)							#Encerra o python;
			
			Key = pygame.key.get_pressed()							#Recebe uma lista com o índice das teclas pressionadas;
			if event.type == pygame.KEYDOWN:							#Se uma tecla for pressionada:
				if event.key == pygame.K_UP or Key[ord("w")] :	#Se a tecla "w" ou "seta pra cima" forem pressionadas:
					SelectCustom = SelectCustom - 1					#Seletor de opções de customização sobe um nível;
				if event.key == pygame.K_DOWN or Key[ord("s")] :#Se a tecla "s" ou "seta pra baixo" forem pressionadas:
					SelectCustom = SelectCustom + 1					#Seletor de opções de customização desce um nível;

				if event.key == pygame.K_RIGHT or Key[ord("d")]:				#Se a tecla "d" ou "seta pra direita" forem pressionadas:
					if SelectCustom == 0:												#Se o Seletor de opções de customização marcar o corpo:
						SelectCustomSnake = SelectCustomSnake + 1					#Passa em um o seletor de cor do sistema para o corpo;
						if SelectCustomSnake == SelectCustomSnakeHead:			#Se a cor do corpo da cobra foi igual a da cabeça:
							SelectCustomSnake = SelectCustomSnake + 1				#Passa em um o seletor de cor do sistema para o corpo;
						if SelectCustomSnake != 1 and SelectCustomSnake != 8:	#Se a cor do corpo da cobra não for preto e branco:
							if SelectCustomSnake == SelectCustomBg:				#Se a cor do corpo da cobra foi igual a do fundo
								SelectCustomSnake = SelectCustomSnake + 1			#Passa em um o seletor de cor do sistema para o corpo;
						if SelectCustomSnake > 8:										#Se o seletor de cor do sistema para o corpo passar do último:
							SelectCustomSnake = 1										#Volta para a primeira (no caso a segundo cor do sistema);
					
					if SelectCustom == 1:												#Se o Seletor de opções de customização marcar a cabeça:
						SelectCustomSnakeHead = SelectCustomSnakeHead + 1		#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead == SelectCustomSnake:			#Se a cor do corpo da cobra foi igual a da cabeça:
							SelectCustomSnakeHead = SelectCustomSnakeHead + 1	#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead == SelectCustomBg:				#Se a cor da cabeça da cobra foi igual a do fundo:
							SelectCustomSnakeHead = SelectCustomSnakeHead + 1	#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead > 8:									#Se o seletor de cor do sistema para a cabeça passar do último:
							SelectCustomSnakeHead = 0									#Volta para a primeira (nesse caso, realmente a primeira, que é "sem cor");
					
					if SelectCustom == 2:												#Se o Seletor de opções de customização marcar o fundo:
						SelectCustomBg = SelectCustomBg + 1							#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead == SelectCustomBg:				#Se a cor do fundo foi igual a da cabeça da cobra:
							SelectCustomBg = SelectCustomBg + 1						#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnake != 1 and SelectCustomSnake != 8:	#Se a cor do corpo da cobra não for preto e branco:
							if SelectCustomSnake == SelectCustomBg:				#Se a cor do corpo da cobra foi igual a do fundo
								SelectCustomBg = SelectCustomBg + 1					#Passa em um o seletor de cor do sistema para o fundo;
						if SelectCustomBg > 8 and SelectCustomBg != SelectCustomSnakeHead:	#Se o seletor de cor do sistema para o corpo passar do último e a cor do fundo for diferente da cabeça:
							SelectCustomBg = 1											#Volta para a primeira (no caso a segundo cor do sistema);

				if event.key == pygame.K_LEFT or Key[ord("a")]:					#Se a tecla "a" ou "seta pra esquerda" forem pressionadas:
					if SelectCustom == 0:												#Se o Seletor de opções de customização marcar o corpo:
						SelectCustomSnake = SelectCustomSnake - 1					#Volta em um o seletor de cor do sistema para o corpo;
						if SelectCustomSnake == SelectCustomSnakeHead:			#Se a cor do corpo da cobra foi igual a da cabeça:
							SelectCustomSnake = SelectCustomSnake - 1				#Volta em um o seletor de cor do sistema para o corpo;
						if SelectCustomSnake != 1 and SelectCustomSnake != 8:	#Se a cor do corpo da cobra não for preto e branco:
							if SelectCustomSnake == SelectCustomBg:				#Se a cor do corpo da cobra foi igual a do fundo:
								SelectCustomSnake = SelectCustomSnake - 1			#Volta em um o seletor de cor do sistema para o corpo;
						if SelectCustomSnake < 1:										#Se o seletor de cor do sistema para o corpo passar do primeiro (técnicamente segunda cor):
							SelectCustomSnake = 8										#Volta para a última;

					if SelectCustom == 1:												#Se o Seletor de opções de customização marcar a cabeça:
						SelectCustomSnakeHead = SelectCustomSnakeHead - 1		#Volta em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead == SelectCustomSnake:			#Se a cor do corpo da cobra foi igual a da cabeça:
							SelectCustomSnakeHead = SelectCustomSnakeHead - 1	#Volta em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead == SelectCustomBg:				#Se a cor da cabeça da cobra foi igual a do fundo:
							SelectCustomSnakeHead = SelectCustomSnakeHead - 1	#Volta em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead < 0:									#Se o seletor de cor do sistema para a cabeça passar do primeiro (nesse caso, realmente a primeira, que é "sem cor"):
							SelectCustomSnakeHead = 8									#Volta para a última;

					if SelectCustom == 2:												#Se o Seletor de opções de customização marcar o fundo:
						SelectCustomBg = SelectCustomBg - 1							#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnakeHead == SelectCustomBg:				#Se a cor do fundo foi igual a da cabeça da cobra:
							SelectCustomBg = SelectCustomBg - 1						#Passa em um o seletor de cor do sistema para a cabeça;
						if SelectCustomSnake != 1 and SelectCustomSnake != 8:	#Se a cor do corpo da cobra não for preto e branco:
							if SelectCustomSnake == SelectCustomBg:				#Se a cor do corpo da cobra foi igual a do fundo
								SelectCustomBg = SelectCustomBg - 1					#Passa em um o seletor de cor do sistema para o fundo;
						if SelectCustomBg < 1 and SelectCustomBg != SelectCustomSnakeHead:	#Se o seletor de cor do sistema para o corpo passar do primeiro (técnicamente segunda cor):
							SelectCustomBg = 8											#Volta para a última;
				
				if Key[pygame.K_SPACE]:		#Se a tecla "espaço" for pressionada:
					SoundPlaylist[3].play()	#Tocar áudio "Player 1, get ready...";
					Menu = 1						#Dá a premissão para a abertura do menu inicial;
		
		if SelectCustom < 0:	#Se o seletor de customização ficar menor que seu alcance:
			SelectCustom = 2	#Ele dá o giro e recebe o valor máximo;
		if SelectCustom > 2:	#Se o seletor de customização ficar maior que seu alcance:
			SelectCustom = 0	#Ele dá o giro e recebe o valor mínimo;

		Window.fill((0,0,0))													#Pinta o fundo de Preto (Cor fixa do fundo);
		FontSys = pygame.font.SysFont("Stencil", 80)					#Recebe a fonte "Stencil" tamanho 80;
		Font = FontSys.render("Customizar", 1, (SysColors[1][1]))#O texto recebe a string "Customizar", cor branca;
		Window.blit(Font,(150,150))										#Escreve essa string na tela;

		FontSys = pygame.font.SysFont("Stencil", 30)																		#Recebe a fonte "Stencil" tamanho 30;
		if SelectCustom == 0:																									#Se o Seletor de opções de customização marcar o corpo:
			if SelectCustomSnake == 1:																							#Se a cor do corpo da cobra for branca:
				Font = FontSys.render("Snake: {}".format(SysColors[SelectCustomSnake][0]),1,(150,150,150))#O texto recebe a string "Snake: {Branco}", cinza claro;
			elif SelectCustomSnake == 8:																						#Se a cor do corpo da cobra for preta:
				Font = FontSys.render("Snake: {}".format(SysColors[SelectCustomSnake][0]),1,(20,20,20))	#O texto recebe a string "Snake: {Preto}", cinza escuro;
			else:																														#Se a cor do corpo da cobra não for preto e branco:
				Font = FontSys.render("Snake: {}".format(SysColors[SelectCustomSnake][0]),1,SysColors[SelectCustomSnake][1])
				#^Pinta o texto com a mesma cor usada na cobra;
		else:																																#Se o Seletor de opções de customização não marcar o corpo:
			Font = FontSys.render("Snake: {}".format(SysColors[SelectCustomSnake][0]),1,(SysColors[1][1]))	#Pinta o texto de branco;
		SnakeColor = SysColors[SelectCustomSnake][1]																			#A cor da cobra recebe a cor selecionada;
		if SelectCustomSnake == 1:																									#Se a cor do corpo da cobra for branca:
			SnakeColor = ((150,150,150))																							#A cobra fica cinza claro;
		if SelectCustomSnake == 8:																									#Se a cor do corpo da cobra for preta:
			SnakeColor = ((50,50,50))																								#A cobra fica cinza escuro;
		Window.blit(Font,(20,350))																									#Escreve essa string na tela;
		
		if SelectCustom == 1:																											#Se o Seletor de opções de customização marcar a cabeça:
			if SelectCustomSnakeHead == 1:																							#Se a cor da cabeça da cobra for branca:
				Font = FontSys.render("Cabeça: {}".format(SysColors[SelectCustomSnakeHead][0]),1,(150,150,150))	#O texto recebe a string "Snake: {Branco}", cinza claro;
			elif SelectCustomSnakeHead == 8:																							#Se a cor da cabeça da cobra for preta:
				Font = FontSys.render("Cabeça: {}".format(SysColors[SelectCustomSnakeHead][0]),1,(20,20,20))		#O texto recebe a string "Snake: {Preto}", cinza escuro;
			else:																																#Se a cor da cabeça da cobra não for preto e branco:
				Font = FontSys.render("Cabeça: {}".format(SysColors[SelectCustomSnakeHead][0]),1,SysColors[SelectCustomSnakeHead][1])
				#^Pinta o texto com a mesma cor usada na cobra;
		else:																																		#Se o Seletor de opções de customização não marcar a cabeça:
			Font = FontSys.render("Cabeça: {}".format(SysColors[SelectCustomSnakeHead][0]),1,(SysColors[1][1]))	#Pinta o texto de branco;
		SnakeHeadColor = (SysColors[SelectCustomSnakeHead][1])																	#A cor da cabeça recebe a cor selecionada;
		if  SelectCustomSnakeHead == 0:																									#Se o jogador não quer pintar a cabeça:
			SnakeHeadColor = ((0,0,0))																										#Anula a cor da cabeça ((0,0,0)) só para marcar;
		if SelectCustomSnakeHead == 1:																									#Se a cor da cabeça da cobra for branca:
			SnakeHeadColor = ((150,150,150))																								#A cabeça fica cinza claro;
		if SelectCustomSnakeHead == 8:																									#Se a cor da cabeça da cobra for preta:
			SnakeHeadColor = ((50,50,50))																									#A cobra fica cinza escuro;
		Window.blit(Font,(20,400))																											#Escreve essa string na tela;

		if SelectCustom == 2:																								#Se o Seletor de opções de customização marcar o fundo:
			if SelectCustomBg == 1:																							#Se a cor do fundo for branca:
				Font = FontSys.render("Fundo: {}".format(SysColors[SelectCustomBg][0]),1,(150,150,150))#O texto recebe a string "Fundo: {Branco}", cinza claro;
			elif SelectCustomBg == 8:																						#Se a cor ddo fundo for preta:
				Font = FontSys.render("Fundo: {}".format(SysColors[SelectCustomBg][0]),1,(20,20,20))	#O texto recebe a string "Fundo: {Preto}", cinza escuro;
			else:																													#Se a cor do fundo não for preto e branco:
				Font = FontSys.render("Fundo: {}".format(SysColors[SelectCustomBg][0]),1,(SysColors[SelectCustomBg][1]))
				#^Pinta o texto com a mesma cor usada na cobra;
		else:																															#Se o Seletor de opções de customização não marcar a cabeça:
			Font = FontSys.render("Fundo: {}".format(SysColors[SelectCustomBg][0]),1,(SysColors[1][1]))	#Pinta o texto de branco;
		BgColor = SysColors[SelectCustomBg][1]																				#A cor do fundo recebe a cor selecionada;
		Window.blit(Font,(20,450))																								#Escreve essa string na tela;
	#------------------------------

	#Menu da loja:
	if SelectMenu == 2 and Menu == 0:	#Se o jogador ordenar a abertura deste layer e não está no menu:
		for event in pygame.event.get():	#Verifica todos os eventos que estão acontecendo:
			if event.type == pygame.QUIT:	#Se o jogador apertar para sair ("x" no canto superior da tela):
				pygame.quit()					#Fecha a execução do pygame;
				exit(0)							#Encerra o python;
			
			Key = pygame.key.get_pressed()							#Recebe uma lista com o índice das teclas pressionadas;
			if event.type == pygame.KEYDOWN:							#Se uma tecla for pressionada:
				if Key[pygame.K_SPACE]:									#Se a tecla "espaço" for pressionada:
					SoundPlaylist[3].play()								#Tocar som "Player 1, get ready..."
					Menu = 1													#Permite o acesso ao menu;
				
				if event.key == pygame.K_LEFT or Key[ord("a")]:	#Se a tecla "a" ou "seta pra esquerda":
					StoreIndexSection = StoreIndexSection - 1		#Volta em um o seletor da seção;
					StoreIndexItem = 0									#Vota para o item inicial daquela seção;
					if StoreIndexSection < 0:							#Se o seletor de seções ficar menor que seu alcance:
						StoreIndexSection = 2							#Ele dá o giro e recebe o valor máximo;
				if event.key == pygame.K_RIGHT or Key[ord("d")]:#Se a tecla "d" ou "seta pra direita":
					StoreIndexSection = StoreIndexSection + 1		#Avança em um o seletor da seção;
					StoreIndexItem = 0									#Vota para o item inicial daquela seção;
					if StoreIndexSection > 2:							#Se o seletor de seções ficar menor que seu alcance:
						StoreIndexSection = 0							#Ele dá o giro e recebe o valor mínimo;

				if event.key == pygame.K_UP or Key[ord("w")]:	#Se a tecla "w" ou "seta pra cima":
					StoreIndexItem = StoreIndexItem - 1				#Volta em um o seletor de item;
					if StoreIndexSection == 2:							#Se o seletor de seções for 2 (músicas):
						if StoreIndexItem < 0:							#Se o seletor de itens (música) ficar menor que seu alcance:
							StoreIndexItem = 35							#Ele dá o giro e recebe o valor máximo;
					elif StoreIndexSection == 1:						#Se o seletor de seções for 1 (itens de efeito contínuo):
						if StoreIndexItem < 0:							#Se o seletor de itens (itens de efeito contínuo) ficar menor que seu alcance:
							StoreIndexItem = 3							#Ele dá o giro e recebe o valor máximo;
					else:														#Se o seletor de seções for 0 (itens de efeito rápido):
						if StoreIndexItem < 0:							#Se o seletor de itens (itens de efeito rápido) ficar menor que seu alcance:
							StoreIndexItem = 1							#Ele dá o giro e recebe o valor máximo;
				
				if event.key == pygame.K_DOWN or Key[ord("s")]:	#Se a tecla "s" ou "seta pra baixo":
					StoreIndexItem = StoreIndexItem + 1				#Volta em um o seletor de item;
					if StoreIndexSection == 2:							#Se o seletor de seções for 2 (músicas):
						if StoreIndexItem > 35:							#Se o seletor de itens (música) ficar maior que seu alcance:
							StoreIndexItem = 0							#Ele dá o giro e recebe o valor mínimo;
					elif StoreIndexSection == 1:						#Se o seletor de seções for 1 (itens de efeito contínuo):
						if StoreIndexItem > 3:							#Se o seletor de itens (itens de efeito contínuo) ficar maior que seu alcance:
							StoreIndexItem = 0							#Ele dá o giro e recebe o valor mínimo;
					else:														#Se o seletor de seções for 0 (itens de efeito rápido):
						if StoreIndexItem > 1:							#Se o seletor de itens (itens de efeito rápido) ficar maior que seu alcance:
							StoreIndexItem = 0							#Ele dá o giro e recebe o valor mínimo;

		Window.fill((0,0,0))												#Pinta o fundo de Preto (Cor fixa do fundo);
		FontSys = pygame.font.SysFont("Stencil", 80)				#Recebe a fonte "Stencil" tamanho 80;
		Font = FontSys.render(("Loja"), 1, (SysColors[1][1]))	#O texto recebe a string "Loja", branco;
		Window.blit(Font,(295,80))										#Escreve essa string na tela;
		FontSys = pygame.font.SysFont("Stencil", 25)				#Recebe a fonte "Stencil" tamanho 25;
		
		if StoreIndexSection == 2:																																			#Se o seletor de seções for 2 (músicas):
			Window.blit(SelectStoreColumn[StoreIndexSection][StoreIndexItem][0], (265,260))																#Imprime a imagem do disco na tela;
			Font = FontSys.render("{}".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]), 1, (SysColors[1][1]))					#O texto recebe a string "{Nome da música}", branco;
			Window.blit(Font,(10,570))																																		#Escreve essa string na tela;
			Font = FontSys.render("{}".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][2]), 1, (SysColors[1][1]))					#O texto recebe a string "{Nome do álbum}", branco;
			Window.blit(Font,(10,605))																																		#Escreve essa string na tela;
			if NewPlaylistIndex == StoreIndexItem:																														#Se o jogador estiver na mesmo múscia que estiver sendo reproduzida:
				Font = FontSys.render("Tocando...".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][2]), 1, (SysColors[1][1]))	#O texto recebe a string "Tocando...", branco;
				Window.blit(Font,(335,230))																																#Escreve essa string na tela;
			if not(StoreIndexItem in MusicUnlockedList):																												#Se o jogador não possuir a múscia que estiver selecionando:
				Font = FontSys.render("${}[g]".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[3][1]))		#O texto recebe a string "${Preço de compra}[g]", verde;
				Window.blit(Font,(355,525))																																#Escreve essa string na tela;
				if Key[ord("g")] and Coins >= SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]:													#Se a tecla "g" for pressionada e o jogador possuir mais ou o mesmo valor em moedas do preço da música:
					AtualizateData = 1																																		#Autoriza o programa ler o Banco de Dados;
					UpdateData(0, "GameSaves", "Coins", -(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]))									#Retira moedas no valor equivalente ao preço da música no banco de dados;
					UpdateData(0, "Musics", "MusicUnlockedList", StoreIndexItem)																				#Adiciona a nova música adquirida à sua lista de músicas;
					SoundPlaylist[6].play()																																	#Tocar som "Som genérico de caixa registradora";
		
		else:																																						#Se o seletor de seções não for 2 (músicas):
			Window.blit(SelectStoreColumn[StoreIndexSection][StoreIndexItem][0], (387 - pygame.Surface.get_width(SelectStoreColumn[StoreIndexSection][StoreIndexItem][0])/2,260))
			#^Imprime a imagem do item no centro tela;
			Font = FontSys.render("{}".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]), 1, (SysColors[1][1]))			#O texto recebe a string "{Nome do item}", branco;
			Window.blit(Font,(10,570))																																#Escreve essa string na tela;
			Font = FontSys.render("${}[g]".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][2]), 1, (SysColors[3][1]))	#O texto recebe a string "${Preço de compra}[g]", verde;
			Window.blit(Font,((310,525)))																															#Escreve essa string na tela;
			Font = FontSys.render("${}[j]".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, ((SysColors[2][1])))	#O texto recebe a string "${Preço de venda}[j]", verde;
			Window.blit(Font,((400,525)))																															#Escreve essa string na tela;
			FontSys = pygame.font.SysFont("Stencil", 15)																										#Recebe a fonte "Stencil" tamanho 15;
			if StoreIndexSection == 0 and StoreIndexItem == 0:																								#Se o jogador estiver selecionando o primeiro item rápido:
				Font = FontSys.render("Permite o jogador à parar o tempo.".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[1][1]))
				#^O texto recebe a string "{descrição do produto}", branco;
				Window.blit(Font,(10,605))																													#
			if StoreIndexSection == 0 and StoreIndexItem == 1:																						#Se o jogador estiver selecionando o segundo item rápido:
				Font = FontSys.render("Reposiciona a comida num lugar aleatório".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[1][1]))
				#^O texto recebe a string "{descrição do produto}", branco;
				Window.blit(Font,(10,605))																													#Escreve essa string na tela;

			if StoreIndexSection == 1 and StoreIndexItem == 0:																						#Se o jogador estiver selecionando o primeiro item contínuo:
				Font = FontSys.render("Aumenta a chance do surgimento de discos e moedas em 200%.".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[1][1]))
				#^O texto recebe a string "{descrição do produto}", branco;
				Window.blit(Font,(10,605))																													#Escreve essa string na tela;
			if StoreIndexSection == 1 and StoreIndexItem == 1:																						#Se o jogador estiver selecionando o segundo item contínuo:
				Font = FontSys.render("A Snake inicia 4x maior.".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[1][1]))
				#^O texto recebe a string "{descrição do produto}", branco;
				Window.blit(Font,(10,605))																													#Escreve essa string na tela;
			if StoreIndexSection == 1 and StoreIndexItem == 2:																						#Se o jogador estiver selecionando o terceiro item contínuo:
				Font = FontSys.render("Protege a snake da primeira colisão por um quadrado.".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[1][1]))
				#^O texto recebe a string "{descrição do produto}", branco;
				Window.blit(Font,(10,605))																													#Escreve essa string na tela;
			if StoreIndexSection == 1 and StoreIndexItem == 3:																						#Se o jogador estiver selecionando o quarto item contínuo:
				Font = FontSys.render("Ressucita a snake com tamanho 20, mantém o tempo e a pontuação.".format(SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]), 1, (SysColors[1][1]))
				#^O texto recebe a string "{descrição do produto}", branco;
				Window.blit(Font,(10,605))																													#Escreve essa string na tela;
			
			Font = FontSys.render("Possui: {}".format(DataI[SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]]), 1, (SysColors[1][1]))
			#^O texto recebe a string "Possui: {quantidade do produto}", branco;
			Window.blit(Font,(10,520))																															#Escreve essa string na tela;
			if Key[ord("g")] and Coins >= SelectStoreColumn[StoreIndexSection][StoreIndexItem][2] and KeyboardPauseStore == 0:	#Se a tecla "g" for pressionada, o jogador possuir mais ou o mesmo valor em moedas do preço do item e o teclado da loja está liberado:
				AtualizateData = 1																																#Autoriza o programa ler o Banco de Dados;
				UpdateData(0, "GameSaves", "Coins", -(SelectStoreColumn[StoreIndexSection][StoreIndexItem][2]))							#Retira moedas no valor equivalente ao preço do item no banco de dados;
				UpdateData(0, "Itens", SelectStoreColumn[StoreIndexSection][StoreIndexItem][1], 1)											#Adiciona em um o item comprado no banco de dados;
				SoundPlaylist[6].play()																															#Tocar som "Som genérico de caixa registradora";
				KeyboardPauseStore = 1																															#Bloqueia o teclado da loja;
			if Key[ord("j")] and DataI[SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]] > 0 and KeyboardPauseStore == 0:	#Se a tecla "g" for pressionada, o jogador possuir um ou mais do item selecionado e o teclado da loja está liberado:
				AtualizateData = 1																																#Autoriza o programa ler o Banco de Dados;
				UpdateData(0, "GameSaves", "Coins", (SelectStoreColumn[StoreIndexSection][StoreIndexItem][3]))							#Adiciona moedas no valor equivalente ao preço de venda do item no banco de dados;
				UpdateData(0, "Itens", SelectStoreColumn[StoreIndexSection][StoreIndexItem][1], -1)											#Retira em um o item comprado no banco de dados;
				SoundPlaylist[6].play()																															#Tocar som "Som genérico de caixa registradora";
				KeyboardPauseStore = 1																															#Bloqueia o teclado da loja;
			
			if (DataI[SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]] > 0) and not(UseItem[0] == SelectStoreColumn[StoreIndexSection][StoreIndexItem][1] or UseItem[1] == SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]):
				#^Se o jogador possuír pelo menos um do item selecionado, e não estiver já equipado:
				FontSys = pygame.font.SysFont("Stencil", 20)																#Recebe a fonte "Stencil" tamanho 20;
				Font = FontSys.render("Equipar[h]", 1, (SysColors[1][1]))											#O texto recebe a string "Equipar[h]", branco;
				Window.blit(Font,(335,230))																					#Escreve essa string na tela;
				if Key[ord("h")]:																									#Se a tecla "h" for pressionada:
					UseItem[StoreIndexSection] = SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]	#Equipa o item selecionado;

			if UseItem[0] == SelectStoreColumn[StoreIndexSection][StoreIndexItem][1] or UseItem[1] == SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]:
				#^Se o jogador estiver equipando um dos itens selecionados:
				FontSys = pygame.font.SysFont("Stencil", 20)																#Recebe a fonte "Stencil" tamanho 20;
				Font = FontSys.render("Desequipar[n]", 1, (SysColors[1][1]))										#O texto recebe a string "Desequipar[n]", branco;
				Window.blit(Font,(312,230))																					#Escreve essa string na tela;
				if Key[ord("n")]:																									#Se a tecla "n" for pressionada:
					UseItem[StoreIndexSection] = None																		#Desequipa o item selecionado;
			if Key[ord("g")] == 0 and Key[ord("h")] == 0 and Key[ord("j")] == 0 and Key[ord("n")] == 0:	#Se nenuma das teclas "g", "h", "j" e "n" forem pressionadas:
				KeyboardPauseStore = 0																							#Desbloqueia o teclado da loja;
			if DataI[SelectStoreColumn[StoreIndexSection][StoreIndexItem][1]] <= 0:								#Se o jogador não possuir mais aquele item:
				UseItem[StoreIndexSection] = None																			#Desequipa automaticamente;
		FontSys = pygame.font.SysFont("Stencil", 15)																		#Recebe a fonte "Stencil" tamanho 15;
		Font = FontSys.render(("Moedas: {}".format(Coins)), 1, (SysColors[1][1]))								#O texto recebe a string "Moedas: {quantiade de moedas}", branco;
		Window.blit(Font,(10,543))																								#Escreve essa string na tela;
		FontSys = pygame.font.SysFont("Stencil", 15)																		#Recebe a fonte "Stencil" tamanho 15;
		Font = FontSys.render("Item rápido: {}.".format(UseItem[0]), 1, (SysColors[1][1]))					#O texto recebe a string "Item rápido: {nome do item rápido equipado}", branco;
		Window.blit(Font,(388 - pygame.Surface.get_width(Font)/2,170))												#Escreve essa string no centro da tela;
		Font = FontSys.render("Item fixo: {}.".format(UseItem[1]), 1, (SysColors[1][1]))						#O texto recebe a string "Item fixo: {nome do item contínuo equipado}", branco;
		Window.blit(Font,(388 - pygame.Surface.get_width(Font)/2,190))												#Escreve essa string no centro da tela;
		pygame.display.update()																									#Atualiza a tela;
	#-------------

	#Menu de configurações / tela de pause:
	if (SelectMenu == 3 and Menu == 0) or (PauseGame):	#
		for event in pygame.event.get():						#Verifica todos os eventos que estão acontecendo:
			if event.type == pygame.QUIT:						#Se o jogador apertar para sair ("x" no canto superior da tela):
				pygame.quit()										#Fecha a execução do pygame;
				exit(0)												#Encerra o python;
			
			Key = pygame.key.get_pressed()							#Recebe uma lista com o índice das teclas pressionadas;
			if event.type == pygame.KEYDOWN:							#Se uma tecla for pressionada:
				if event.key == pygame.K_UP or Key[ord("w")]:	#Se a tecla pressionada for "w" ou "seta pra cima":
					SelectOptions = SelectOptions - 1				#Volta em um o seletor de opções;
				if event.key == pygame.K_DOWN or Key[ord("s")]:	#Se a tecla pressionada for "s" ou "seta pra baixo":
					SelectOptions = SelectOptions + 1				#Avança em um o seletor de opções;
				
				if event.key == pygame.K_RIGHT or Key[ord("d")]:	#Se a tecla pressionada for "d" ou "seta pra direita":
					if SelectOptions == 0:									#Se o seletor marcar a formatação de grade:
						SelectOptionsGrid = SelectOptionsGrid + 1		#Avança em um o estilo de formatação da grade;
						if SelectOptionsGrid > 2:							#Se o seletor de opções ficar maior que seu alcance:
							SelectOptionsGrid = 0							#Ele dá o giro e recebe o valor mínimo;
					if SelectOptions == 1:									#Se o seletor marcar a visualiazção de tempo de partida:
						SelectOptionsTime = not(SelectOptionsTime)	#Permite / Desautoriza sua visualização durante a partida;
					if SelectOptions == 2:									#Se o seletor marcar a visualiazção da ponuação de partida:
						SelectOptionsScore = not(SelectOptionsScore)	#Permite / Desautoriza sua visualização durante a partida;
					if SelectOptions == 3:									#Se o seletor marcar o volume dos sons:
						SelectOptionsSound = SelectOptionsSound + 5	#Aumenta em 5% o volume do som;
						if SelectOptionsSound > 100:						#Se o volume do som ficar maior que seu alcance:
							SelectOptionsSound = 0							#Ele dá o giro e recebe o valor mínimo;
					if SelectOptions == 4:									#Se o seletor marcar o volume das músicas:
						SelectOptionsMusic = SelectOptionsMusic + 5	#Aumenta em 5% o volume da música;
						if SelectOptionsMusic > 100:						#Se o volume da música ficar maior que seu alcance:
							SelectOptionsMusic = 0							#Ele dá o giro e recebe o valor mínimo;
				
				if event.key == pygame.K_LEFT or Key[ord("a")]:		#Se a tecla pressionada for "d" ou "seta pra esquerda":
					if SelectOptions == 0:									#Se o seletor marcar a formatação de grade:
						SelectOptionsGrid = SelectOptionsGrid - 1		#Regride em um o estilo de formatação da grade;
						if SelectOptionsGrid < 0:							#Se o seletor de grades ficar menor que seu alcance:
							SelectOptionsGrid = 2							#Ele dá o giro e recebe o valor máximo;
					if SelectOptions == 1:									#Se o seletor marcar a visualiazção de tempo de partida:
						SelectOptionsTime = not(SelectOptionsTime)	#Permite / Desautoriza sua visualização durante a partida;
					if SelectOptions == 2:									#Se o seletor marcar a visualiazção da ponuação de partida:
						SelectOptionsScore = not(SelectOptionsScore)	#Permite / Desautoriza sua visualização durante a partida;
					if SelectOptions == 3:									#Se o seletor marcar o volume dos sons:
						SelectOptionsSound = SelectOptionsSound - 5	#Diminui em 5% o volume do som;
						if SelectOptionsSound < 0:							#Se o seletor de sons ficar menor que seu alcance:
							SelectOptionsSound = 100						#Ele dá o giro e recebe o valor máximo;
					if SelectOptions == 4:									#Se o seletor marcar o volume das músicas:
						SelectOptionsMusic = SelectOptionsMusic - 5	#Diminui em 5% o volume da música;
						if SelectOptionsMusic < 0:							#Se o seletor de músicas ficar menor que seu alcance:
							SelectOptionsMusic = 100						#Ele dá o giro e recebe o valor máximo;

				if Key[pygame.K_SPACE]:			#Se a tecla pressionada for "espaço":
					if PauseGame == 0:			#Se o jogo não estiver pausado:
						Menu = 1						#Volta ao menu inicial;
						SoundPlaylist[3].play()	#Tocar som "Player 1, get ready...";
					elif PauseGame:				#Se o jogo não estiver pausado:
						PauseGame = 0				#Despausa o jogo;
		
		if SelectOptions < 0:	#Se o seletor de opções ficar menor que seu alcance:
			SelectOptions = 4		#Ele dá o giro e recebe o valor máximo;
		if SelectOptions > 4:	#Se o seletor de opções ficar maior que seu alcance:
			SelectOptions = 0		#Ele dá o giro e recebe o valor mínimo;

		Window.fill((0,0,0))												#Pinta o fundo de Preto (Cor fixa do fundo);
		FontSys = pygame.font.SysFont("Stencil", 80)				#Recebe a fonte "Stencil" tamanho 80;
		Font = FontSys.render("Opções", 1, (SysColors[1][1]))	#O texto recebe a string "Opções", branco;
		Window.blit(Font,(250,150))									#Escreve essa string na tela;

		FontSys = pygame.font.SysFont("Stencil", 30)															#Recebe a fonte "Stencil" tamanho 80;
		if SelectOptions == 0:																						#Se o seletor marcar a formatação de grade:
			Font = FontSys.render("Grade: {}".format(SelectOptionsGrid), 1, ((SysColors[2][1])))#O texto recebe a string "Grade: {formato}", vermelha;
		else:																												#Se o seletor não marcar a formatação de grade:
			Font = FontSys.render("Grade: {}".format(SelectOptionsGrid), 1, (SysColors[1][1]))	#O texto recebe a string "Grade: {formato}", branca;
		Window.blit(Font,(20,350))																					#Escreve essa string na tela;
		
		if SelectOptions == 1:																						#Se o seletor marcar o tempo:
			Font = FontSys.render("Tempo: {}".format(SelectOptionsTime), 1, ((SysColors[2][1])))#O texto recebe a string "Tempo: {permissão}", vermelha;
		else:																												#Se o seletor não marcar o tempo:
			Font = FontSys.render("Tempo: {}".format(SelectOptionsTime), 1, (SysColors[1][1]))	#O texto recebe a string "Tempo: {permissão}", branca;
		Window.blit(Font,(20,400))																					#Escreve essa string na tela;
		
		if SelectOptions == 2:																								#Se o seletor marcar a pontuação:
			Font = FontSys.render("Pontuação: {}".format(SelectOptionsScore), 1, ((SysColors[2][1])))	#O texto recebe a string "Pontuação: {permissão}", vermelha;
		else:																														#Se o seletor não marcar a pontuação:
			Font = FontSys.render("Pontuação: {}".format(SelectOptionsScore), 1, (SysColors[1][1]))	#O texto recebe a string "Pontuação: {permissão}", branca;
		Window.blit(Font,(20,450))																							#Escreve essa string na tela;

		if SelectOptions == 3:																							#Se o seletor marcar o volume do som:
			Font = FontSys.render("Sons: {}%".format(SelectOptionsSound), 1, ((SysColors[2][1])))	#O texto recebe a string "Sons {volume}%", vermelha;
		else:																													#Se o seletor não marcar o volume do som:
			Font = FontSys.render("Sons: {}%".format(SelectOptionsSound), 1, (SysColors[1][1]))		#O texto recebe a string "Sons {volume}%", branca;
		Window.blit(Font,(20,500))																						#Escreve essa string na tela;
		
		#Nivela todos os sons de acordo com o volume escolhido:
		SoundPlaylist[0].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[1].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[2].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[3].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[4].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[5].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[6].set_volume(SelectOptionsSound / 100)
		SoundPlaylist[7].set_volume(SelectOptionsSound / 100)
		#------------------------------------------------------

		if SelectOptions == 4:																								#Se o seletor marcar o volume da música:
			Font = FontSys.render("Música: {}%".format(SelectOptionsMusic), 1, ((SysColors[2][1])))	#O texto recebe a string "Música {volume}%", vermelha;
		else:																														#Se o seletor não marcar o volume da música:
			Font = FontSys.render("Música: {}%".format(SelectOptionsMusic), 1, (SysColors[1][1]))		#O texto recebe a string "Música {volume}%", branca;
		if SelectOptionsMusic > 0:																							#Se o volume da música for maior que 0:
			pygame.mixer.music.set_volume(SelectOptionsMusic / 100)												#Nivela a música de acordo com o volume escolhido
			if Zawarudo[0] != 0:																								#Se o jogo não estiver numa parada temporal:
				pygame.mixer.music.unpause()																				#Despausa a música;
		else:																														#Se o volume da música for 0:
			pygame.mixer.music.pause()																						#Pausa a música;
		Window.blit(Font,(20,550))																							#Escreve essa string na tela;
		FontSys = pygame.font.SysFont("Stencil", 20)																	#Recebe a fonte "Stencil" tamanho 20;
		Font = FontSys.render("{}".format(MusicPlaylist[NewPlaylistIndex][1]), 1, (SysColors[1][1]))	#O texto recebe a string "{nome da música que está tocando}", branca;
		Window.blit(Font,(20,600))																							#Escreve essa string na tela;
		pygame.display.update()																								#Atualiza a tela;
		pygame.time.delay(50)																								#Aguarda 0.5/10 de segundo; 
	#--------------------------------------
	
	#Tela de créditos / input de trapaças:
	if SelectMenu == 4 and Menu == 0:	#Se o jogador ordenar a abertura deste layer e não está no menu:
		InputKey = ReadKey()					#Recebe uma string contendo o nome da tecla pressionada;
		print(InputKey)
		if InputKey == "escape":													#Se o jogador apertar a tecla "ESC":
			Menu = 1																		#Concede a permissão para o jogador voltar ao menu;
			if InputCheat == ["c", "l", "e", "a", "r"]:						#Se a sequencia de caracteres formar "clear":
				UpdateData(1, "all","all",0)										#Deleta os récordes e moedas do jogador, zera a mochila de itens e retorna às músicas padrões iniciais;
			if InputCheat == ["c", "l", "e", "a", "r", "i"]:				#Se a sequencia de caracteres formar "cleari":
				UpdateData(1, "Itens","all",0)									#Deleta os itens do jogador;
			if InputCheat == ["c", "l", "e", "a", "r", "g"]:				#Se a sequencia de caracteres formar "clearm":
				UpdateData(1, "GameSaves","all",0)								#Deleta os récordes e moedas do jogador;
			if InputCheat == ["c", "l", "e", "a", "r", "m"]:				#Se a sequencia de caracteres formar "clearg":
				UpdateData(1, "Musics","all",0)									#Deleta as músicas compradas/ganhas (retorna às músicas padrões iniciais do jogador);
			if InputCheat == ["i", "d", "d", "q", "d"]:						#Se a sequencia de caracteres formar "iddqd":
				InvulnerabilityFix = not(InvulnerabilityFix)					#Concede o jogador a invulnerabilidade fixa durante toda a partida (Modo Deus do DoomI)
			if InputCheat == ["i", "d", "k", "f", "a"]:						#Se a sequencia de caracteres formar "idkfa":
				UpdateData(0, "Itens", "all", 5)									#O jogador ganha 5 de cada item da loja (Sim, eu amo DoomI);  
			if InputCheat == ["u","n","o","d","e","f","i","r","m","a"]:	#Se a sequencia de caracteres formar "unodefirma":
				GameSpeed = GameSpeed - 5											#O jogo fica mais rápido (redução de 0.05/10 de segundo);
			if InputCheat == ["e","s","t","a","t","a","l"]:					#Se a sequencia de caracteres formar "estatal":
				GameSpeed = GameSpeed + 5											#O jogo fica mais lento (atraso de 0.05/10 de segundo);
			if InputCheat == ["t","e","l","e","s","e","n","a"]:			#Se a sequencia de caracteres formar "telesena":
				UpdateData(0, "GameSaves", "Coins", 20)						#O jogador recebe 20 moedas;
			if InputCheat == ["d","i","o"]:										#Se a sequencia de caracteres formar "dio":
				UpdateData(0, "Itens", "Zawarudo", 1)							#O jogador recebe um item "Zawarudo";
			if InputCheat == ["y", "u", "g", "i"]:								#Se a sequencia de caracteres formar "yugi":
				UpdateData(0, "Itens", "Ressurreicao", 1)						#O jogador recebe um item "Ressurreicao";
			if InputCheat == ["b","a","i","d","u"]:							#Se a sequencia de caracteres formar "baidu":
				UpdateData(0, "Itens", "Escudo", 1)								#O jogador recebe um item "Escudo";
			AtualizateData = 1														#Autoriza o programa ler o Banco de Dados;
			InputCheat = []															#Limpa a lista que guarda a sequência de caracteres;
		
		if InputKey != "escape" and InputKey != "space":	#Se as teclas pressionadas não forem "ESC" ou "Espaço":
			InputCheat.append(InputKey)							#Adiciona o nome da tecla na sequência de caracteres;

		Window.fill((0,0,0))													#Pinta o fundo de Preto (Cor fixa do fundo);
		FontSys = pygame.font.SysFont("Stencil", 120)				#Recebe a fonte "Stencil" tamanho 120;
		Font = FontSys.render("Créditos", 5, (SysColors[1][1]))	#O texto recebe a string "Créditos", branca;
		Window.blit(Font,(110,150))										#Escreve essa string na tela;
		
		FontSys = pygame.font.SysFont("Stencil", 20)				#Recebe a fonte "Stencil" tamanho 20;
		Font = FontSys.render("<--ESC", 1, (SysColors[1][1]))	#O texto recebe a string "<--ESC", branca;
		Window.blit(Font,(20,20))										#Escreve essa string na tela;

		FontSys = pygame.font.SysFont("Stencil", 30)																#Recebe a fonte "Stencil" tamanho 30;
		Font = FontSys.render("Programador: Marco Antônio Zerbielli Bee", 1, (SysColors[1][1]))	#O texto recebe a string "Programador: Marco Antônio Zerbielli Bee", branca;
		Window.blit(Font,(20,320))																						#Escreve essa string na tela;

		Font = FontSys.render("Desenv. Criativo: Lucas Lodi Valenga", 1, (SysColors[1][1]))			#O texto recebe a string "Desenv. Criativo: Lucas Lodi Valenga", branca;
		Window.blit(Font,(20,370))																						#Escreve essa string na tela;

		Font = FontSys.render("Relatório: Erika Vitória de Oliveira Cesco", 1, (SysColors[1][1]))	#O texto recebe a string "Relatório: Erika Vitória de Oliveira Cesco", branca;
		Window.blit(Font,(20,420))																						#Escreve essa string na tela;

		Font = FontSys.render("Relatório: Guilherme Tecchio Pereira", 1, (SysColors[1][1]))			#O texto recebe a string "Relatório: Guilherme Tecchio Pereira", branca;
		Window.blit(Font,(20,470))																						#Escreve essa string na tela;
			
		Font = FontSys.render("Instituto Fed.: Campus Concórdia", 1, (SysColors[1][1]))				#O texto recebe a string "Instituto Fed.: Campus Concórdia", branca;
		Window.blit(Font,(20,520))																						#Escreve essa string na tela;

		Font = FontSys.render("Data: 24/01/2021 - 02/03/2021", 1, (SysColors[1][1]))					#O texto recebe a string "Data: 24/01/2021 - 02/03/2021", branca;
		Window.blit(Font,(20,570))																						#Escreve essa string na tela;

		Font = FontSys.render("Professor: Tiago Mazzutti", 1, (SysColors[1][1]))						#O texto recebe a string "Professor: Tiago Mazzutti", branca;
		Window.blit(Font,(20,620))																						#Escreve essa string na tela;
	#-------------------------------------

	#Sair do jogo (Via seletor de layers):
	if SelectMenu == 5 and Menu == 0:	#Se o jogador ordenar a abertura deste layer e não está no menu:
		pygame.quit()							#Fecha a execução do pygame;
		exit(0)									#Encerra o python;
	#-------------------------------------
	
	#Tela de game over, quando o jogador perde, (A tela que tu mais vai ver jogando isso aqui):
	if Retry:									#Se o jogador perder a partida:
		for event in pygame.event.get():	#Verifica todos os eventos que estão acontecendo:
			if event.type == pygame.QUIT:	#Se o jogador apertar para sair ("x" no canto superior da tela):
				pygame.quit()					#Fecha a execução do pygame;
				exit(0)							#Encerra o python;
		
		Window.fill((BgColor))																	#Pinta o fundo com a cor escolhida pelo jogador;
		Key = pygame.key.get_pressed()														#Recebe uma lista com o índice das teclas pressionadas;
		FontSys = pygame.font.SysFont("Stencil", 120)									#Recebe a fonte "Stencil" tamanho 120;
		if SelectCustomBg == 2:																	#Se a cor de fundo for vermelha:
			Font = FontSys.render("GAME OVER!", 5, (SysColors[1][1]))				#O texto recebe a string "GAME OVER!", branca;
		else:																							#Se a cor de fundo não for vermelha:
			Font = FontSys.render("GAME OVER!", 5, (SysColors[2][1]))				#O texto recebe a string "GAME OVER!", vermelha;
		Window.blit(Font,(40,150))																#Escreve essa string na tela;
		
		FontSys = pygame.font.SysFont("Stencil", 30)										#Recebe a fonte "Stencil" tamanho 30;
		if SelectCustomBg == 2:																	#Se a cor de fundo for vermelha:
			Font = FontSys.render("Press 'R' to retry", 1, (SysColors[1][1]))		#O texto recebe a string "Press 'R' to retry", branca;
		else:																							#Se a cor de fundo não for vermelha:
			Font = FontSys.render("Press 'R' to retry", 1, (SysColors[2][1]))		#O texto recebe a string "Press 'R' to retry", vermelha;
		Window.blit(Font,(240,400))															#Escreve essa string na tela;

		if SelectCustomBg == 2:																	#Se a cor de fundo for vermelha:
			Font = FontSys.render("Press 'E' to exit", 1, (SysColors[1][1]))		#O texto recebe a string "Press 'E' to exit", branca;
		else:																							#Se a cor de fundo não for vermelha:
			Font = FontSys.render("Press 'E' to exit", 1, (SysColors[2][1]))		#O texto recebe a string "Press 'E' to exit", vermelha;
		Window.blit(Font,(260,440))															#Escreve essa string na tela;

		if SelectCustomBg == 2:																	#Se a cor de fundo for vermelha:
			Font = FontSys.render("Press 'F' in respect", 1, (SysColors[1][1]))	#O texto recebe a string "Press 'F' in respect", branca;
		else:																							#Se a cor de fundo não for vermelha:
			Font = FontSys.render("Press 'F' in respect", 1, (SysColors[2][1]))	#O texto recebe a string "Press 'F' in respect", vermelha;
		Window.blit(Font,(227,480))															#Escreve essa string na tela;
		
		SecondsPlayed = 0												#Zera o contador de segundos;
		MinutesPlayed = 0												#Zera o contador de minutos;
		HoursPlayed = 0												#Zera o contador de horas;
		DirMovement = 1												#Define a direção da snake como para cima;
		Zawarudo[0] = 2												#Define a direção bloqueada da parada temporal como para baixo;
		SnakeBody = [(380, 340), (380, 360), (380, 380)]	#Define o tamanho e a posição inicial do cobra;
		NewRecord = 0													#Permite que seja tocado o som se o jogador bater seu récorde;

		if Key[ord("e")]:																	#Se a tecla "e" estiver pressionada:
			pygame.time.delay(500)														#Aguarda 1/2 segundo;
			Retry = 0																		#Define a saída da tela de "Game Over";
			Menu = 1																			#Define a entrada da tela de "Game Over";
		if Key[ord("r")]:																	#Se a tecla "f" estiver pressionada:
			pygame.time.delay(500)														#Aguarda 1/2 segundo;
			Retry = 0																		#Define a saída da tela de "Game Over";
			if (UseItem[1] == "Escudo") and (DataI[UseItem[1]] > 0):			#Se o jogador equipar um ou mais escudos:
				Invulnerability = 1														#Permite a invulnerabilidade da cobra;
			if (UseItem[1] == "Ressurreicao") and (DataI[UseItem[1]] > 0):	#Se o jogador equipar um ou mais "ressurreicoes":
				SnakeReborn = 1															#Permite o renascimento da cobra;
			FoodCoordinates = ((random.randint(0,760)//20 * 20), ((random.randint(20,640))//20 * 20))
			#^Sorteia um énuplo com (x, y) para a nova posição com valores inteiros múltiplos de 20;
	#------------------------------------------------------------------------------------------

	#Tela de vitória, quando o jogador ganha, (se é que ganha...):
	if WinLayout:								#Se o jogador ganhar a partida:
		for event in pygame.event.get():	#Verifica todos os eventos que estão acontecendo:
			if event.type == pygame.QUIT:	#Se o jogador apertar para sair ("x" no canto superior da tela):
				pygame.quit()					#Fecha a execução do pygame;
				exit(0)							#Encerra o python;
		
		Window.fill((BgColor))																#Pinta o fundo com a cor escolhida pelo jogador;
		Key = pygame.key.get_pressed()													#Recebe uma lista com o índice das teclas pressionadas;
		FontSys = pygame.font.SysFont("Stencil", 120)								#Recebe a fonte "Stencil" tamanho 120;
		if SelectCustomBg == 2:																#Se a cor de fundo for vermelha:
			Font = FontSys.render("YOU WIN!!!", 5, (SysColors[1][1]))			#O texto recebe a string "YOU WIN!!!", branca;
		else:																						#Se a cor de fundo não for vermelha:
			Font = FontSys.render("YOU WIN!!!", 5, (SysColors[2][1]))			#O texto recebe a string "YOU WIN!!!", vermelha;
		Window.blit(Font,(90,150))															#Escreve essa string na tela;
		FontSys = pygame.font.SysFont("Stencil", 15)									#Recebe a fonte "Stencil" tamanho 15;
		if SelectCustomBg == 2:																#Se a cor de fundo for vermelha:
			Font = FontSys.render("Parabéns, tu jogou por {} para absolutamente nada!".format(TimePlayed), 1, (SysColors[1][1]))
			#^O texto recebe a string "Parabéns, tu jogou por {tempo jogado} para absolutamente nada!", branca;
		else:																						#Se a cor de fundo não for vermelha:
			Font = FontSys.render("Parabéns, tu jogou por {} para absolutamente nada!".format(TimePlayed), 1, (SysColors[2][1]))
			#^O texto recebe a string "Parabéns, tu jogou por {tempo jogado} para absolutamente nada!", vermelha;
		Window.blit(Font,(388 - pygame.Surface.get_width(Font)/2,300))			#Escreve essa string no centro da tela;
		FontSys = pygame.font.SysFont("Stencil", 30)									#Recebe a fonte "Stencil" tamanho 30;
		if SelectCustomBg == 2:																#Se a cor de fundo for vermelha:
			Font = FontSys.render("Press 'E' to exit", 1, (SysColors[1][1]))	#O texto recebe a string "Press 'E' to exit", branca;
		else:																						#Se a cor de fundo não for vermelha:
			Font = FontSys.render("Press 'E' to exit", 1, (SysColors[2][1]))	#O texto recebe a string "Press 'E' to exit", vermelha;
		Window.blit(Font,(262,440))														#Escreve essa string na tela;
		
		SecondsPlayed = 0												#Zera o contador de segundos;
		MinutesPlayed = 0												#Zera o contador de minutos;
		HoursPlayed = 0												#Zera o contador de horas;
		DirMovement = 1												#Define a direção da snake como para cima;
		Zawarudo[0] = 1												#Define a direção bloqueada da parada temporal como para baixo;
		SnakeBody = [(380, 340), (380, 360), (380, 380)]	#Define o tamanho e a posição inicial do cobra;
		FoodCoordinates = ((random.randint(0,760)//20 * 20), ((random.randint(20,640))//20 * 20))
		#^Sorteia um énuplo com (x, y) para a nova posição com valores inteiros múltiplos de 20;
		NewRecord = 0													#Permite que seja tocado o som se o jogador bater seu récorde;

		if Key[ord("e")]:																	#Se a tecla "e" estiver pressionada:
			pygame.time.delay(500)														#Aguarda 1/2 segundo;
			WinLayout = 0																	#Define a saída da tela de "Game Over";
			Menu = 1																			#Define a entrada da tela de "Game Over";
	#-------------------------------------------------------------
	pygame.display.update()	#Atualiza a tela;