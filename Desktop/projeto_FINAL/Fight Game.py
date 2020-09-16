import pygame, os, sys #importe de pygame e sys
os.environ["SDL_VIDEO_CENTERED"] = "1" #centralizando janela
from pygame.locals import * #importe de modulos pygame
pygame.init() #iniciando pygame
clock = pygame.time.Clock() #pygame set de clock

#----------------- criando e organizando janela
pygame.display.set_caption("my pygame game") #nome do display
global RESOLUTION #resolucao do game
RESOLUTION = 3
janela = pygame.display.set_mode((256 * RESOLUTION, 224 * RESOLUTION), 0, 32) #iniciando janela

global FLOOR
FLOOR = 130

#----------------- carregar imagens
global IMAGENS_LIST
IMAGENS_LIST = {}

def carregar_img(path, frames):
    global IMAGENS_LIST

    banco_de_frames = []
    img_name = path.split("/")[-1] #nome da imagem
    frame_number = 0 #numero da imagem

    for index1 in frames:
        frame_id = img_name + "_" + str(frame_number) #ex: sprite_0
        frame_path = path + "/" + frame_id + ".png" #ex: path/sprite_0.png
        load_img = pygame.image.load(frame_path).convert()
        load_img.set_colorkey((130, 174, 200))
        load_img = pygame.transform.scale(load_img, (load_img.get_width() * RESOLUTION, load_img.get_height() * RESOLUTION))
        IMAGENS_LIST[frame_id] = load_img.copy()
    
        for index2 in range(index1):
            banco_de_frames.append(frame_id)

        frame_number += 1

    return banco_de_frames
    
#carrendo imagens
banco_de_imagens = {}
imagens_origin = {}

banco_de_imagens["c1_esp_pose"] = carregar_img("resoucers/player_animations/c1_esp_pose", [14, 14, 14])
imagens_origin["c1_esp_pose"] = [(0, 0 ), (0, 0), (0, 0)]
banco_de_imagens["c1_andarDir"] = carregar_img("resoucers/player_animations/c1_andarDir", [14, 14, 14])
imagens_origin["c1_andarDir"] = [(0, -2), (0, -2), (0, -2)]
banco_de_imagens["c1_andarEsq"] = carregar_img("resoucers/player_animations/c1_andarEsq", [14, 14, 14])
imagens_origin["c1_andarEsq"] = [(0, -2), (0, -2), (0, -2)]
banco_de_imagens["c1_chargeOff"] = carregar_img("resoucers/player_animations/c1_chargeOff", [1])
imagens_origin["c1_chargeOff"] = [(0, 1)]
banco_de_imagens["c1_dashDir"] = carregar_img("resoucers/player_animations/c1_dashDir", [1])
imagens_origin["c1_dashDir"] = [(0, 2)]
banco_de_imagens["c1_dashEsq"] = carregar_img("resoucers/player_animations/c1_dashEsq", [1])
imagens_origin["c1_dashEsq"] = [(-2, 1)]
banco_de_imagens["c1_defesa"] = carregar_img("resoucers/player_animations/c1_defesa", [1])
imagens_origin["c1_defesa"] = [(-1, 1)]
banco_de_imagens["c1_jump"] = carregar_img("resoucers/player_animations/c1_jump", [1])
imagens_origin["c1_jump"] = [(0, -2)]
banco_de_imagens["c1_jumpDown"] = carregar_img("resoucers/player_animations/c1_jumpDown", [8, 8, 8])
imagens_origin["c1_jumpDown"] = [(-4, -2), (-4, -2), (-4, -2)]

banco_de_imagens["sombra"] = carregar_img("resoucers/miscellaneous/sombra", [1])
imagens_origin["sombra"] = [(-1, 39)]
imagens_origin["sombra_c1_chargeOff"] = [(0, 39)]
imagens_origin["sombra_c1_defesa"] = [(-2, 39)]

banco_de_imagens["dash"] = carregar_img("resoucers/miscellaneous/dash", [5, 5, 5])
imagens_origin["dash"] = [(0, 0), (0, 0), (0, 0)]

