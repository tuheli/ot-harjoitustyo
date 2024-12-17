# Arkkitehtuurikuvaus

## Sovelluksen käynnistys

Pelisovelluksen käynnistystiedosto on index_game.py.

Kenttäeditorin käynnistystiedosto on index_game.py.

## Pääasialliset komponentit

### Game

Game-luokka on pelisovellusta hallinnoiva pääkomponentti. Se on eräänlainen keskeinen kontrolleri, joka suorittaa ja integroi muita pienempiä komponentteja. Game luokassa on myös pelaajan syötettä koskevaa tilaa ja logiikkaa sekä muuta siihen läheisesti liittyvää toiminnallisuutta, jota ei ole abstraktoitu.

### Editor

Editor-luokka hallinnoi kenttäeditoria ja mahdollistaa pelikenttien muokkaamisen visuaalisesti. Se tarjoaa käyttäjälle työkalut ruutujen lisäämiseen, poistamiseen ja siirtämiseen sekä pelaajan aloituspisteen asettamiseen. Editori sisältää kameran liikuttamisen navigointia varten sekä tallennus- ja lataustoiminnot kenttädatan pysyvää säilyttämistä varten.

### Menu

Menu-luokka sisältää pelin päävalikon logiikan ja piirtämisen. Valikko tarjoaa käyttäjälle mahdollisuuden aloittaa tasoja, siirtyä editoriin ja käyttää muita toimintoja. Valikko koostuu loogisesti ja visuaalisesti erillisistä komponenteista, kuten GlowText ja GlowTextButton.

### Line

Line-luokka on yksinkertainen piirtokomponentti, joka luo suoria viivoja valikon taustalle. Luokkaa käytetään graafisiin koriste-elementteihin, jotka tuovat visuaalista ilmettä käyttöliittymään.

### GlowText
GlowText-luokka vastaa hehkuvan tekstin piirtämisestä käyttöliittymään. Se korostaa valikon otsikkoa.

### GlowTextButton(GlowText)

GlowTextButton on GlowText-luokan laajennus, joka tuo mukaan vuorovaikutteisuuden. GlowTextButton toimii nappina, joka reagoi käyttäjän hiiren klikkauksiin ja osoittamiseen.

### PhysicsEntity

PhysicsEntity-luokka sisältää koodin peliobjekteille, joilla on kyky liikkua ja törmätä pelikenttään. Se määrittelee perustason fysiikkalogiikan, kuten painovoiman, liikkeen ja törmäysten käsittelyn.

### Player(PhysicsEntity)

Player-luokka on PhysicsEntityn aliluokka, joka sisältää hyppytoiminnallisuuden sekä pelaajalle ominaisen törmäyksen tarkistuksen.

### Tilemap

Tilemap-luokka sisältää pelikentän datan, piirtämislogiikan sekä metodeita törmäysten tarkistamista varten. Tilemap tallentaa kentän ruutujen tiedot ja tarjoaa metodeita kentän ympärillä olevien ruutujen käsittelyyn.

### EditorTilemap(Tilemap)

EditorTilemap-luokka laajentaa Tilemappia tarjoamalla metodeita, joiden avulla voidaan muokata ja tallentaa muokattu pelikenttä. Se on erityisesti editorityökalua varten.

### Particle

Particle-luokka kapseloi yksittäisen partikkelin tilan ja sisältää partikkelin päivitys- ja piirtämislogiikan. 

### ParticleSystem

ParticleSystem-luokka hallinnoi useiden partikkeleiden kokonaisuutta: niiden luontia, päivitystä sekä piirtämistä.

