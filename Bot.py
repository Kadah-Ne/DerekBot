#Importation des librairies nécessaires
import discord
import asyncio
from discord.ext import commands
from discord import Spotify
from dotenv import load_dotenv
from random import *
import os
import requests
import json
from datetime import datetime, datetime


intents = discord.Intents.all()
load_dotenv(dotenv_path="config")
bot = commands.Bot(command_prefix='!', description = "Notre Derek",intents=intents)





def emoteListUpdate():
    emoteFile = open("EmoteList","r")
    for mojies in emoteFile:
        if len(mojies) > 7 and mojies.strip("\n") not in EmoteList:
            EmoteList.append(mojies.strip("\n"))

    emoteFile.close()



def geolocalisation(adresse : str):
    
    page = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={adresse}&limit=1")
    return(page.json()["features"][0]["geometry"]["coordinates"])

def meteo4Heures(meteo : json) -> tuple:
    heureActuel = str(datetime.now()).split()
    heures = heureActuel[1].split(":")[0]
    jours = heureActuel[0].split("-")
    occurence = 0

    #Temperature pour les 4 prochaines heures
    for i in meteo["hourly"]["time"]:
        heuresMeteo = i.split("T")[1].split(":")[0]
        joursMeteo = i.split("T")[0].split("-")
        if(jours[0]>joursMeteo[0] or jours[1]>joursMeteo[1] or jours[2]>joursMeteo[2] or heures > heuresMeteo):
            occurence +=1
        else:
            break
    listeTemp=[]
    listForecast=[]
    for i in range(5):
        listeTemp.append(meteo["hourly"]["temperature_2m"][occurence+i])
        listForecast.append(meteo["hourly"]["weathercode"][occurence+i])
    return (listeTemp,listForecast)



def meteoJournaliere(meteo : json) -> tuple:
    aujourdhui = str(datetime.now()).split()[0].split("-")[2]
    occurence = 0
    for i in meteo["daily"]["time"]:
        if (i.split("T")[0].split("-")[2])!=aujourdhui:
            occurence+=1
        else:
            break
    forecast = meteo["daily"]["weathercode"][occurence]
    occurence = 0
    for i in meteo["hourly"]["time"]:
        if (i.split("T")[0].split("-")[2])!=aujourdhui:
            occurence+=1
        else:
            break
    prepMoy=[]
    for i in range(12):
        prepMoy.append(meteo["hourly"]["temperature_2m"][occurence+7+i])
        #                                       Miam le bon scotch ^

    moyenneTemp = 0
    for i in prepMoy:
        moyenneTemp+=i
    return (forecast,moyenneTemp/len(prepMoy))

def journalisteMeteo(code : int) -> str:
    match code:
        case 0:
            return ":sun_with_face:"
        case 1:
            return ":white_sun_small_cloud: "
        case 2:
            return ":white_sun_cloud:"
        case 3:
            return ":cloud:"
        case 45:
            return ":fog:"
        case 48:
            return ":fog::icecube:"
        case 51:
            return ":white_sun_rain_cloud: "
        case 53:
            return ":white_sun_rain_cloud: "
        case 55:
            return ":white_sun_rain_cloud:"
        case 56:
            return ":white_sun_rain_cloud::ice_cube:"
        case 57:
            return ":white_sun_rain_cloud::ice_cube:"
        case 61:
            return ":cloud_rain:"
        case 63:
            return ":cloud_rain:"
        case 65:
            return ":cloud_rain:"
        case 66:
            return ":cloud_rain::ice_cube:"
        case 67:
            return ":cloud_rain::ice_cube:"
        case 71:
            return ":snowflake:"
        case 73:
            return ":cloud_snow:"
        case 75:
            return ":snowman:"
        case 77:
            return ":snowflake::ice_cube:"
        case 80:
            return ":umbrella:"
        case 81:
            return ":umbrella:"
        case 82:
            return ":umbrella:"
        case 85:
            return ":cloud_snow:"
        case 86:
            return ":cloud_snow:"
        case _:
            return "Code non reconnu, contacter Kadah Ne #2737"
            
