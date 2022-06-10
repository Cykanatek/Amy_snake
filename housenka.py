# KÓD v jazyce Python pro Tkinter #
# Název souboru / modulu:  gui_housenky.py
# Popis programu:  program demonstruje jednoduchou hru, kdy housenka ovládaná šipkami pojídá kolečka
# Autor: Michal Kočer - upraveno Amálie Jirotková 3.r. IVT 2021/2022
######################################################################################

# MODULY
from tkinter import *
import tkinter
import random
import math

# NEZNÁMÉ
player1 = ""
player2 = ""


######################################################################################

# Deklarace tříd


class Clanek(object):
    """
     Třída pro jeden článek housenky
    """

    def __init__(self, canvas, x, y, r, barva) -> None:
        """
        Konstruktor článku housenky: 
           canvas ... plátno 
           x, y ... poloha článku
           r ... polomer článku
           barva ... barva článku
        """
        # deklarace atributů instance
        self.canvas = canvas
        self.x, self.y = x, y
        self.r = r
        self.barva = barva
        self.id = None  # užijeme na konrétní odkaza na ID prvku na canvasu

    def kresli(self):
        """
         metoda pro vykreslení článku na canvas
        """
        # výpočet bounding boxu (nejmenšího ohraničující rámečku)
        x1 = self.x - self.r
        y1 = self.y - self.r
        x2 = self.x + self.r
        y2 = self.y + self.r
        # vykreslení oválu na canvas a uložení identifikátoru prvku do proměnné self.id
        self.id = self.canvas.create_oval(x1, y1, x2, y2, fill=self.barva)
        return self.id

    def zmen_barvu(self, barva):
        """
         metoda pro změnu barvy článku
        """
        self.barva = barva  # uložíme barvu pro další referenci jako parametr instance
        if self.id is not None:  # v přápadě, že článek byl vykreslen
            self.canvas.itemconfig(self.id, fill=barva)  # změníme barvu vykreleného článku

    def zmiz(self):
        """
         metoda odstraní článek z canvasu 
        """
        if self.id is not None:
            self.canvas.delete(self.id)

    def je_nademnou(self, clanek):
        """
         funkce navrací boolean podle toho zda se na canvase prolne
         aktuální instance s instancí zadanou jako parametr "clanek"
        """
        if clanek.id in self.canvas.find_all():  # zjistí zda je clánek zobrazen na canvasu
            x1, y1, x2, y2 = self.canvas.bbox(clanek.id)  # zjistí bounding box zobrazeného článku
            # následující zjistí zda se zobrazené jídlo (identifikátor mé instance jídla na canvasu)
            # vyskytuje v seznamu všech objektů, které se nachází ve vyznačeném obdélníku
            if self.id in self.canvas.find_overlapping(x1, y1, x2, y2):
                return True


######################################################################################


class Jidlo(Clanek):
    """
     třída pro zobrazení jídla pro housenku
     dědí od třídy článek s tím, že přidává instantci třídy navíc parametr hodnota
     a kontrolu existence jiného objektu, který se s jídlem na canvase prolíná
    """

    def __init__(self, canvas, x, y, r, barva, hodnota) -> None:
        """
         upravený konstruktor
        """
        super().__init__(canvas, x, y, r, barva)
        self.hodnota = hodnota

    def je_nademnou(self, clanek):
        """
         funkce navrací boolean podle toho zda se na canvase prolne
         aktuální instance s instancí zadanou jako parametr "clanek"
        """
        if clanek.id in self.canvas.find_all():  # zjistí zda je clánek zobrazen na canvasu
            x1, y1, x2, y2 = self.canvas.bbox(clanek.id)  # zjistí bounding box zobrazeného článku
            # následující zjistí zda se zobrazené jídlo (identifikátor mé instance jídla na canvasu)
            # vyskytuje v seznamu všech objektů, které se nachází ve vyznačeném obdélníku
            if self.id in self.canvas.find_overlapping(x1, y1, x2, y2):
                return True


