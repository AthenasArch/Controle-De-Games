# -----------------------------------------------------------------------------
# Nome do arquivo: main.py
# Descrição: Este projeto tras uma interface grafica para vizualizar acionamentos de botoes de Joysticks
#
# Autor: Leonardo Hilgemberg Lopes.
# Empresa: AthenasArch.
# Data de criação: 08/03/2023.
# Última atualização: 04/04/2023.
# Versão: 2.1
# -----------------------------------------------------------------------------
# 
# Base de codigos utilizada:
# https://www.pygame.org/docs/ref/joystick.html
# -----------------------------------------------------------------------------
import math
import pygame

# Definicao de cores - Basic colors in RGB tuples. 
RGB_COLOR_BLACK = (0, 0, 0)  # Preto
RGB_COLOR_WHITE = (255, 255, 255)  # Branco
RGB_COLOR_RED = (255, 0, 0)  # Vermelho
RGB_COLOR_GREEN = (0, 255, 0)  # Verde
RGB_COLOR_BLUE = (0, 0, 255)  # Azul
RGB_COLOR_YELLOW = (255, 255, 0)  # Amarelo
RGB_COLOR_CYAN = (0, 255, 255)  # Ciano
RGB_COLOR_MAGENTA = (255, 0, 255)  # Magenta
RGB_COLOR_GRAY = (128, 128, 128)  # Cinza
RGB_COLOR_LIGHT_GRAY = (200, 200, 200)  # Cinza Claro
RGB_COLOR_DARK_GRAY = (64, 64, 64)  # Cinza Escuro
RGB_COLOR_ORANGE = (255, 165, 0)  # Laranja
RGB_COLOR_PINK = (255, 105, 180)  # Rosa
RGB_COLOR_BROWN = (139, 69, 19)  # Marrom


# Classe TextPrint que será usada para exibir informações na tela
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 24) # Configura a fonte a ser usada para exibir o texto
        self.text_color = RGB_COLOR_WHITE # Define a cor do texto como branco

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

