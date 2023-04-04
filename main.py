# Inicio de exemplo extraido da: https://www.pygame.org/docs/ref/joystick.html

# Nome projeto: Controle-De-Games
# Data: [08/03/2023]
# Projeto Iniciado: [23/02/2023]
# Desenvolvido por:
#
# [AthenasArch].
# [Leonardo Hilgemberg Lopes].
import math
import pygame

# Cores básicas em tuplas RGB
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CIANO = (0, 255, 255)
MAGENTA = (255, 0, 255)
CINZA = (128, 128, 128)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (64, 64, 64)
LARANJA = (255, 165, 0)
ROSA = (255, 105, 180)
MARROM = (139, 69, 19)



# Classe TextPrint que será usada para exibir informações na tela
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25) # Configura a fonte a ser usada para exibir o texto
        self.text_color = (255, 255, 255) # Define a cor do texto como branco

    def tprint(self, screen, text):
        # Renderiza o texto na tela
        text_bitmap = self.font.render(text, True, self.text_color)
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        # Reinicia as posições x e y e a altura da linha de texto
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        # Aumenta o valor de x para criar uma indentação
        self.x += 10

    def unindent(self):
        # Diminui o valor de x para remover a indentação
        self.x -= 10


def handle_analog_axes(joystick, text_print, screen):

    # Obtém o número de eixos do joystick
    axes = joystick.get_numaxes()
    text_print.tprint(screen, f"Número de eixos: {axes}")
    text_print.indent()

    # Exibe o valor atual de cada eixo
    for i in range(axes):
        axis = joystick.get_axis(i)
        text_print.tprint(screen, f"Eixo {i} valor: {axis:>6.3f}")
    
    text_print.unindent()


def draw_analog_stick(joystick, axis_x, axis_y, x, y, width, height, screen):
    # Converte os valores analógicos para coordenadas no plano cartesiano
    xpos = int((joystick.get_axis(axis_x) + 1) * width / 2 + x)
    ypos = int((-joystick.get_axis(axis_y) + 1) * height / 2 + y)

    # Desenha o plano cartesiano como um retângulo
    pygame.draw.rect(screen, PRETO, (x, y, width, height), 2)

    # Desenha uma linha do centro do plano até a posição da bolinha
    center_x = x + width // 2
    center_y = y + height // 2
    border_line = 3
    pygame.draw.line(screen, AMARELO, (center_x, center_y), (xpos, ypos), border_line)

    # Desenha a bolinha na posição atual
    pygame.draw.circle(screen, VERMELHO, (xpos, ypos), 10)

# Aqui vamos desenhar os analogicos dos gatilhos quando tiver...
# def draw_trigger_meter(trigger_value, x, y, width, height, screen):
#     # Desenha o retângulo de fundo do velocímetro
#     pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))

#     # Calcula o ângulo do ponteiro com base no valor do gatilho
#     angle = math.pi * (1 - trigger_value)

#     # Calcula a posição do ponteiro
#     pointer_length = (height - 10) // 2
#     pointer_x = x + width // 2 + int(math.cos(angle) * pointer_length)
#     pointer_y = y + height - 10 - int(math.sin(angle) * pointer_length)

#     # Desenha o ponteiro
#     pygame.draw.line(screen, (0, 0, 0), (x + width // 2, y + height - 10), (pointer_x, pointer_y), 3)

#     # Desenha um pequeno círculo no centro do velocímetro
#     pygame.draw.circle(screen, (0, 0, 0), (x + width // 2, y + height - 10), 5)

def draw_trigger_velocity(trigger_value, x, y, screen):
    radius = 50
    angle = 180 * (1 - (trigger_value + 1) / 2)

    # Desenha o arco base do velocímetro
    pygame.draw.arc(screen, (0, 0, 0), (x, y, 2 * radius, 2 * radius), math.radians(180), math.radians(360), 2)

    # Calcula as coordenadas da ponta da seta
    end_x = x + radius + radius * math.cos(math.radians(angle))
    end_y = y + radius + radius * math.sin(math.radians(angle))

    # Desenha a seta do velocímetro
    pygame.draw.line(screen, (0, 0, 255), (x + radius, y + radius), (end_x, end_y), 2)


