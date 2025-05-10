
import pygame
class Text():
    def __init__(self,screen) -> None:
        self.basic_font = pygame.font.Font('font/a신디나루B.ttf',15)
        self.sub_title = pygame.font.Font('font/a신디나루B.ttf',25)
        self.clock = pygame.font.Font('font/a신디나루B.ttf',100)
        self.waiting = pygame.font.Font('font/a신디나루B.ttf',30)
        self.inf_bar = pygame.font.Font('font/a신디나루B.ttf',27)
        self.team_inf = pygame.font.Font('font/a신디나루B.ttf',30)
        
        self.black_alpah = pygame.Surface((0,0))
        self.black_alpah.set_alpha(100)
            
        self.screen = screen

    def Writing(self,word="nothing",color=(0,0,0),pos=(0,0),type=None,num=False):


        x,y = pos
        if type == None:
            self.text = self.basic_font.render(word,True,color)
            self.screen.blit(self.text,(x,y))
            
        # elif type == 'nametag':
        #     self.text = self.basic_font.render(word,True,color)
        #     self.screen.blit(self.text,((num - self.text.get_size()[0])/2+x,y))

        # elif type == 'clock':
        #     self.text = self.clock.render(word,True,color)
        #     self.screen.blit(self.text,(x,y))
        
        # elif type == 'waiting':
        #     self.text = self.waiting.render(word,True,color)
        #     self.screen.blit(self.text,((num-self.text.get_size()[0])/2+x,y))
        
        # elif type == 'team_inf':
        #     self.text = self.team_inf.render(word,True,color)
        #     self.screen.blit(self.text,(x,y))


        # elif type == 'inf_bar':
        #     self.text = self.inf_bar.render(word,True,color)
        #     self.black_alpah = pygame.transform.scale(self.black_alpah,(self.text.get_size()[0]*1.13,self.text.get_size()[1]*1.13))
        #     self.screen.blit(self.black_alpah,(x,y))
        #     self.screen.blit(self.text,(x,y))

