# Program name: project2.py
# Developer: Blake Konkolesky (ITCS 1950 MW)
# Date: 15.11.16
# Description: Pong with a level framework based on points scored and 2 players

# Player 1 controls: W = up, S = down
# Player 2 controls: Up Arrow = up, Down Arrow = down
# Player 3 controls: 7 = left, 8 = right
# Player 4 controls: B = left, N = right

import pygame, random, sys

BG_COLOR = (0, 0, 0) 
SCR_WID, SCR_HEI = 590, 590
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))

class Player():
        def __init__(self, properties, level):  
                self.properties = properties
                self.level = level
                self.x, self.y = 16, SCR_HEI/2
                self.speed = 7
                self.score_font = pygame.font.Font("imagine_font.ttf", 64)
                self.side = properties["side"]

                if level < 5:
                        self.score = 0
                
                if self.side == "left":
                        self.x = properties["offset"]
                        if level < 5:
                                self.pad_wid, self.pad_hei = 8, 64        
                        else:
                                self.pad_wid, self.pad_hei = 8, 48
                        
                elif self.side == "right":
                        if level < 5:
                                self.pad_wid, self.pad_hei = 8, 64        
                        else:
                                self.pad_wid, self.pad_hei = 8, 48
                        self.x = SCR_WID - (self.pad_wid + self.properties["offset"])
                
        def scoring(self, scores):
                score_blit = self.score_font.render(str(self.score), 1, (255, 255, 255))
                if self.side == "left":
                        scores[0] = self.score
                        screen.blit(score_blit, (self.properties["offset"], 16))

                elif self.side == "right":
                        scores[1] = self.score
                        screen.blit(score_blit, (SCR_WID - (score_blit.get_width() + self.properties["offset"]), SCR_HEI - (score_blit.get_height() + 16))) 
                        
                if self.score == 12:
                        print("The winner is %s!" % (self.properties["name"]))
                        pygame.quit()
                        sys.exit()
                return scores
       
        def movement(self):
                keys = pygame.key.get_pressed()
                if self.properties["name"] == "player 1" or self.properties["name"] == "player 2":
                        if keys[self.properties["key_up"]]:
                                self.y -= self.speed
                        elif keys[self.properties["key_down"]]:
                                self.y += self.speed
               
                        if self.y <= 0:
                                self.y = 0
                        elif self.y >= SCR_HEI - self.pad_hei:
                                self.y = SCR_HEI - self.pad_hei
                        
       
        def draw(self):
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.pad_wid, self.pad_hei))

class Ball():
        def __init__(self, players, speed, level):
                self.x, self.y = SCR_WID/2, SCR_HEI/2
                self.speed = speed
                self.speed_x = -self.speed
                self.speed_y = self.speed
                self.size = 8
                self.players = players
                self.level = level
                      
        def movement(self):
                self.x += self.speed_x
                self.y += self.speed_y
 
                #wall col
                if self.x <= 0:
                        self.reset()
                        for player in self.players:
                                if player.side == "right":
                                        player.score += 1
                        
                if self.x >= SCR_WID - self.size:
                        self.reset()
                        self.speed_x = self.speed
                        for player in self.players:
                                if player.side == "left":
                                        player.score += 1
                
                if self.y <= 0:
                        self.speed_y *= -1
                                        
                elif self.y >= SCR_HEI - self.size:
                        self.speed_y *= -1
                        self.speed_x = self.speed

                #paddle col
                for player in self.players:
                        if player.side == "left":
                                for n in range(-self.size, player.pad_hei):
                                        if self.y == player.y + n:
                                                if self.x <= player.x + player.pad_wid:
                                                        self.speed_x *= -1
                                                        break
                                        n += 1

                        elif player.side == "right":
                                for n in range(-self.size, player.pad_hei):
                                        if self.y == player.y + n:
                                                if self.x >= player.x - player.pad_wid:
                                                        self.speed_x *= -1
                                                        break
                                        n += 1


        def reset(self):
                if self.level < 3:
                        self.x, self.y = SCR_WID/2, SCR_HEI/2
                else:
                        self.x, self.y = random.randint((SCR_WID/2) - 100, (SCR_WID/2) + 100), random.randint((SCR_HEI/2) - 100, (SCR_HEI/2) + 100)
                self.speed_x = -self.speed
                self.speed_y = self.speed
                
        def draw(self):
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 8, 8)) 

def levelUp(level, ball, balls, ball_speed, players, property_list):
        # Level 2: Ball speed increases
        if level == 2:
                bg_color = (128, 0, 128)
                ball_speed = 5

        # Level 3: Random ball respawn point                
        if level == 3:
                bg_color = (0, 0, 128)

        # Level 4: Second ball added       
        if level == 4:
                bg_color = (0, 128, 0) 
                second_ball = Ball(players, ball_speed, level)
                balls.append(second_ball)
                ball_speed = 4 

        # Level 5: Smaller paddles
        if level == 5:
                bg_color = (255, 140, 0)
                index = 0
                for player in players:
                        player.__init__(property_list[index], level)
                        index += 1

        # Level 6: Third ball added
        if level == 6:
                bg_color = (128, 0, 0)
                third_ball = Ball(players, ball_speed, level)
                balls.append(third_ball)
                ball_speed = 3

        if level >= 2:
                for ball in balls:
                        ball.__init__(players, ball_speed, level)

        if level >= 4:
                for ball in balls:
                        ball.reset()

        return level, bg_color, balls

##def levelDisplay(level):
##        level_text = ""
##        level_font = pygame.font.Font("imagine_font.ttf", 24)
##        level_blit = level_font.render(level_text, 1, (255, 255, 255))
##        if level == 1:
##                level_text = "LEVEL ONE"
##                screen.blit(level_blit, ((SCR_WID/2) - 30, (SCR_HEI/2) - 10)) 
##                
                
                                                
def main():
        
        pygame.display.set_caption("Pong")
        pygame.font.init()
        clock = pygame.time.Clock()
        FPS = 60
        level = 1
        next_level_score = 1
        ball_speed = 4
        scores = ["","","",""]
        bg_color = (0, 0, 0)
        
        player_one_properties = {"name" : "player 1", "side" : "left", "offset" : 32, "key_up" : pygame.K_w, "key_down" : pygame.K_s}
        player_two_properties = {"name" : "player 2", "side" : "right", "offset" : 32, "key_down" : pygame.K_DOWN, "key_up" : pygame.K_UP}
        property_list = [player_one_properties, player_two_properties]
                                                 
        player_one = Player(player_one_properties, level)
        player_two = Player(player_two_properties, level)
        players = [player_one, player_two] 
        first_ball = Ball(players, ball_speed, level)
        balls = []
        balls.append(first_ball)
                 
        while True:
                for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                       print ("Game exited by user")
                                       pygame.quit()
                                       sys.exit()

##                levelDisplay(level) 
                
                for player in players:
                        player.movement()

                for ball in balls:
                        ball.movement()
                
                screen.fill(bg_color)

                for ball in balls:
                        ball.draw()
                
                for player in players:
                        player.draw()  
                
                for player in players:
                        scores = player.scoring(scores)
                        if level < 6:
                                if next_level_score in scores:
                                        level += 1
                                        next_level_score += 2
                                        level, bg_color, balls = levelUp(level, ball, balls, ball_speed, players, property_list)
                                        break

                pygame.display.flip()
                clock.tick(FPS)

main()