# aqui tratamos os triggers dos gatilhos dos novos controles
def handle_triggers(joystick, text_print, screen):
    # Verifique se o joystick tem pelo menos 6 eixos analógicos
    if joystick.get_numaxes() < 6:
        # Se o joystick não tiver pelo menos 6 eixos, ele provavelmente não tem gatilhos analógicos
        text_print.tprint(screen, f"Este joystick não possui gatilhos analógicos.")
        return

    trigger_left = joystick.get_axis(4)
    trigger_right = joystick.get_axis(5)

    text_print.tprint(screen, f"Gatilho esquerdo: {trigger_left:>6.3f}")
    text_print.tprint(screen, f"Gatilho direito: {trigger_right:>6.3f}")

    trigger_x = 550
    trigger_y = 300
    draw_trigger_velocity(trigger_left, trigger_x, trigger_y, screen)
    draw_trigger_velocity(trigger_right, trigger_x + 250, trigger_y, screen)



# trata os botoes
def handle_buttons(joystick, text_print, screen):

    # Obtém o número de botões do joystick
    buttons = joystick.get_numbuttons()
    text_print.tprint(screen, f"Número de botões: {buttons}")

    # Exibe o estado de cada botão
    for i in range(buttons):
        button = joystick.get_button(i)
        text_print.tprint(screen, f"Botão {i:>2} valor: {button}")
    text_print.unindent()

def draw_checkboxes(joystick, x, y, width, height, screen):
    # Obtém o número de botões do joystick
    buttons = joystick.get_numbuttons()

    # Desenha as checkboxes e atualiza o estado de acordo com o valor do botão
    for i in range(buttons):
        button_value = joystick.get_button(i)
        draw_checkbox(button_value, x + i * 30, y, width, height, screen)

def draw_checkbox(button_value, x, y, width, height, screen):
    # Desenha o retângulo da checkbox
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)

    # Se o botão estiver pressionado, desenha um retângulo preenchido dentro da checkbox
    if button_value:
        pygame.draw.rect(screen, (0, 0, 0), (x + 4, y + 4, width - 8, height - 8))



def handle_hats(joystick, text_print, screen):

    # Obtém o número de chapeus (hat) do joystick
    hats = joystick.get_numhats()
    text_print.tprint(screen, f"Número de chapeus: {hats}")
    text_print.indent()

    # Exibe a posição atual de cada chapéu
    for i in range(hats):
        hat = joystick.get_hat(i)
        text_print.tprint(screen, f"Chapéu {i} valor: {str(hat)}")
    text_print.unindent()

# trata a inicializacao da pygame e retorna a tela
def init_pygame():
    pygame.init() # Inicializa a biblioteca Pygame
    size = (1100, 700)  # Aumente a largura da tela para acomodar a caixa de texto
    # Configura o tamanho da tela (largura, altura) e o nome da janela
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Teste do Joystick")
    return screen

# carrega e dimensiona a logo
def load_resources():
    logo = pygame.image.load("logo.png")
    logo_width = 400
    logo_height = 100
    logo = pygame.transform.scale(logo, (logo_width, logo_height))

    return {"logo": logo}

# desenha a interface de texto do usuario.
def draw_ui(screen, logo):
    # Preencha o fundo com a cor preta
    screen.fill((0, 0, 0))

    # Desenha a logo e as cordenadas dela
    logo_x = 10
    logo_y = 500 
    screen.blit(logo, (logo_x, logo_y))

    # Desenha a caixa na lateral esquerda
    # screen: A superfície de destino na qual o retângulo será desenhado (geralmente a tela principal do jogo).
    
    # (100, 100, 100): A cor da borda do retângulo em formato RGB, neste caso, um cinza claro (100, 100, 100).
    rect_border_color = (100, 100, 100)
    
    # (300, 10, 480, 480): Uma tupla contendo as coordenadas e o tamanho do retângulo no formato 
    # (x, y, largura, altura). Neste caso, x=300, y=10, largura=480 e altura=480.
    rect_x = 500
    rect_y = 10
    rect_width = 480
    rect_height = 480
    rect_cordinate_and_size = (rect_x, rect_y, rect_width, rect_height)
    
    # 2: A espessura da linha que forma o retângulo. Neste caso, a espessura é 2 pixels. Se o valor for 0, o retângulo será preenchido.
    border_thickness = 4
    pygame.draw.rect(screen, rect_border_color, rect_cordinate_and_size, border_thickness)


    # Desenha o retângulo de fundo (preenchido) dentro do retângulo de borda
    cor_de_fundo = (200, 200, 200)  # Defina a cor de fundo que você deseja usar
     # (x, y, largura, altura). Neste caso, x=300, y=10, largura=480 e altura=480.
    pygame.draw.rect(screen, cor_de_fundo, ((rect_x + border_thickness), (rect_y + border_thickness), (rect_width - border_thickness), (rect_height - border_thickness)), 0)

