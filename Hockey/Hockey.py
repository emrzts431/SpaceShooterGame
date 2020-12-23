import pygame,sys,random,time,os
pygame.init()
yükseklik = 600
genişlik = 800
ekran = pygame.display.set_mode((genişlik,yükseklik))
dosya = os.path.dirname(__file__)
puan = 0
level = 1

#resimler#######################################################################
background = pygame.image.load(os.path.join(dosya,"uzunarkaplan.png"))
background2 = pygame.image.load(os.path.join(dosya,"uzunarkaplan.png"))
background3 = pygame.image.load(os.path.join(dosya,"uzunarkaplan.png"))
gemiResmi = pygame.image.load(os.path.join(dosya,"anagemi.png")).convert()
düşmanResim = pygame.image.load(os.path.join(dosya,"düşman.png")).convert()
düşmanMermi = pygame.image.load(os.path.join(dosya,"kırmızılazer.png")).convert()
gemiMermi = pygame.image.load(os.path.join(dosya,"mavilazer.png")).convert()
kaybettin_yazısı = pygame.image.load(os.path.join(dosya,"lost.png"))
booster = pygame.image.load(os.path.join(dosya,"medic.png")).convert()
kazandın_yazısı = pygame.image.load(os.path.join(dosya,"kazandın.png"))
patlama_resimleri = []
for i in range(9):
    patlama_resimleri.append("{}.png".format(i))

##################################################################################

#efektler#########################################################################
def lazer():
    lazer = pygame.mixer.music.load("mermi.mp3")
    pygame.mixer.music.play()
def düşmanpatlama():
    düşman_patlama = pygame.mixer.music.load("düşmanpatlama.mp3")
    pygame.mixer.music.play()
def gemi_patlama():
    patlama = pygame.mixer.music.load("patlama.mp3")
    pygame.mixer.music.play()
def gemi_vurulma():
    pygame.mixer.music.load("gemivurulma.mp3")
    pygame.mixer.music.play()
def iyileşme():
    pygame.mixer.music.load("iyileşme.wav")
    pygame.mixer.music.play()
##################################################################################

#müzik############################################################################
pygame.mixer.music.load("starblast.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

#Sprite`lar#########################################################################
class Gemi(pygame.sprite.Sprite):
    def __init__(self,x = genişlik/2,y = yükseklik-10):
        super().__init__()
        self.image = gemiResmi
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.rectSpeed = 6
        self.can = 100
    def update(self, *args):
        up,down,left,right = args
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x +40> 800:
            self.rect.x = 800-40
        if self.rect.y +46 < 0 :
            self.rect.y = yükseklik-46
        if self.rect.y > 590:
            self.rect.y = 590
        if left:
            self.rect.x -= self.rectSpeed
        if right:
            self.rect.x += self.rectSpeed
        if up:
            self.rect.y -= self.rectSpeed
        if down:
            self.rect.y += self.rectSpeed

        if self.can == 0:
            self.kill()
            gemi_patlama()
            time.sleep(2)
            sys.exit()

    def shoot(self):
        mermi = Mermi(self.rect.x,self.rect.y)
        all_sprites.add(mermi)
        mermiler.add(mermi)

class Mermi(pygame.sprite.Sprite):
    def __init__(self,gemix,gemiy):
        super().__init__()
        self.image = gemiMermi
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = gemix + 20
        self.rect.y = gemiy
    def update(self, *args):
        self.rect.y -= 7
        if self.rect.y > 600:
            self.kill()

class Düşman(pygame.sprite.Sprite):
    def __init__(self,x = genişlik/2,y = yükseklik/2):
        super().__init__()
        self.image = düşmanResim
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,800)
        self.rect.y = random.randrange(0,300)
        self.enemySpeedx = random.randint(5,7)
        self.enemySpeedy = random.randint(4,6)
        self.yön = 1
        self.yönler = [1,-1]


    def update(self, *args):
        seçim = random.choice(self.yönler)
        self.rect.x += self.enemySpeedx * self.yön
        self.rect.y += self.enemySpeedy * seçim
        if self.rect.x + 40 > 800:
            self.rect.x = 760
            self.yön *= -1
        if self.rect.x < 0 :
            self.rect.x = 0
            self.yön *= -1
        if self.rect.y > 250:
            self.rect.y = 250
            self.yön *= -1
        if self.rect.y < 0:
            self.rect.y = 0
            self.yön *= -1
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,5,6,89,75,44,
             46,47,48,50,76,45,31,54,74,75,78,79,80,56,45,
             72,13,16,46,75,22,78,46,51,541,564,
             635,458,42,43,21,20,74,56,12,14,13,15,50]
        seçim = random.choice(a)
        if seçim == 2:
            self.shoot()
        seçim2 = random.randint(1,1000)
        if seçim2 == 4:
            self.shoot2()


    def shoot(self):
        düşmanmermi = Düşman_Mermi(self.rect.x,self.rect.y)
        düşman_mermi.add(düşmanmermi)
        all_sprites.add(düşmanmermi)
    def shoot2(self):
        boostlar = Booster()
        boosts.add(boostlar)
        all_sprites.add(boostlar)

