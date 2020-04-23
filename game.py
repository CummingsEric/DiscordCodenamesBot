import cards
import discord
import UI

class Game:
    def __init__(self, set):
        self.UI = UI.UserInterface()
        self.image_location = 'screenshot.jpg'
        self.gameState = cards.Cards(set)
        self.currentTeam = cards.Type.BLUE
        self.guessedWords = []
        self.correctBlue = 9
        self.correctRed = 8
        self.gameStarted = False
        self.teams_dict = {}
        self.spymasters = []
        self.num_players = 100
        self.roundStarted = False
        self.channel = None
        self.guesses = 100

    def reset(self, set):
        self.UI = UI.UserInterface()
        self.gameState = cards.Cards(set)
        self.currentTeam = cards.Type.BLUE
        self.guessedWords = []
        self.correctBlue = 9
        self.correctRed = 8
        self.gameStarted = False
        self.teams_dict = {}
        self.spymasters = []
        self.num_players = 100
        self.roundStarted = False
        self.channel = None
        self.guesses = 100

    # all functions are to manipulate the cards
    def process(self, guess, team):
        # check the team
        if (team != self.currentTeam):
            return (False, "Wrong Team", None, None)
        else:
            if (guess == "EndRound"):
                return (True, "EndRound", None, None)
            # check if the word is in the cards
            if (guess in self.gameState.words and not guess in self.guessedWords):
                # update the guessed word and set the current team to the correct one
                cardID = self.gameState.wordstoID[guess]
                card = self.gameState.cards[cardID]
                card.selected = True
                self.guessedWords.append(guess)
                return (True, "Valid Play", (card.type == self.currentTeam), card.type == cards.Type.ASSASSIN)
            else:
                return (False, "Word does not exist or has already been guessed", None, None)

    def round(self):
        guesses = self.getNumberGuesses()
        while (guesses > -1):
            guess = self.getGuess()
            processReport = self.process(guess[0], guess[1])
            if (processReport[0] == True):
                # redraw and reset
                guesses -= 1
                # check for an assassin guess
                if (processReport[3]):
                    if (self.currentTeam == cards.Type.BLUE):
                        self.currentTeam = cards.Type.RED
                    else:
                        self.currentTeam = cards.Type.BLUE
                    return (False)
                # check for a bad guess
                if (not processReport[2]):
                    break
                # check to see if a team has won
                else:
                    # need to reduce the correct teams score
                    if (self.currentTeam == cards.Type.BLUE):
                        self.correctBlue -= 1
                        if (self.correctBlue == 0):
                            return (False)
                    else:
                        self.correctRed -= 1
                        if (self.correctRed == 0):
                            return (False)
        # swap the current team that is playing
        if (self.currentTeam == cards.Type.BLUE):
            self.currentTeam = cards.Type.RED
        else:
            self.currentTeam = cards.Type.BLUE
        return (True)

    def getGuess(self):
        value = str(input("Word to guess for team " + str(self.currentTeam.name) + ":\n"))
        return (value, self.currentTeam)

    def getNumberGuesses(self):
        value = int(input("number of guesses for team " + str(self.currentTeam.name) + ":\n"))
        return value

    def gameStart(self):
        while (self.round()):
            continue
        print(str(self.currentTeam.name) + " wins the game")

    def switch_teams(self):
        if (self.currentTeam == cards.Type.BLUE):
            self.currentTeam = cards.Type.RED
        else:
            self.currentTeam = cards.Type.BLUE


# here is all the discord stuff
client = discord.Client()
counter_array = []
game = Game('Dirty')
print(game.gameState.solution())
#game.gameStart()