banco_de_imagens["HUD_main"] = carregar_img("resoucers/miscellaneous/HUD_main", [1])
imagens_origin["HUD_main"] = [(0, 0)]

#----------------- HUD
class HUD:
    def __init__(self):
        self.animation_name = "HUD_main"
        self.frame = 0

    def draw(self, janela, x, y):
        IMAGENS_LIST

        self.frame += 1
        if self.frame >= len(banco_de_imagens[self.animation_name]):
            self.frame = 0
        
        #origen
        origin_frame = banco_de_imagens[self.animation_name][self.frame].split("_")[-1]
        x += imagens_origin[self.animation_name][int(origin_frame)][0] * RESOLUTION
        y += imagens_origin[self.animation_name][int(origin_frame)][1] * RESOLUTION

        render = IMAGENS_LIST[banco_de_imagens[self.animation_name][self.frame]]
        janela.blit(render, (round(x), round(y)))
        
obj_hud_main = HUD()

#----------------- fighter
class Fighter:
    def __init__(self, x, y, animation_name):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.speed = 1 * RESOLUTION
        self.animation_name = animation_name
        self.frame = 0
        self.animation_roll = True
        self.shadown = "sombra"
        self.shadown_origin = "sombra"
        self.shadown_w = 0
        self.shadown_h = 0
        self.trigger = 0
        self.in_trigger = "off"
        self.estado = "pose"
        self.old_c = (80, 120, 248)
        self.new_c = (80, 120, 248)
        self.step_time = 0
        self.grav = 0.4 * RESOLUTION
        self.dash_effect_list = []

    def draw(self, janela, x, y):
        IMAGENS_LIST

        if self.animation_roll == True:
            self.frame += 1
            if self.frame >= len(banco_de_imagens[self.animation_name]) and self.animation_name != "c1_jumpDown":
                self.frame = 0

        #fighter origen
        origin_frame = banco_de_imagens[self.animation_name][self.frame].split("_")[-1]
        x += imagens_origin[self.animation_name][int(origin_frame)][0] * RESOLUTION
        y += imagens_origin[self.animation_name][int(origin_frame)][1] * RESOLUTION

        render = self.mudar_cor(IMAGENS_LIST[banco_de_imagens[self.animation_name][self.frame]], self.new_c, self.old_c)
        render.set_colorkey((130, 174, 200))
        janela.blit(render, (round(x), round(y)))

        self.x += self.hspeed

        self.vspeed += self.grav
        if (self.y + self.vspeed) >= FLOOR * RESOLUTION:
            self.vspeed = 0
            self.y = FLOOR * RESOLUTION
            if self.estado == "jump" or self.estado == "impulse":
                self.acao("pose")
        else:
            self.y += self.vspeed

        #draw dash effect
        for obj_dash_effect in self.dash_effect_list:
            obj_dash_effect.draw(janela)

    def mudar_cor(self, render, new_c, old_c):

        image_copy = pygame.Surface(render.get_size())
        image_copy.fill(new_c)
        render.set_colorkey(old_c)
        image_copy.blit(render, (0, 0))

        return image_copy

    def draw_shadown(self, janela, x, y):
        IMAGENS_LIST

        #shadown origen
        origin_frame = banco_de_imagens[self.shadown][0].split("_")[-1]
        x += imagens_origin[self.shadown_origin][int(origin_frame)][0] * RESOLUTION - int(self.shadown_w/2)
        y += imagens_origin[self.shadown_origin][int(origin_frame)][1] * RESOLUTION - int(self.shadown_h/2)

        render = IMAGENS_LIST[banco_de_imagens[self.shadown][0]]
        render = pygame.transform.scale(render, (render.get_width() + self.shadown_w, render.get_height() + self.shadown_h))
        janela.blit(render, (x, y))

    def create_dash_effect(self, create, x, flip):
        obj_dash_effect = Dash_effect(x, flip)
        if create == 1:
            self.dash_effect_list.append(obj_dash_effect)
        if create == 0:
            self.dash_effect_list.pop(0)

    def change_animation(self, new_a):
        if self.animation_name != new_a:
            self.animation_name = new_a
            self.frame = 0
        return self.animation_name, self.frame

    def acao(self, acao = "pose", impulse = 0):
        if acao == "pose":
            self.estado = "pose"
            self.hspeed = 0
            self.change_animation("c1_esp_pose")
            self.shadown_origin = "sombra"
            self.new_c = (80, 120, 248)
            self.shadown_w = 0
            self.shadown_h = 0
        if acao == "andarDir":
            self.hspeed = self.speed
            if self.animation_name != "c1_jump" and self.animation_name != "c1_jumpDown":
                self.change_animation("c1_andarDir")
            self.shadown_origin = "sombra"
        if acao == "andarEsq":
            self.hspeed = -self.speed
            if self.animation_name != "c1_jump" and self.animation_name != "c1_jumpDown":
                self.change_animation("c1_andarEsq")
            self.shadown_origin = "sombra"
        if acao == "chargeOff":
            self.estado = "pose"
            self.hspeed = 0
            self.change_animation("c1_chargeOff")
            self.shadown_origin = "sombra_c1_chargeOff"
        if acao == "dashDir":
            self.estado = "dash"
            self.hspeed = 3 * RESOLUTION
            self.change_animation("c1_dashDir")
            self.shadown_origin = "sombra"
        if acao == "dashEsq":
            self.estado = "dash"
            self.hspeed = -3 * RESOLUTION
            self.change_animation("c1_dashEsq")
            self.shadown_origin = "sombra"
        if acao == "defesa_especial":
            self.estado = "defesa_especial"
            self.hspeed = 0
            self.change_animation("c1_defesa")
            self.shadown_origin = "sombra_c1_defesa"
        if acao == "jump":
            self.estado = "jump"
            if impulse != 0:
                self.hspeed = impulse * RESOLUTION
                self.estado = "impulse"
            self.vspeed = -6 * RESOLUTION
            self.change_animation("c1_jump")
            self.shadown_origin = "sombra"
        if acao == "jumpDown":
            self.change_animation("c1_jumpDown")
            self.shadown_origin = "sombra"