######################################################################################


class Housenka(object):
    """
      třída na vytváření housenek
    """

    def __init__(self, canvas, x, y, r, delka, barvaHlavy, barvaClanku, rychlost) -> None:
        """
          konstruktor tvorby instance housenky:
             canvas ... plátno pro kreslení housenky
             x, y ... poloha hlavičky
             delka ... počet článků housenky (včetně hlavičky)
             barvaHlavy ... barva hlavičky
             barvaClanku ... barva článku
             rychlost ... vektor rychlosti [vx, vy] !!! budeme používat jen vektory jednotkové
                        [-1,0] vlevo, [1,0] vpravo, [0,-1] nahoru, [0,1] dolů
        """
        self.delka = delka
        self.canvas = canvas
        self.x, self.y, self.r = x, y, r
        self.rychlost = rychlost
        self.clanky = []  # seznam pro uchování vytvořených článků housenky
        for i in range(delka):
            xc = x + (2 * r) * (-rychlost[0]) * i  # x-ová souřadnice i-tého článku
            yc = y + (2 * r) * (-rychlost[1]) * i  # y-ová souřadníce i-tého článku
            clanek = Clanek(self.canvas, xc, yc, r, barvaClanku)  # konstrukce instance tridy Clanek
            clanek.kresli()  # vykreslení článku
            self.clanky.append(clanek)  # uložení článku do seznamu článků
        self.clanky[0].zmen_barvu(barvaHlavy)  # prvnímu článku změníme barvu na barvu hlavičky
        ######################################################################################

    def zmen_rychlost(self, rychlost):
        """
         metoda pro změnu rychlosti 
        """
        self.rychlost = rychlost
        ######################################################################################

    def get_hlava(self):
        """
         metoda vrací odkaz na instanci článku hlavičky
        """
        return self.clanky[0]
        ######################################################################################

    def krok(self):
        """
         metoda pro učenění jednoho kroku housenky
        """
        hlavicka = self.get_hlava()  # najdu článek s hlavičkou
        barva_hlavicky = hlavicka.barva  # uložím si barvu současné hlavičky#
        prvni_clanek = self.clanky[1]  # najdu další článek
        # !! pozor housenka MUSI mít vedle hlavičky ještě jeden článek
        barva_clanku = prvni_clanek.barva  # uložíme si barvu článku
        hlavicka.zmen_barvu(barva_clanku)  # změníme barvu hlavičky na barvu článku
        # vytvořím nový článek ve směru vektoru rychlosti pohybu
        xc = hlavicka.x + (2 * self.r * self.rychlost[0])
        yc = hlavicka.y + (2 * self.r * self.rychlost[1])
        # PODIVAM jestli nejsem mimo canvas
        if xc <= -self.r:
            xc = self.canvas.sirka
        elif xc >= (self.canvas.sirka + self.r):
            xc = 0
        if yc <= -self.r:
            yc = self.canvas.vyska
        elif yc >= (self.canvas.vyska + self.r):
            yc = 0
        nova_hlavicka = Clanek(self.canvas, xc, yc, self.r, barva_hlavicky)
        nova_hlavicka.kresli()  # vykrelíme nový článek (hlavičku)
        # přidám článek do seznamu článků
        self.clanky.insert(0, nova_hlavicka)  # nový článek zařadíme v seznamu na začátek (index 0)
        # smažeme poslední článek
        self.clanky[-1].zmiz()  # zmizí poslední článek (index -1) z canvasu
        self.clanky.remove(self.clanky[-1])  # smažeme smazaný rlánek ze seznamu článků
        ######################################################################################

    def pridej_clanek(self):
        """
         přidáme článek na konec housenky, resp. pod poslední článek
        """
        ocas = self.clanky[-1]  # najdu poslední článek
        # vytvořím nový článek  na místě posledního článku
        clanek = Clanek(self.canvas, ocas.x, ocas.y, self.r, ocas.barva)
        self.delka += 1
        clanek.kresli()  # ten vykreslím
        # přidám článek na konec seznamu článků
        self.clanky.append(clanek)