def main():
    
    screen = init_pygame()
    resources = load_resources()
    logo = resources["logo"]

    # Prepara a classe TextPrint
    text_print = TextPrint()
    text_print.x = 320  # Ajuste o valor de X para a posição inicial da caixa lateral
    text_print.y = 60  # Ajuste o valor de Y para a posição inicial da caixa lateral

    # Usado para controlar a velocidade de atualização da tela
    clock = pygame.time.Clock()

    # Dicionário para armazenar os joysticks conectados
    joysticks = {}

    # Variável de controle do loop principal
    done = False
    while not done:        
        
        # Processamento de eventos
        # Eventos possíveis do joystick: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Marca o fim do programa

            if event.type == pygame.JOYBUTTONDOWN:
                print("Botão do joystick pressionado.")
                # Verifica se o botão 0 foi pressionado
                if event.button == 0:
                    # Verifica se o efeito de vibração pode ser reproduzido
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Efeito de vibração reproduzido no joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Botão do joystick solto.")
            # Adiciona o novo joystick à lista de joysticks conectados
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} conectado")

            # Remove o joystick desconectado da lista de joysticks conectados
            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} desconectado")
        
        # Desenho na tela
        # Primeiro, limpa a tela com branco. Não coloque outros comandos de desenho
        # acima desta linha, pois serão apagados com este comando.
        # screen.fill((255, 255, 255)) # co de fundo branco.
        screen.fill((0, 0, 0))
        text_print.reset()

        draw_ui(screen, logo)

        # Conta o número de joysticks conectados
        joystick_count = pygame.joystick.get_count()

        # Exibe o número de joysticks conectados
        text_print.tprint(screen, f"Número de joysticks conectados: {joystick_count}")
        text_print.indent()

        # Para cada joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            # Exibe o identificador do joystick
            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Obtém o nome do joystick
            name = joystick.get_name()
            text_print.tprint(screen, f"Nome do joystick: {name}")

            # Obtém o identificador único do joystick
            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            # Obtém o nível de energia do joystick
            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Nível de energia do joystick: {power_level}")

            # Desenha as checkboxes na posição (50, 300) com tamanho 20x20
            checkboxes_x = 510
            checkboxes_y = 250
            draw_checkboxes(joystick, checkboxes_x, checkboxes_y, 20, 20, screen)

            handle_triggers(joystick, text_print, screen)

            # vamos desenhar aqui, em algum ponto da tela a parte do plano cartesiano que recebe as informacoes 
            # dos eixos dos controles.
            # draw_analog_stick(joystick, eixo_x, eixo_y, x, y, largura, altura, tela)

            analog_stick_x = 550 
            analog_stick_y = 50
            draw_analog_stick(joystick, 0, 1, analog_stick_x + 000 , analog_stick_y, 140, 140, screen)  # Analógico esquerdo
            draw_analog_stick(joystick, 2, 3, analog_stick_x + 250 , analog_stick_y, 140, 140, screen)  # Analógico direito

            # *******************************************
            # *******************************************
            # *******************************************
            handle_analog_axes(joystick, text_print, screen)
            handle_buttons(joystick, text_print, screen)
            handle_hats(joystick, text_print, screen)

            text_print.unindent()


        # Atualiza a tela com o que foi desenhado
        pygame.display.flip()

        # Limita a 30 quadros por segundo
        clock.tick(30)

if __name__ == "__main__":
    main()
    # Se esquecer desta linha, o programa ficará preso ao sair
    # se estiver sendo executado a partir do IDLE.
    pygame.quit()