obj_p1 = Fighter(20 * RESOLUTION, FLOOR * RESOLUTION, "c1_esp_pose") #obj_p1

#----------------- classe de dash
class Dash_effect:
    def __init__(self, x, flip):
        self.x = x
        self.y = (FLOOR + 38) * RESOLUTION
        self.animation_name = "dash"
        self.frame = 0
        self.origin = "dash"
        self.flip = flip
        self.create = 1
        
    def draw(self, janela):
        IMAGENS_LIST

        self.frame += 1
        if self.frame >= len(banco_de_imagens[self.animation_name]):
            self.frame = 0
            self.create = 0
            obj_p1.create_dash_effect(0, 0, False)

        if self.create == 1:
            render = IMAGENS_LIST[banco_de_imagens[self.animation_name][self.frame]]
            janela.blit(pygame.transform.flip(render, self.flip, False), (self.x, self.y))

#----------------- classe de armas
#class weapons:
            
#----------------- main
def main():
    run = True
    FPS = 60

    clock = pygame.time.Clock()
    
    def redraw_window():
        janela.fill((0, 0, 0)) #fundo preto
        obj_hud_main.draw(janela, 0, 0)
        obj_p1.draw_shadown(janela, obj_p1.x, FLOOR * RESOLUTION)
        obj_p1.draw(janela, obj_p1.x, obj_p1.y)
        
        pygame.display.update()
    
    #loop do jogo
    while run:
        clock.tick(FPS) #velocidade do clock
        redraw_window()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r: #restart
                    obj_p1.x = 20 * RESOLUTION
                    obj_p1.y = FLOOR * RESOLUTION
                    obj_p1.hspeed = 0
                    obj_p1.vspeed = 0
                    obj_p1.estado = "pose"
                    obj_p1.acao("pose")
                    obj_p1.trigger = 0
                    obj_p1.in_trigger = "off"

                if event.key == K_RIGHT and obj_p1.estado == "pose":
                    if obj_p1.in_trigger == "off" and obj_p1.trigger == 0:
                        obj_p1.in_trigger = "dashDir"
                        obj_p1.trigger = 0.1
                    elif obj_p1.trigger > 0 and obj_p1.in_trigger == "dashDir":
                        obj_p1.acao("dashDir")
                        obj_p1.trigger = 0

                        obj_p1.create_dash_effect(1, obj_p1.x - (3 * RESOLUTION), False) #create dash effect

                    elif obj_p1.in_trigger != "off":
                        obj_p1.in_trigger = "off"                  

                if event.key == K_LEFT and obj_p1.estado == "pose":
                    if obj_p1.in_trigger == "off" and obj_p1.trigger == 0:
                        obj_p1.in_trigger = "dashEsq"
                        obj_p1.trigger = 0.1
                    elif obj_p1.trigger > 0 and obj_p1.in_trigger == "dashEsq":
                        obj_p1.acao("dashEsq")
                        obj_p1.trigger = 0

                        obj_p1.create_dash_effect(1, obj_p1.x + (28 * RESOLUTION), True) #create dash effect
                        
                    elif obj_p1.in_trigger != "off":
                        obj_p1.in_trigger = "off"

                if event.key == K_UP and obj_p1.estado == "pose":
                    if obj_p1.in_trigger == "off" and obj_p1.trigger == 0:
                        obj_p1.in_trigger = "defesa_especial"
                        obj_p1.trigger = 0.1
                    elif obj_p1.trigger > 0 and obj_p1.in_trigger == "defesa_especial":
                        obj_p1.acao("defesa_especial")
                        obj_p1.trigger = 0
                    elif obj_p1.in_trigger != "off":
                        obj_p1.in_trigger = "off"

                if event.key == K_z and obj_p1.estado != "jump":
                    if obj_p1.estado == "dash" and obj_p1.hspeed > 0:
                        obj_p1.acao("jump", 2)
                    elif obj_p1.estado == "dash" and obj_p1.hspeed < 0:
                        obj_p1.acao("jump", -2)
                    elif obj_p1.estado == "pose":
                        obj_p1.acao("jump")

        keys = pygame.key.get_pressed()
        if obj_p1.estado == "pose" or obj_p1.estado == "jump":
            if keys[pygame.K_RIGHT]:
                obj_p1.acao("andarDir")
            if keys[pygame.K_LEFT]:
                obj_p1.acao("andarEsq")
        if obj_p1.estado == "pose":
            if not keys[K_RIGHT] and not keys[K_LEFT]:
                obj_p1.acao("pose")
            if keys[pygame.K_DOWN]:
                obj_p1.acao("chargeOff")

        if obj_p1.estado == "jump" or obj_p1.estado == "impulse":
            if obj_p1.vspeed >= 0:
                obj_p1.acao("jumpDown")
                obj_p1.shadown_w += 1 * RESOLUTION
            else:
                obj_p1.shadown_w -= 1 * RESOLUTION

        if obj_p1.trigger > 0 and obj_p1.estado == "pose":
            obj_p1.trigger += 0.1
            if obj_p1.trigger >= 1.5:
                obj_p1.trigger = 0
                obj_p1.in_trigger = "off"

        if obj_p1.estado == "dash":
            obj_p1.trigger += 0.1
            if obj_p1.trigger >= 1:                
                obj_p1.acao("pose")

        if obj_p1.estado == "defesa_especial":
            obj_p1.trigger += 0.1
            obj_p1.step_time += 0.1
            if obj_p1.step_time < 0.5:
                obj_p1.new_c = (176, 192, 248)
            if obj_p1.step_time > 0.5:
                obj_p1.new_c = (80, 120, 248)
                if obj_p1.step_time > 1:
                    obj_p1.step_time = 0
            if obj_p1.trigger >= 4:
                obj_p1.step_time = 0
                obj_p1.acao("pose")
            
main()
    