class Düşman_Mermi(pygame.sprite.Sprite):
    def __init__(self,düşmanx,düşmany):
        super().__init__()

        self.image = düşmanMermi
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = düşmanx+20
        self.rect.y = düşmany
        self.hız = random.randint(4,6)
    def update(self, *args):
        self.rect.y += self.hız
        if self.rect.y > 600:
            self.kill()

class Booster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = booster
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,750)
        self.rect.y = 0
    def update(self, *args):
        self.rect.y += 6
        if self.rect.y > 600:
            self.kill()

class Patlama(pygame.sprite.Sprite):
    def __init__(self,düşman):
        super().__init__()
        self.sayaç = 0
        self.düşman = düşman
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(dosya,patlama_resimleri[self.sayaç])),self.düşman.image.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.düşman.rect.center
        self.delay = 75
        self.sondeğişim = pygame.time.get_ticks()
    def update(self, *args):
        şimdi = pygame.time.get_ticks()
        if şimdi-self.sondeğişim > self.delay:
            şimdi = self.sondeğişim
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(dosya,patlama_resimleri[self.sayaç])),self.düşman.image.get_size())
            self.rect = self.image.get_rect()
            self.rect.center = self.düşman.rect.center

            self.sayaç += 1
        if self.sayaç > 8:
            self.kill()
class Boss(pygame.sprite.Sprite):
    def __init__(self,x = 283,y = 0):
        super().__init__()
        self.image = pygame.image.load(os.path.join(dosya,"boss.jpg")).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yön = 1
        self.hız = 5
        self.can = 100
        self.asagı_yukarı = [1,1,1,1,1,-1,-1,-1,-1,-1]
    def update(self, *args):
        if self.yön == 1:
            self.rect.x += self.hız
            if self.rect.x + 283 > 800:
                self.yön *= -1
        if self.yön == -1:
            self.rect.x -= self.hız
            if self.rect.x < 0:
                self.yön *= -1
        b = random.choice(self.asagı_yukarı)
        if b == 1:
            self.rect.y -= 2
            if self.rect.y < 0:
                self.rect.y = 0
        if b == -1:
            self.rect.y += 2
            if self.rect.y > 100:
                self.rect.y = 100
        a = random.randint(1,15)
        if a == 5:
            self.shoot()
        c = random.randint(1,200)
        if c == 10:
            self.shoot2()

        if self.can == 0:
            gemi_patlama()
            time.sleep(5)
            sys.exit()



    def shoot(self):
        boss_mermi = Düşman_Mermi(self.rect.x+142,self.rect.y+300)
        boss_mermileri.add(boss_mermi)
        all_sprites.add(boss_mermi)

    def shoot2(self):
        boostlar = Booster()
        boosts.add(boostlar)
        all_sprites.add(boostlar)


all_sprites = pygame.sprite.Group()
boosts = pygame.sprite.Group()
all_sprites.add(boosts)
mermiler = pygame.sprite.Group()
düşmanlar = pygame.sprite.Group()
gemi = Gemi()
all_sprites.add(gemi)
düşman_mermi = pygame.sprite.Group()
boss_mermileri = pygame.sprite.Group()
bosslar = pygame.sprite.Group()



######################################################################################

#Level#################################################################################
for i in range(5):
    düşman = Düşman()
    düşmanlar.add(düşman)
    all_sprites.add(düşman)

######################################################################################

def Kalkan(ekran,x,y,değer):
    x = int(x)
    y = int(y)
    değer = int(değer)
    if gemi.can < 0:
        gemi.can = 0
    bar_uzunluk = int(100)
    bar_yükseklik = int(10)
    doldurulacak_yer = int(((değer/100)) * bar_uzunluk)
    dış_çerçeve = pygame.Rect(x,y,bar_uzunluk,bar_yükseklik)
    boyancak_yer = pygame.Rect(x,y,(doldurulacak_yer),bar_yükseklik)

    pygame.draw.rect(ekran,(255,255,255),dış_çerçeve,3)
    if gemi.can >= 60:
        pygame.draw.rect(ekran,(0,255,0),boyancak_yer)
    elif gemi.can >= 40:
        pygame.draw.rect(ekran,(255,255,0),boyancak_yer)
    elif gemi.can < 40:
        pygame.draw.rect(ekran,(255,0,0),boyancak_yer)