######################################################################################
class Platno(tkinter.Canvas):
    """
     rozšíření třídy tkinter.Canvas o možnost uložení šířky a výšky canvasu jako parametr instance
     .sirka a .vyska
    """

    def __init__(self, okno, width, height, background):
        super().__init__(okno, width=width, height=height, background=background)
        self.sirka = width
        self.vyska = height


class App(tkinter.Tk):
    """
     třída vlastní aplikace
    """

    def __init__(self, titulek, sirka, vyska, barva="White"):
        super().__init__()
        # NASTAVENI HLAVNIHO OKNA aplikace
        self.title(titulek)  # nastavení titulku okna
        self.geometry("+1200+100")
        # přidán nápis
        self.napis = tkinter.Label(self, text="Housenky", bg="red", fg="yellow", font="Arial 30 bold")
        self.napis.pack(fill=tkinter.X)  # použití layout manageru PACK, vyplnění přes celou osu X
        # přidání plátna (canvasu)
        self.canvas = Platno(self, width=sirka, height=vyska, background=barva)
        self.canvas.pack()  # použití layout manageru PACK bez parametrů
        # přidání tlačítka "Quit", které spustí funkci self.klik_tlacitka() - obsluhu události stisku
        self.tlacitko = tkinter.Button(self, text="Quit", command=self.klik_tlacitka)
        self.tlacitko.pack()  # použití layout manageru PACK bez parametrů
        # tvoříme menubar
        self.menubar = tkinter.Menu(self)  # s hlavní oknem aplikace self bude souviset menubar
        # filemenu - vytvoření robalovací nabídky menu - spojené s menubarem
        self.fileMenu = tkinter.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="New", command=self.destroy, state=tkinter.DISABLED)
        self.fileMenu.add_command(label="Open", command=self.destroy, state=tkinter.DISABLED)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Ukončit", command=self.destroy)
        # settingsMenu - vytvoření další robalovací nabídky menu - spojené s menubarem
        self.menuNastaveni = tkinter.Menu(self.menubar, tearoff=0)
        self.menuNastaveni.add_command(label="Černá", command=self.zmen_na_cernou)
        self.menuNastaveni.add_command(label="Zelená", command=self.zmen_na_zelenou)
        # spojime s fileMenu s menubarem - napojíme rozbalovací nabídky na volby v menubaru
        self.menubar.add_cascade(label="Soubor", menu=self.fileMenu)
        self.menubar.add_cascade(label="Nastavení", menu=self.menuNastaveni)
        # celé hotové menu označíme jako hlavní menu, které má okno teď zobrazit
        self.config(menu=self.menubar)
        # kreslime housenky
        self.housenka1 = Housenka(self.canvas, 150, 150, 10, 3, "silver", "yellow", [-1, 0])
        self.housenka2 = Housenka(self.canvas, 100, 100, 10, 3, "gold", "yellow", [-1, 0])
        # kreslime jidlo
        self.jidla = []  # seznam všech jídel na canvas
        for i in range(2):
            # na náhodném místě vykreslíme n zkazených jídel
            x = random.randint(10, sirka - 10)
            y = random.randint(10, vyska - 10)
            # vytvořejí jednoho jídla s hodnotou -100
            jidlo = Jidlo(self.canvas, x, y, 10, "red", -100)
            jidlo.kresli()
            # zařazení jídla na konec seznamu jídel
            self.jidla.append(jidlo)

        for i in range(5):
            # na náhodném místě vykreslíme n jídel
            x = random.randint(10, sirka - 10)
            y = random.randint(10, vyska - 10)
            # vytvořejí jednoho jídla s hodnotou 100
            jidlo = Jidlo(self.canvas, x, y, 10, "blue", 100)
            jidlo.kresli()
            # zařazení jídla na konec seznamu jídel
            self.jidla.append(jidlo)

            # zařazení jídla na konec seznamu jídel

        # vazby udalosti
        self.housenka1.canvas.bind("<Left>", self.krok_vlevo1)
        self.housenka1.canvas.bind("<Right>", self.krok_vpravo1)
        self.housenka1.canvas.bind("<Up>", self.krok_nahoru1)
        self.housenka1.canvas.bind("<Down>", self.krok_dolu1)
        self.housenka1.canvas.bind("p", self.housenka1.pridej_clanek)
        self.housenka1.canvas.focus_set()  # získání fokusu vstupu z klávesnice
        self.housenka2.canvas.bind("<a>", self.krok_vlevo2)
        self.housenka2.canvas.bind("<d>", self.krok_vpravo2)
        self.housenka2.canvas.bind("<w>", self.krok_nahoru2)
        self.housenka2.canvas.bind("<s>", self.krok_dolu2)
        self.housenka2.canvas.bind("p", self.housenka2.pridej_clanek)
        self.housenka2.canvas.focus_set()  # získání fokusu vstupu z klávesnik
        self.update()
        self.after(200, self.krok_vpred1)  # časovač pro jeden krok vpřed
        self.after(200, self.krok_vpred2)  # časovač pro jeden krok vpřed

    def run(self):
        # Hlavní smyčka Tk (čekání na události)
        self.mainloop()

    # OBSLUHY událostí
    def klik_tlacitka(self):
        self.destroy()

    def zmen_na_cernou(self):
        self.canvas.config(background="black")

    def zmen_na_zelenou(self):
        self.canvas.config(background="green")

    # POKUS O POJEMNOVÁNÍ HRÁČŮ
    """
    def Take_input(self):
        player1 = ""
        player2 = ""
        print("----HRÁČI----")
        player1 = INPUT = inputtxt1.get("1.0",'end-1c')
        print("hráč 1: ", player1)
        player2 = INPUT = inputtxt2.get("1.0",'end-1c')
        print("hráč 2: ", player2)
        print("--------------")

    p1 = Label(text = "Zadejte jméno hráče 1 (šipky)")
    inputtxt1 = Text(root, height = 0,
                    width = 15,
                    bg = "light yellow")

    p2 = Label(text = "Zadejte jméno hráče 2 (wsad)")
    inputtxt2 = Text(root, height = 0,
                    width = 15,
                    bg = "light yellow")

    Display = Button(root, height = 2,
                    width = 20,
                    text ="Hrát",
                    command = lambda:[Take_input(), Game(), End()])
    
    ##spuštění
    p1.pack()
    inputtxt1.pack()
    p2.pack()
    inputtxt2.pack()
    Display.pack()
    mainloop()
    """

    # kroky housenka1
    def krok_vlevo1(self, udalost):
        self.housenka1.zmen_rychlost([-1, 0])

    def krok_vpravo1(self, udalost):
        self.housenka1.zmen_rychlost([1, 0])

    def krok_nahoru1(self, udalost):
        self.housenka1.zmen_rychlost([0, -1])

    def krok_dolu1(self, udalost):
        self.housenka1.zmen_rychlost([0, 1])

    # kroky housenka2
    def krok_vlevo2(self, udalost):
        self.housenka2.zmen_rychlost([-1, 0])

    def krok_vpravo2(self, udalost):
        self.housenka2.zmen_rychlost([1, 0])

    def krok_nahoru2(self, udalost):
        self.housenka2.zmen_rychlost([0, -1])

    def krok_dolu2(self, udalost):
        self.housenka2.zmen_rychlost([0, 1])

    # krok na jdeno tiknutí 1
    def krok_vpred1(self):
        global sezrane
        self.housenka1.krok()  # housenka udělá jeden krok
        # JEDENI JIDLA 1
        for jidlo in self.jidla:  # projdeme všechna zobrazená jídla
            sezrane = []  # seznam právě snědených jídel
            # podíváme se zda se hlavička housenky překrývá s tímto jedním jídlem
            if jidlo.je_nademnou(self.housenka1.get_hlava()) and jidlo.barva == "red":
                self.destroy()
                print("-> Vyhrál hráč 2")
            elif jidlo.je_nademnou(self.housenka1.get_hlava()):
                # v případě, že se hlavička překrývá s jídlem přidáme housence článek
                self.housenka1.pridej_clanek()
                # necháme zmizet jídlo z canvasu
                jidlo.zmiz()
                # abychom mohli jídlo smazat ze seznamu jídel, přidáme jej do seznamu snědených
                sezrane.append(jidlo)
                #  podmínka pro limit po sežrání věech jídel - nevím, proč nefunguje, už to běželo, jen jsem něco
                # provedla a nějak pokazilo to samé pak na řádku 360-362
                if len(sezrane) == 5:
                    self.destroy()
                    self.ahoj()

        for clanek in self.housenka1.clanky:
            if clanek.je_nademnou(self.housenka2.get_hlava()):
                self.destroy()

        for clanek in self.housenka2.clanky:
            if clanek.je_nademnou(self.housenka1.get_hlava()):
                self.destroy()

        # krok na jedno tiknutí 2
        for jidlo in sezrane:
            self.jidla.remove(jidlo)  # každé snězené jídlo smažeme ze seznamu jídel
        self.after(200, self.krok_vpred1)  # další tiknutí za 200ms

    def krok_vpred2(self):
        global sezrane
        self.housenka2.krok()  # housenka udělá jeden krok
        # KONROLA POLOHY - taky nevím, jak toto úplně zprovoznit...
        """for clanek in self.housenka1.clanky:
            if clanek.je_nademnou_(self.housenka2.get_hlava()) == True:
                self.destroy()"""
        # JEDENI JIDLA 2d
        for jidlo in self.jidla:  # projdeme všechna zobrazená jídla
            sezrane = []  # seznam právě snědených jídel
            # podíváme se zda se hlavička housenky překrývá s tímto jedním jídlem
            if jidlo.je_nademnou(self.housenka2.get_hlava()) and jidlo.barva == "red":
                self.destroy()
                print("-> Vyhrál hráč 1")
            elif jidlo.je_nademnou(self.housenka2.get_hlava()):
                # v případě, že se hlavička překrývá s jídlem přidáme housence článek
                self.housenka2.pridej_clanek()
                # necháme zmizet jídlo z canvasu
                jidlo.zmiz()
                # abychom mohli jídlo smazat ze seznamu jídel, přidáme jej do seznamu snědených
                sezrane.append(jidlo)
                if len(sezrane) == 5:
                    self.destroy()
                    self.ahoj()
            for clanek in self.housenka2.clanky:
                if clanek.je_nademnou_(self.housenka2.get_hlava()):
                    self.destroy()
        # projdeme seznam snědených jídel
        for jidlo in sezrane:
            self.jidla.remove(jidlo)  # každé snědené jídlo smažeme ze seznamu jídel
        self.after(200, self.krok_vpred2)  # další tiknutí za 200ms

    def ahoj(self):
        print("Bye!")
        print("-----BODY-----")
        print("hráč 1: ", self.housenka1.delka)
        print("hráč 2: ", self.housenka2.delka)
        print("--------------")
        if self.housenka1.delka > self.housenka2.delka:
            print("-> Vyhrál hráč 1")
        elif self.housenka1.delka < self.housenka2.delka:
            print("-> Vyhrál hráč 2")
        else:
            print("-> Remíza")


######################################################################################
# HLAVNÍ PROGRAM

def Game():
    if __name__ == "__main__":
        app = App("Housenky", 400, 400, barva="dark green")
        # rozběhneme aplikaci
    app.run()


Game()
# KONEC PROGRAMU