@client.event
async def on_message(message):
    message.content.lower()
    if message.author == client.user:
        return None
    if "test" in message.content and message.author.name == 'EE-Rak':
        game.reset('Dirty')
        print(game.gameState.solution())
        game.channel = message.channel
        await clear_channel()
        gamestart = await message.channel.send(
            "Starting Codenames...\nPlease select a team to join by clicking the appropriate reaction\nIf you are the teams spymaster, please select the detective")
        emojis = ['\U0001F535', '\U0001F534', '\U0001F575']
        await gamestart.add_reaction(emojis[0])
        await gamestart.add_reaction(emojis[1])
        await gamestart.add_reaction(emojis[2])
        game.num_players = int(message.content.split('-p=')[1])

    elif message.content == 'clear' and message.author.name == 'EE-Rak':
        game.channel = message.channel
        await clear_channel()

    else:
        if(game.gameStarted):
            print("need to proccess guess")



            if(game.roundStarted):
                print("processing")
                processReport = game.process(message.content, game.teams_dict[message.author.name])
                print(processReport, game.teams_dict[message.author.name])


                if (processReport[0] == True):
                    game.guesses -= 1
                    if(processReport[1] == 'EndRound' or game.guesses == -1):
                        game.switch_teams()
                        game.roundStarted = False
                        await clear_channel()
                        await send_game_state()
                        await prompt_for_spymaster()
                        return
                    # redraw and reset

                    # check for an assassin guess
                    if (processReport[3]):
                        #set the correct team to win
                        game.switch_teams()
                        await end_game()
                        return
                    # check for a bad guess
                    if (not processReport[2]):
                        game.switch_teams()
                        game.roundStarted = False
                        await clear_channel()
                        await send_game_state()
                        await prompt_for_spymaster()
                        return
                        #team needs to change
                    # check to see if a team has won
                    else:
                        # need to reduce the correct teams score
                        if (game.currentTeam == cards.Type.BLUE):
                            game.correctBlue -= 1
                            if (game.correctBlue == 0):
                                await end_game()
                                return
                        else:
                            game.correctRed -= 1
                            if (game.correctRed == 0):
                                await end_game()
                                return
                        await clear_channel()
                        await send_game_state()
                        await game.channel.send("Correct! " + game.currentTeam.name + " team still has (" + str(game.guesses) + ") guesses left. Type \'EndRound\' to end guessing")
                else:
                    await message.channel.delete_messages([message])


                #need to makes checks based on the processed request
            else:
                if(message.author in game.spymasters and game.teams_dict[message.author.name] == game.currentTeam):
                    try:
                        game.guesses = int(message.content)
                        game.roundStarted = True
                        print("guesses set")
                    except:
                        print("the number entered by the spymaster was not a recognizable number")

                else:
                    print("please wait for spymaster to start round")
                    await message.channel.delete_messages([message])
        else:
            print("invalid input")
            await message.channel.delete_messages([message])

@client.event
async def on_reaction_add(reaction, user):
    if(user == client.user):
        return
    if (reaction.emoji == '🔵'):
        game.teams_dict[str(user).split('#')[0]] = cards.Type.BLUE
    if (reaction.emoji == '🔴'):
        game.teams_dict[str(user).split('#')[0]] = cards.Type.RED
    if (reaction.emoji == '🕵'):
        game.spymasters.append(user)
    if(len(game.teams_dict) >= game.num_players and len(game.spymasters) == 1 and not game.gameStarted):
        game.gameStarted = True
        await reaction.message.channel.send("Required number of players have selected teams... starting game")
        await send_game_state()
        game.UI.create_solution(game.gameState)
        for spymaster in game.spymasters:
            await send_dm(spymaster,"You are the spymaster of the " + game.teams_dict[str(spymaster).split('#')[0]].name + " team")
            await send_image_dm(spymaster, "solution.jpg")
        await prompt_for_spymaster()

async def send_dm(member: discord.Member, content):
    dmchannel = await member.create_dm()
    await dmchannel.send(content)

async def send_image_dm(member: discord.Member, content):
    dmchannel = await member.create_dm()
    await dmchannel.send(file=discord.File(content))

async def prompt_for_spymaster():
    await game.channel.send("The spymaster for the "+game.currentTeam.name+" team needs to give a hint and enter the number of guesses")

async def clear_channel():
    # get messages to delete
    messages = await game.channel.history(oldest_first=True).flatten()

    # delete messages
    await game.channel.delete_messages(messages)

async def end_game():
    await clear_channel()
    await send_game_state()
    await game.channel.send("The " + game.currentTeam.name + " has won the game!")
    await game.channel.send("Here is the solution")
    await send_image('solution.jpg')

async def send_game_state():
    game.UI.update_board(game.gameState)
    game.UI.save_frame('screenshot.jpg')
    await game.channel.send(file=discord.File('screenshot.jpg'))

async def send_image(image):
    await game.channel.send(file=discord.File(image))

client.run('')