boss = Boss()
yer1 = -985
clock = pygame.time.Clock()
sayaç_sıfırlama = True
sayaç_sıfırlama2 = True
#Ana oyun loopu###########################################################################
while True:
    düşman_sayısı = len(düşmanlar)
    clock.tick(60)
    ekran.fill((0, 0, 0))
    yer1 += 5
    resim = ekran.blit(background,(0,yer1))
    if yer1 ==0:
        yer1 = -985
        resim2 = ekran.blit(background2,(0,yer1))
        resim2 = resim

    Kalkan(ekran, 10,10,gemi.can)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lazer()
                gemi.shoot()
    font = pygame.font.SysFont("Normal",48)
    PuanYazı = font.render("Puan : {}".format(puan),1, (255, 255, 255), (0, 0, 0))
    ekran.blit(PuanYazı,(600,550))

    all_sprites.draw(ekran)
    up,down,left,right = keys[pygame.K_UP],keys[pygame.K_DOWN],keys[pygame.K_LEFT],keys[pygame.K_RIGHT]
    all_sprites.update(up,down,left,right)
    durum = pygame.sprite.spritecollide(gemi,düşman_mermi,True)
    durum2 = pygame.sprite.spritecollide(gemi,düşmanlar,False)
    durum3 = pygame.sprite.groupcollide(mermiler,düşmanlar,True,True)
    can_boostlama = pygame.sprite.spritecollide(gemi,boosts,True)


    if durum:
        gemi.can -= 25
        gemi_vurulma()
        if gemi.can == 0:
            ekran.blit(kaybettin_yazısı,kaybettin_yazısı.get_rect())
    if durum2:
        gemi.can = 0
        ekran.blit(kaybettin_yazısı, kaybettin_yazısı.get_rect())
    if durum3:
        düşmanpatlama()
        for enemies in durum3.values():
            for enemy in enemies:

                kaboom = Patlama(düşman=enemy)
                all_sprites.add(kaboom)
        puan += 10
    if düşman_sayısı == 0 and level < 10:
        if sayaç_sıfırlama:
            bitişdeğeri = pygame.time.get_ticks()
            sayaç_sıfırlama = False
            LevelYazıFont = pygame.font.SysFont("Helvetica",50)
            yazı = LevelYazıFont.render("Level {}".format(level+1),1,(0,255,0))
        ekran.blit(yazı,(10,30))
        if pygame.time.get_ticks() - bitişdeğeri > 4000:
            sayaç_sıfırlama = True
            level += 1
            for i in range(level * 3):
                düşman = Düşman()
                düşmanlar.add(düşman)
                all_sprites.add(düşman)


    if level == 10:
        def boss_kalkan(ekran, x, y, değer):
            x = int(x)
            y = int(y)
            değer = int(değer)
            if boss.can < 0:
                boss.can = 0
            bar_uzunluk = int(100)
            bar_yükseklik = int(10)
            doldurulacak_yer = int(((değer / 100)) * bar_uzunluk)
            dış_çerçeve = pygame.Rect(x, y, bar_uzunluk, bar_yükseklik)
            boyancak_yer = pygame.Rect(x, y, (doldurulacak_yer), bar_yükseklik)
            pygame.draw.rect(ekran, (255, 255, 255), dış_çerçeve, 3)
            pygame.draw.rect(ekran, (255, 0, 0), boyancak_yer)

        boss_kalkan(ekran=ekran, x=10, y=500, değer=boss.can)
        durum4 = pygame.sprite.spritecollide(gemi,boss_mermileri,True)
        durum5 = pygame.sprite.spritecollide(boss,mermiler,True)
        if sayaç_sıfırlama2:
            bitişdeğeri2 = pygame.time.get_ticks()
            sayaç_sıfırlama2 = False

            all_sprites.add(boss)
            for enemy in düşmanlar:
                enemy.kill()
        if durum4:
            gemi_vurulma()
            gemi.can -= 25
            if gemi.can == 0:
                ekran.blit(kaybettin_yazısı, kaybettin_yazısı.get_rect())

        if durum5:
            düşmanpatlama()
            boss.can -=1
            if boss.can == 0:
                ekran.blit(kazandın_yazısı,(0,0))

    if can_boostlama:
        if gemi.can <= 75:
            iyileşme()
            gemi.can += 25







    pygame.display.update()

##################################################################################################