# CRIA A CHECKBOX
class Checkbox:
    def __init__(self, x, y, width, height, text, font, font_color, check_color, box_color, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_color = font_color
        self.check_color = check_color
        self.box_color = box_color
        self.screen = screen
        self.checked = False

    def render(self):
        pygame.draw.rect(self.screen, self.box_color, (self.x, self.y, self.width, self.height), 2)
        if self.checked:
            pygame.draw.rect(self.screen, self.check_color, (self.x + 4, self.y + 4, self.width - 8, self.height - 8))
        
        text_surface = self.font.render(self.text, True, self.font_color)
        self.screen.blit(text_surface, (self.x + self.width + 5, self.y))

    def toggle(self):
        self.checked = not self.checked

    def is_mouse_over(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

#inicializa a checkbox 
def initialize_checkbox(screen):
    font = pygame.font.Font(None, 25)
    checkbox = Checkbox(520, 450, 20, 20, "Inverter eixo Y", font, RGB_COLOR_BLACK, RGB_COLOR_RED, RGB_COLOR_BLACK, screen)
    return checkbox

# trata a checkbox
def handle_checkbox_click(checkbox, event, last_click_time, click_interval):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Botão esquerdo do mouse
            current_time = pygame.time.get_ticks()
            if checkbox.is_mouse_over(pygame.mouse.get_pos()) and current_time - last_click_time > click_interval:
                checkbox.toggle()
                last_click_time = current_time
    return last_click_time

# Trata os eixos analogicos no joystick
def handle_analog_axes(joystick, text_print, screen):

    text_print.tprint(screen, f"")
    # Obtém o número de eixos do joystick
    axes = joystick.get_numaxes()
    text_print.tprint(screen, f"Número de eixos: {axes}")
    text_print.indent()

    # Exibe o valor atual de cada eixo
    for i in range(axes):
        axis = joystick.get_axis(i)
        text_print.tprint(screen, f"  Eixo {i} valor: {axis:>6.3f}")
    
    text_print.unindent()


# Desenha os analogicos direcionais
def draw_analog_stick(joystick, axis_x, axis_y, x, y, width, height, screen, invert_y=False):
    
    # Converte os valores analógicos para coordenadas no plano cartesiano
    xpos = int((joystick.get_axis(axis_x) + 1) * width / 2 + x)
    if invert_y:
        ypos = int((-joystick.get_axis(axis_y) + 1) * height / 2 + y) # faz o eixo trabalhar invertido do controle
    else:
        ypos = int((joystick.get_axis(axis_y) + 1) * height / 2 + y)

    # Desenha o plano cartesiano como um retângulo
    pygame.draw.rect(screen, RGB_COLOR_BLACK, (x, y, width, height), 2)

    # Desenha uma linha do centro do plano até a posição da bolinha
    center_x = x + width // 2
    center_y = y + height // 2
    border_line = 3
    pygame.draw.line(screen, RGB_COLOR_YELLOW, (center_x, center_y), (xpos, ypos), border_line)

    # Desenha a bolinha na posição atual
    pygame.draw.circle(screen, RGB_COLOR_RED, (xpos, ypos), 10)


def draw_gradient_arc(screen, start_angle, end_angle, x, y, radius, color1, color2, steps):
    # Função para desenhar um gradiente de cores em um arco
    # Parâmetros:
    # - screen: superfície do Pygame onde o arco será desenhado
    # - start_angle, end_angle: ângulos inicial e final do arco (em graus)
    # - x, y: coordenadas do canto superior esquerdo do retângulo delimitador do arco
    # - radius: raio do arco
    # - color1, color2: cores inicial e final do gradiente
    # - steps: número de passos para interpolação linear das cores

    angle_step = (end_angle - start_angle) / steps  # Calcula o tamanho do passo angular

    for i in range(steps):
        angle1 = start_angle + i * angle_step  # Ângulo inicial do segmento atual
        angle2 = angle1 + angle_step  # Ângulo final do segmento atual

        # Interpolação linear das cores
        color = (
            int(color1[0] + i * (color2[0] - color1[0]) / steps),
            int(color1[1] + i * (color2[1] - color1[1]) / steps),
            int(color1[2] + i * (color2[2] - color1[2]) / steps),
        )

        # Desenha o segmento de arco com a cor interpolada

        border_thickness = 14
        pygame.draw.arc(screen, color, (x, y, 2 * radius, 2 * radius), math.radians(angle1), math.radians(angle2), border_thickness)


def draw_trigger_velocity(trigger_value, x, y, screen, invert_y=False):
    radius = 50  # Raio do velocímetro
    # Ângulo da seta, baseado no valor do gatilho (-1 a 1, mapeado para 180 a 360 graus)
    if invert_y:

        angle = 180 * (1 - (trigger_value + 1) / 2)
        
        # Desenha o gradiente de cores ao redor do arco base do velocímetro
        angle_start = 180
        angle_end = 360
        draw_gradient_arc(screen, 180, 360, x, y, radius, RGB_COLOR_GREEN, RGB_COLOR_RED, 50)
        
        # Calcula as coordenadas da ponta da seta usando trigonometria
        end_x = x + radius + radius * math.cos(math.radians(angle))
        end_y = y + radius + radius * math.sin(math.radians(angle))
    else:
        # como foi realizado o calculo do angulo:
        # 1)    trigger_value + 1: O valor do gatilho varia de -1 a 1. Ao adicionar 1, o intervalo é 
        #       ajustado para 0 a 2.
        # .
        # 2)    (trigger_value + 1) / 2: Agora que o intervalo é de 0 a 2, dividimos por 2 para normalizá-lo 
        #       para um intervalo de 0 a 1.
        # .
        # 3)    180 * (trigger_value + 1) / 2: Multiplicamos o valor normalizado (0 a 1) por 180 para converter 
        #       o intervalo em um ângulo que varia de 0 a 180 graus.
        #
        # 4)    180 - 180 * (trigger_value + 1) / 2: Por fim, subtraímos o ângulo obtido no passo anterior de 180. 
        #       Isso inverte a direção do arco, fazendo com que ele vá de 180 graus quando o gatilho está em -1 (não pressionado) a 0 graus quando o gatilho está em 1 (totalmente pressionado).
        angle = 180 - 180 * (trigger_value + 1) / 2
        
        # Desenha o gradiente de cores ao redor do arco base do velocímetro
        angle_start = 180
        angle_end = 360
        draw_gradient_arc(screen, 0, 180, x, y, radius, RGB_COLOR_GREEN, RGB_COLOR_RED, 50)
        end_x = x + radius + radius * math.cos(math.radians(angle))
        end_y = y + radius - radius * math.sin(math.radians(angle))

    # Desenha a seta do velocímetro
    pygame.draw.line(screen, (0, 0, 255), (x + radius, y + radius), (end_x, end_y), 2)


def handle_triggers(joystick, text_print, screen, invert_y=False):
    # Verifique se o joystick tem pelo menos 6 eixos analógicos
    if joystick.get_numaxes() < 6:
        # Se o joystick não tiver pelo menos 6 eixos, ele provavelmente não tem gatilhos analógicos
        text_print.tprint(screen, f"Este joystick não possui gatilhos analógicos.")
        return

    trigger_left = joystick.get_axis(4)
    trigger_right = joystick.get_axis(5)

    text_print.tprint(screen, f"")
    text_print.tprint(screen, f"Gatilhos:")
    # Exibe os valores dos gatilhos na tela
    text_print.tprint(screen, f"  Esquerdo: {trigger_left:>6.3f}")
    text_print.tprint(screen, f"  Direito: {trigger_right:>6.3f}")

    trigger_x = 550  # Coordenada X dos velocímetros na tela
    trigger_y = 300  # Coordenada Y dos velocímetros na tela

    # Desenha o velocímetro para o gatilho esquerdo
    draw_trigger_velocity(trigger_left, trigger_x, trigger_y, screen, invert_y)

    # Desenha o velocímetro para o gatilho direito, deslocado horizontalmente em 250 unidades
    draw_trigger_velocity(trigger_right, trigger_x + 250, trigger_y, screen, invert_y)


# trata os botoes
def handle_buttons(joystick, text_print, screen):

    # Obtém o número de botões do joystick
    buttons = joystick.get_numbuttons()
    text_print.tprint(screen, f"")
    text_print.tprint(screen, f"Número de botões: {buttons}")

    # Exibe o estado de cada botão
    for i in range(buttons):
        button = joystick.get_button(i)
        text_print.tprint(screen, f"    Botão {i:>2} valor: {button}")
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



def handle_digitalDirectionals(joystick, text_print, screen):

    # Obtém o número de Direcionais (direcional) do joystick
    directionals = joystick.get_numhats()
    text_print.tprint(screen, f"Número de Direcionais digitais: {directionals}")
    text_print.indent()

    # Exibe a posição atual de cada uma das cirecionais
    for i in range(directionals):
        directional = joystick.get_hat(i)
        text_print.tprint(screen, f"Direcional {i} valor: {str(directional)}")
    text_print.unindent()

# trata a inicializacao da pygame e retorna a tela
def init_pygame():
    pygame.init() # Inicializa a biblioteca Pygame
    size = (1100, 700)  # Aumente a largura da tela para acomodar a caixa de texto
    # Configura o tamanho da tela (largura, altura) e o nome da janela
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Teste de Joystick - AthenasArch")
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
    logo_y = 550 
    screen.blit(logo, (logo_x, logo_y))

    # Desenha a caixa na lateral esquerda
    # screen: A superfície de destino na qual o retângulo será desenhado (geralmente a tela principal do jogo).
    
    # (100, 100, 100): A cor da borda do retângulo em formato RGB, neste caso, um cinza claro (100, 100, 100).
    rect_border_color = (RGB_COLOR_BLUE)
    
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
    cor_de_fundo = (RGB_COLOR_DARK_GRAY)  # Defina a cor de fundo que você deseja usar
     # (x, y, largura, altura). Neste caso, x=300, y=10, largura=480 e altura=480.
    pygame.draw.rect(screen, cor_de_fundo, ((rect_x + border_thickness), (rect_y + border_thickness), (rect_width - (border_thickness*2)), (rect_height - (border_thickness*2))), 0)

# Processamento de eventos
# Eventos possíveis do joystick: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
# JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
def handle_event(event, joysticks):
    """
    Processa os eventos do pygame e atualiza a lista de joysticks conectados.

    :param event: Evento do Pygame a ser processado.
    :param joysticks: Dicionário contendo os joysticks conectados.
    :return: Retorna True se o evento QUIT foi detectado, caso contrário, retorna False.
    """
    quit_detected = False

    if event.type == pygame.QUIT:
        quit_detected = True  # Marca o fim do programa

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

    return quit_detected

def display_joystick_info(screen, text_print, joysticks, checkbox):
    
    # Conta o número de joysticks conectados
    joystick_count = pygame.joystick.get_count()

    # Exibe o número de joysticks conectados
    text_print.tprint(screen, f"Número de joysticks conectados: {joystick_count}")
    text_print.indent()

    # Para cada joystick:
    for joystick in joysticks.values():
        jid = joystick.get_instance_id()

        # text_print.tprint(screen, f"")
        # Exibe o identificador do joystick
        text_print.tprint(screen, f"Dados do Joystick {jid}:")
        text_print.indent()
    
        # Obtém o nome do joystick
        text_print.tprint(screen, f"")
        name = joystick.get_name()
        text_print.tprint(screen, f"Nome do joystick: ")
        text_print.tprint(screen, f"- {name}")
        # text_print.tprint(screen, f"")

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

        # trata os gatilhos do controle
        handle_triggers(joystick, text_print, screen, invert_y=checkbox.checked)

        # vamos desenhar aqui, em algum ponto da tela a parte do plano cartesiano que recebe as informacoes 
        # dos eixos dos controles.
        # draw_analog_stick(joystick, eixo_x, eixo_y, x, y, largura, altura, tela)

        # Renderize a checkbox e desenhe o joystick com o valor invertido
        checkbox.render()
        
        analog_stick_x = 550 
        analog_stick_y = 50
        num_axes = joystick.get_numaxes()

        # Verifica primeiro se o Joystick utiliza gatilhos e eixos analogicos antes de tentar desenhar
        if num_axes > 1:
            draw_analog_stick(joystick, 0, 1, analog_stick_x + 000 , analog_stick_y, 140, 140, screen, invert_y=checkbox.checked)  # Analógico esquerdo
        if num_axes > 3:
            draw_analog_stick(joystick, 2, 3, analog_stick_x + 250 , analog_stick_y, 140, 140, screen, invert_y=checkbox.checked)  # Analógico direito

        # draw_analog_stick(joystick, 0, 1, analog_stick_x + 000 , analog_stick_y, 140, 140, screen, invert_y=checkbox.checked)  # Analógico esquerdo
        # draw_analog_stick(joystick, 2, 3, analog_stick_x + 250 , analog_stick_y, 140, 140, screen, invert_y=checkbox.checked)  # Analógico direito

        # *******************************************
        # *******************************************
        # *******************************************
        handle_analog_axes(joystick, text_print, screen)
        handle_buttons(joystick, text_print, screen)
        handle_digitalDirectionals(joystick, text_print, screen)

        text_print.unindent()

def main():
    # estou gerando a documentacao do projeto, esta e minhe ´primeira documentcacao, 
    # entao vou testar ela neste codigo.
    """
    Função principal do programa para controlar e exibir informações sobre
    joysticks conectados.
    """
    screen = init_pygame()
    resources = load_resources()
    logo = resources["logo"]

    # Prepara a classe TextPrint
    text_print = TextPrint()
    text_print.x = 320  # Ajuste o valor de X para a posição inicial da caixa lateral
    text_print.y = 60  # Ajuste o valor de Y para a posição inicial da caixa lateral

    # Inicialize a fonte e crie a checkbox
    checkbox = initialize_checkbox(screen)

    # Variáveis para controlar o intervalo entre cliques da checkbox
    click_interval = 100  # Intervalo mínimo entre cliques em milissegundos
    last_click_time = 0

    # Usado para controlar a velocidade de atualização da tela
    clock = pygame.time.Clock()

    # Dicionário para armazenar os joysticks conectados
    joysticks = {}

    # Variável de controle do loop principal
    done = False
    while not done:        
        for event in pygame.event.get():
            quit_detected = handle_event(event, joysticks)
            if quit_detected:
                done = True

        # Adicione um evento para lidar com cliques do mouse
        last_click_time = handle_checkbox_click(checkbox, event, last_click_time, click_interval)


        # Desenho na tela
        # Primeiro, limpa a tela com branco. Não coloque outros comandos de desenho
        # acima desta linha, pois serão apagados com este comando.
        # screen.fill((255, 255, 255)) # co de fundo branco.
        screen.fill((0, 0, 0))
        text_print.reset()

        draw_ui(screen, logo)
        display_joystick_info(screen, text_print, joysticks, checkbox)

        # Atualiza a tela com o que foi desenhado
        pygame.display.flip()

        # Limita a 30 quadros por segundo
        clock.tick(30)

if __name__ == "__main__":
    main()
    # Se esquecer desta linha, o programa ficará preso ao sair
    # se estiver sendo executado a partir do IDLE.
    pygame.quit()