import pygame, cards

class UserInterface:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1040
        self.SCREEN_HEIGHT = 740
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background_color = (54, 57, 62)
        self.card_color = (247,220,180)
        self.font = pygame.font.SysFont("comicsansms", 24)


    def drawCard(self, card: cards.Card, x, y, solution):
        #card constants
        r = 20
        w = 120
        h = 60
        color = (255,255,255)
        word_color = (0,0,0)
        if card.selected or solution:
            if card.type == cards.Type.NEUTRAL:
                color = self.card_color
            elif card.type == cards.Type.BLUE:
                color = (91,138,253)
            elif card.type == cards.Type.RED:
                color = (255,99,92)
            else:
                color = (0,0,0)
                word_color = (255,255,255)
        pygame.draw.rect(self.screen, self.card_color, (x, y + r, w + 2 * r, h))
        pygame.draw.rect(self.screen, self.card_color, (x + r, y, w, h + 2 * r))
        #pygame.draw.rect(self.screen, self.card_color, (x, y, 2, 2))
        pygame.draw.circle(self.screen, self.card_color, (x + r, y + r), r)
        pygame.draw.circle(self.screen, self.card_color, (x + w + r, y + r), r)
        pygame.draw.circle(self.screen, self.card_color, (x + r, y + h + r), r)
        pygame.draw.circle(self.screen, self.card_color, (x + w + r, y + h + r), r)
        pygame.draw.rect(self.screen, color, (x, y + r, w + 2 * r, h))
        text = self.font.render(card.word, True, word_color)
        self.screen.blit(text, (x+r+0.5*w-0.5*text.get_width(), y+r+0.5*h-0.5*text.get_height()))
        return

    def init_board(self, gamestate: cards.Cards, solution):
        for x in range(5):
            for y in range(5):
                card = gamestate.cards[x+5*y]
                self.drawCard(card, 40+x*200,40+140*y, solution)
        return False


    def update_board(self, gamestate, solution = False):
        pygame.event.get()  # used to clear the buffer we will not use these inputs
        self.screen.fill(self.background_color)
        self.init_board(gamestate, solution)
        pygame.display.flip()

    def save_frame(self, location):
        pygame.image.save(self.screen, location)

    def create_solution(self, gamestate):
        self.update_board(gamestate, solution=True)
        pygame.image.save(self.screen, "solution.jpg")