@bot.event
async def on_ready():
    print("Derekbot est dans la place")


@bot.command(name = "meteo", help = "La meteo de Derek")
async def Meteo(ctx, * address:str):
    query=""
    addressMSG=""
    for i in address:
        query +="+"+i
        addressMSG+= " "+i
    liste = geolocalisation(query)
    lat = liste[1]
    lon = liste[0]
    meteo = (requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weathercode&daily=weathercode&timezone=Europe%2FBerlin")).json()
    temperatures = meteo4Heures(meteo)[0]
    forcast = meteo4Heures(meteo)[1]
    forcastH=[]
    for i in forcast:
        forcastH.append(journalisteMeteo(i))
    #Meteojournaliere
    tmp = meteoJournaliere(meteo)
    forecastD = journalisteMeteo(tmp[0])
    message = f"Temperatures a {addressMSG} pour les 4 prochaines heures : \nNow : {temperatures[0]}°C, météo : {forcastH[0]}\nH+1 : {temperatures[1]}°C, météo : {forcastH[1]}\nH+2 : {temperatures[2]}°C, météo : {forcastH[2]}\nH+3 : {temperatures[3]}°C, météo : {forcastH[3]}\nTemperature moyenne sur la journée : {round(tmp[1],2)}°C\nPire conditions météo de la journée : {forecastD}"
    await ctx.channel.send(message)



@bot.command(name = "derekNorris", help = "Livre de blagues sur chuck norris")
async def DerekNorris(ctx):
    page = requests.get("https://api.chucknorris.io/jokes/random")
    liste = page.json()

    await ctx.channel.send(liste['value'])

@bot.command(name = "derekSagesse", help = "Besoin d'aide pour quelque chose ? DerekBot peut partager avec vous son immense sagesse")
async def Xagesse(ctx):
    page = requests.get("https://api.kanye.rest/")
    liste = page.json()

    await ctx.channel.send(liste['quote'])


@bot.command(name = "hello", help = "DerekBot vous dit bonjour")
async def hello(ctx, user : discord.Member = None):
    user = user or ctx.author
    await ctx.channel.send("Salut "+user.name+" j'aime bien ta PP")
    await ctx.channel.send(user.avatar_url)    

@bot.command(name = "daleatoire", help = "Génére une emote aléatoire parmis la liste des emotes de Derekbot")
async def randomEmote(ctx):
    number = randint(0,len(EmoteList)-1)
    await ctx.channel.send(EmoteList[number])


@bot.command(name = "addMoji", help = "Ajoute un emoji a la liste de Xavbot pour qu'il puisse l'utiliser /!\ mettre des espaces entres les emotes")
async def addMoji(ctx, * emojies: discord.Emoji):
    for emoji in emojies:
        mojiId = str(emoji)
        if emoji in EmoteList:
            await ctx.channel.send("J'ai déjà cette emote bro, la preuve "+mojiId)
        else:
            emoteFile = open("EmoteList","a")
            emoteFile.write(mojiId+"\n")
            emoteFile.close()
            await ctx.channel.send("ok j'ai ajouté " + mojiId + " a ma liste d'emotes.")

    emoteListUpdate()

@bot.command(name = "mojiesList",help="Affiche la liste des emojies dans la liste de Derekbot")
async def mojiesList(ctx):
    message = "Voici la liste des emojies customs que je peux utilisé : "
    for mojies in EmoteList:
        message += (mojies +" ")
    await ctx.channel.send(message)


def createRandomVerbList():
    longAsFStringVerbes = "être avoir faire dire voir prendre pouvoir parler aller savoir donner passer mettre partir trouver rire vivre laisser rendre sourire venir comprendre penser chercher croire entendre tenir demander souvenir attendre sortir regarder jouer écrire connaître devenir mourir rester retrouver entrer manger tomber tirer lire suivre répondre obtenir perdre expliquer assurer servir porter montrer étranger éviter arriver vouloir reconnaître monter boire oublier poser aimer arrêter sentir atteindre revenir devoir changer dormir permettre quitter reprendre appeler dîner apprendre empêcher établir travailler garder marcher imaginer considérer tendre lever tourner gagner recevoir revoir aider créer découvrir compter tuer courir rentrer réaliser toucher finir descendre ajouter essayer présenter coucher occuper asseoir payer jeter définir déjeuner agir choisir distinguer préparer apparaître remettre raconter échapper acheter rejoindre battre écouter offrir glisser conduire paraître exprimer pleurer étudier retourner accepter défendre maintenir rappeler continuer commencer disparaître produire officier observer apporter former admettre retenir fournir déterminer pousser rencontrer fixer construire constater remarquer cacher développer prévoir préciser réduire constituer résoudre crier sauver remonter imposer naître envoyer souffrir tenter juger bouger exercer intervenir supporter mesurer sauter apercevoir conserver représenter placer traiter appliquer remplacer baiser étendre affirmer mener satisfaire réfléchir chanter vendre traverser fier décider entraîner avancer refuser abandonner protéger noter remplir fermer dégager ramener poursuivre couper embrasser décrire répéter organiser vérifier danser espérer frapper avouer exister accomplir couler élever parvenir arracher citer provoquer renoncer approcher lancer séparer transformer examiner justifier installer respirer rêver prévenir taire plancher relever livrer pénétrer détruire rouler discuter modifier participer régler engager employer profiter envisager concevoir soutenir promener conclure nourrir prouver douter laver disposer aboutir dépasser intéresser prononcer apprécier assister rechercher lutter marquer effectuer rompre partager supposer accorder casser procéder convaincre éloigner emporter augmenter introduire évoquer amener enlever désigner franchir écarter réveiller proposer calculer diriger posséder retirer voler durer crever résister deviner tromper dresser céder prêter craindre couvrir ménager traîner cesser traduire confondre aborder peindre entreprendre débarrasser comparer entretenir plaindre amuser attaquer fabriquer combattre accroître ignorer reposer attirer songer opposer emmener visiter améliorer annoncer éprouver accompagner recommencer conseiller brûler adresser adapter prétendre rapprocher confier indiquer nier signaler serrer démontrer réussir soumettre appuyer surveiller prier éclater super chasser acquérir endormir attribuer souligner épouser adopter interroger éclairer révéler limiter demeurer consacrer faciliter inventer libérer ranger plaire goûter boucher communiquer effacer exécuter rocher réunir repartir respecter refaire forcer interpréter contrôler vaincre ficher lâcher trembler supprimer identifier opérer diminuer imiter insister manifester admirer rétablir filer contenter mêler nommer exposer écraser achever marier jouir surprendre fondre soulever allumer dissimuler briser consulter obéir reconstituer enfoncer analyser éliminer étonner terminer procurer peser contempler transporter ressembler classer éteindre inscrire déplacer habiter attacher ramasser sonner accueillir substituer soigner déceler fumer arranger parcourir veiller claquer reculer publier compléter hésiter téléphoner contenir transmettre dominer causer situer détacher fonctionner rassurer avaler associer rassembler saluer briller commander valoir recueillir reproduire taper mentir isoler multiplier rattraper orienter affronter enseigner user falloir enfermer dessiner favoriser retomber pratiquer recourir abattre baisser bénéficier exiger fonder réparer risquer vider percevoir comporter accéder composer caresser formuler prolonger signer varier détourner consoler rapporter éveiller calmer regagner survivre renforcer plonger réclamer ressortir attraper négliger figurer chier corriger hurler craquer préserver récupérer accrocher grandir reprocher habiller tarder déposer assumer évaluer susciter noyer regretter remuer exploiter remercier rejeter déduire charger inviter échanger appartenir persuader planter percer tracer distraire bâtir combler guider déranger déclarer inquiéter plier interrompre bouffer secouer entrevoir souffler souhaiter allonger confirmer discerner réagir grimper pardonner repérer presser estimer creuser clocher lier boulanger verser refermer piquer repousser obliger pencher informer étouffer conquérir correspondre déchiffrer ressentir sacrifier subsister mordre désirer encourager excuser explorer nettoyer coller délivrer gêner avertir ôter élargir intégrer renouveler garantir répandre fouiller oser résumer pisser interdire venger convenir surmonter rédiger jaillir contribuer emprunter défiler agiter séduire revivre défaire signifier flotter concilier croître émettre suffire concentrer renverser renvoyer commettre inspirer chauffer troubler balancer enregistrer mentionner réserver soucier réchauffer élaborer assimiler dénoncer voyager précipiter témoigner suggérer embarquer loger régner sécher enrichir distribuer essuyer soupçonner compenser dissoudre cueillir progresser caractériser grouper manier absorber maîtriser répartir compromettre basculer circuler déclencher pêcher alimenter épargner instruire apaiser remédier accuser cracher enfiler heurter souper redresser nager ennuyer envahir coudre verger évoluer louer préférer repasser soustraire habituer baigner consentir condamner négocier guetter protester reporter sembler vibrer bondir pendre dissiper moquer rattacher trancher voter priver atténuer déchirer murmurer triompher pourvoir repentir exclure édifier enterrer renseigner parer ordonner déployer diviser frotter gratter raisonner rigoler tailler relire bavarder capter illustrer mériter dérouler émouvoir revêtir dérober étaler abriter fréquenter promettre passager animer approuver blesser célébrer cultiver relier dévorer contester hâter résigner vanter recouvrir critiquer conférer croiser doubler qualifier réciter restaurer résulter promouvoir approfondir gémir attarder bûcher combiner succéder abaisser cogner coordonner imprimer accélérer déshabiller invoquer jurer mouiller ralentir contraindre préoccuper dépenser accumuler déboucher siffler restituer retarder décrocher influencer redouter entamer généraliser balayer perfectionner simplifier épuiser épanouir éclaircir fendre redevenir soulager consommer débarquer décourager engendrer fêter renaître affranchir freiner initier racheter raser solliciter dater errer dépouiller entourer féliciter honorer accommoder énumérer exciter incliner insérer pleuvoir tâcher exploser convertir viser méconnaître redire nouer rallier aménager débrouiller sombrer proclamer ressusciter buter découper masquer menacer mépriser cerner contrarier mater réjouir virer affecter dispenser gouverner renier plaider périr gonfler étrangler expédier fourrer hisser inciter photographier puiser redonner saigner projeter accentuer exagérer lasser méditer sauvegarder insulter choir emplir pourrir rembourser abuser décoller lécher autoriser frémir gravir tisser débattre dépendre cocher compliquer équilibrer emmerder détendre rater plaisanter copier déborder gâcher contredire reconstruire redescendre abîmer évacuer aggraver conformer résonner grossir hausser administrer dissocier effondrer pressentir prévaloir chialer coïncider coûter disputer fusiller gueuler différencier équiper foncer modeler recommander décharger inspecter aligner énoncer instituer tousser violer assigner ébranler émerger gérer planquer référer réprimer retracer tâter contourner démarrer effrayer frayer liquider camper commenter différer semer pater ranimer sursauter anéantir retentir barrer confesser confronter flatter incarner détester regrouper tremper feindre refroidir articuler brouiller doter économiser égarer adhérer trier attendrir tordre ramper recruter pointer apprivoiser assassiner aventurer défier détailler envelopper impressionner engloutir restreindre abolir réconcilier ruiner amorcer corner dériver esquisser incorporer manipuler disperser échouer mélanger replacer rôder ronfler raccrocher applaudir reparaître aspirer bousculer détecter dévoiler excéder financer afficher collaborer meubler pallier tolérer rafraîchir fleurir"
    dico = longAsFStringVerbes.split(' ')
    return dico

def createRandomAdjList():
    longAsFStringAdj = "bleu super autre bizarre difficile drôle étrange facile grave impossible jeune juste libre malade même pauvre possible propre rouge sale simple tranquille triste vide bonne toute doux faux français gros heureux mauvais sérieux vieux vrai ancien beau blanc certain chaud cher clair content dernier désolé différent droit entier fort froid gentil grand haut humain important joli léger long meilleur mort noir nouveau pareil petit plein premier prêt prochain quoi seul tout vert vivant "
    dico = longAsFStringAdj.split(' ')
    return dico

def createRandomWordList():
    longAsFStringWord = "aide chef enfant garde gauche geste gosse livre merci mort ombre part poche professeur tour fois madame paix voix affaire année arme armée attention balle boîte bouche carte cause chambre chance chose classe confiance couleur cour cuisine dame dent droite école église envie épaule époque équipe erreur espèce face façon faim famille faute femme fenêtre fête fille fleur force forme guerre gueule habitude heure histoire idée image impression jambe joie journée langue lettre lèvre ligne lumière main maison maman manière marche merde mère minute musique nuit odeur oreille parole partie peau peine pensée personne peur photo pièce pierre place police porte présence prison putain question raison réponse robe route salle scène seconde sécurité semaine situation soeur soirée sorte suite table terre tête vérité ville voiture avis bois bras choix corps cours gars mois pays prix propos sens temps travers vieux accord agent amour appel arbre argent avenir avion bateau bébé besoin bonheur bonjour bord boulot bout bruit bureau café camp capitaine chat chemin chéri cheval cheveu chien ciel client cœur coin colonel compte copain côté coup courant début départ dieu docteur doigt dollar doute droit effet endroit ennemi escalier esprit état être exemple fait film flic fond français frère front garçon général genre goût gouvernement grand groupe haut homme honneur hôtel instant intérêt intérieur jardin jour journal lieu long maître mari mariage matin médecin mètre milieu million moment monde monsieur mouvement moyen noir nouveau numéro oeil oiseau oncle ordre papa papier parent passage passé patron père petit peuple pied plaisir plan point pouvoir premier présent président prince problème quartier rapport regard reste retard retour rêve revoir salut sang secret seigneur sentiment service seul siècle signe silence soir soldat soleil sourire souvenir sujet téléphone tout train travail trou truc type vent ventre verre village visage voyage fils gens"
    dico = longAsFStringWord.split(' ')
    return dico


def createRandomDeterList():
    longAsFStringWord = "je moi un une tu il nous vous ils de des EPSI Grenoble John_Cena Néo la le les lui La_Dicktatrice"
    dico = longAsFStringWord.split(' ')
    return dico

@bot.command(name = "derekBall", help = "Posez une question a Derekbot et il vous répondra avec toute sa sagesse.")
async def magicDerekBall(ctx,* messageUser: str):
    messageRandom =""
    message = ""
    messageLen = randint(5,25)
    wordList = createRandomWordList()
    adjList = createRandomAdjList()
    deterList = createRandomDeterList()
    verbList = createRandomVerbList()
    for word in messageUser:
        message += word + " "
    messageRandom += deterList[randint(0,len(deterList)-1)] + " "
    for i in range(messageLen-1):
        nextStr = randint(1,5)
        
        if nextStr == 1:
            randomChoice = wordList[randint(0,len(wordList)-1)]
        elif nextStr == 2:
            randomChoice = verbList[randint(0,len(verbList)-1)]
        elif nextStr == 3:
            randomChoice = adjList[randint(0,len(adjList)-1)]
        elif nextStr == 4:
            randomChoice = deterList[randint(0,len(deterList)-1)]
        elif nextStr == 5:
            emoteListUpdate()
            randomChoice = EmoteList[randint(0,len(EmoteList)-1)]
        messageRandom += randomChoice + " "
    await ctx.channel.send("A ton message : \n"+message+"\nje réponds:")
    await ctx.channel.send(messageRandom)



@bot.command(name = "ping")
async def Ping(ctx, user : discord.Member = None):
    user = user or ctx.author
    for i in range(randint(0,10)):
        await ctx.channel.send(user.mention)


@bot.command(name = "spotify")
async def test(ctx, user :discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            await ctx.send(f"{user} est en train d'écouter {activity.title} par {activity.artists}")
        


#Rick Rollette Russe
@bot.command(name = "russe")
async def Roulette(ctx):
    dmChannel = await ctx.author.create_dm()
    i = randint(1,6)
    if i == 6:
        await ctx.message.channel.send(f"Bang.<:Gun:891046373376536627>\nCheck your DM's ")
        await dmChannel.send("||https://www.youtube.com/watch?v=dQw4w9WgXcQ||")
    else:
        await ctx.message.channel.send("You survived another round")








def masterMind(playerNumbers,guessNumbers):
    correction = ['X','X','X','X']
    for i in range(len(playerNumbers)):

        if(int(playerNumbers[i])==guessNumbers[i]):
            correction[i]='O'
        else:
            occurence = 0
            for j in guessNumbers:
                if int(playerNumbers[i])==j:
                    occurence +=1
            if occurence >= 1:
                for j in range(len(guessNumbers)):
                    if int(playerNumbers[i] == guessNumbers[j] and correction[j] == 'O'):
                        occurence-=1
                if occurence>=1:
                    correction[i] = '~'
            
    return correction




#Master Mind again
@bot.command(name = "jeu", help = "Jouez au mastermind avec XavBot, deviner le nombre a 4 chiffre de XavBot et vous avez gagné. difficultés : 1 = Facile | 2 = Normal | 3 = Difficile | 4 = Impossible")
async def jeu(ctx,diff : int):
    if diff == 1:
        vieMax = 15
        vie = 15
        await ctx.message.channel.send("Difficulté facile choisie : nombre de vies = 15")

    elif diff == 2:
        vieMax = 10
        vie = 10
        await ctx.message.channel.send("Difficulté normale choisie : nombre de vies = 10")
    elif diff == 3:
        vieMax = 5
        vie = 5
        await ctx.message.channel.send("Difficulté difficile  choisie : nombre de vies = 5")
    elif diff >=4:
        vie = 1
        await ctx.message.channel.send("Difficulté impossible choisie : nombre de vies = 1")
    user = ctx.author
    a = randint(0,9)
    b = randint(0,9)
    c = randint(0,9)
    d = randint(0,9)
    guessNumbers = [a,b,c,d]
    gameFlag = True
    def check(message):
        try: 
            int(message.content)
            flag = True
        except:
            flag = False
        return message.author == ctx.author and flag
    while gameFlag:
        try:
            await ctx.message.channel.send(f"Nombre de vies : {vie}\nEntrez 4 chiffres : ")
            playerString = await bot.wait_for("message",check=check,timeout=30)
            correction =  masterMind(playerString.content,guessNumbers)
            await ctx.channel.send(correction)
            if correction == ['O','O','O','O']:
                gameFlag = False
                await ctx.message.channel.send(f"GG, nombre de tentatives : {vieMax - vie}")
                randomEmote(ctx)
            elif vie <= 0:
                gameFlag = False
                await ctx.message.channel.send(f"Dommage la réponse était : {guessNumbers}")
            vie -=1  
        except asyncio.TimeoutError:
            await ctx.message.channel.send(f"Temps écoulé")
            gameFlag = False

    
    
EmoteList = []
emoteListUpdate()
bot.run(os.getenv("TOKEN"))