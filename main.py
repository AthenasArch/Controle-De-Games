# Inicio de exemplo extraido da: https://www.pygame.org/docs/ref/joystick.html

# Nome projeto: Controle-De-Games
# Data: [08/03/2023]
# Projeto Iniciado: [23/02/2023]
# Desenvolvido por:
#
# [AthenasArch].
# [Leonardo Hilgemberg Lopes].

import pygame

# Inicializa a biblioteca Pygame
pygame.init()

# Classe TextPrint que será usada para exibir informações na tela
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25) # Configura a fonte a ser usada para exibir o texto

    def tprint(self, screen, text):
        # Renderiza o texto na tela
        text_bitmap = self.font.render(text, True, (0, 0, 0))
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
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)

    # Desenha uma linha do centro do plano até a posição da bolinha
    center_x = x + width // 2
    center_y = y + height // 2
    pygame.draw.line(screen, (0, 0, 255), (center_x, center_y), (xpos, ypos), 2)

    # Desenha a bolinha na posição atual
    pygame.draw.circle(screen, (255, 0, 0), (xpos, ypos), 10)

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

def main():
    # Configura o tamanho da tela (largura, altura) e o nome da janela
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Exemplo de Joystick")

    # Usado para controlar a velocidade de atualização da tela
    clock = pygame.time.Clock()

    # Prepara a classe TextPrint
    text_print = TextPrint()

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
        screen.fill((255, 255, 255))
        text_print.reset()

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
            draw_checkboxes(joystick, 50, 300, 20, 20, screen)

            # vamos desenhar aqui, em algum ponto da tela a parte do plano cartesiano que recebe as informacoes 
            # dos eixos dos controles.
            # draw_analog_stick(joystick, eixo_x, eixo_y, x, y, largura, altura, tela)
            draw_analog_stick(joystick, 0, 1, 50, 50, 140, 140, screen)  # Analógico esquerdo
            draw_analog_stick(joystick, 2, 3, 300, 50, 140, 140, screen)  # Analógico direito

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