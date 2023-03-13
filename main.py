# Inicio de exemplo extraido da: https://www.pygame.org/docs/ref/joystick.html

# Nome projeto: Controle-De-Games
# Data: [08/03/2023]
# Projeto Iniciado: [23/02/2023]
# Desenvolvido por:
#
# [AthenasArch].
# [Leonardo Hilgemberg Lopes].
# [Nome do Colaborador 3]
# [Nome do Colaborador 3]
# [Nome do Colaborador 3]
# [Nome do Colaborador 3]
# [E assim por diante...]

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

            # Obtém o número de eixos do joystick
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Número de eixos: {axes}")
            text_print.indent()

            # Exibe o valor atual de cada eixo
            for i in range(axes):
                axis = joystick.get_axis(i)
                text_print.tprint(screen, f"Eixo {i} valor: {axis:>6.3f}")
            text_print.unindent()

            # Obtém o número de botões do joystick
            buttons = joystick.get_numbuttons()
            text_print.tprint(screen, f"Número de botões: {buttons}")

            # Exibe o estado de cada botão
            for i in range(buttons):
                button = joystick.get_button(i)
                text_print.tprint(screen, f"Botão {i:>2} valor: {button}")
            text_print.unindent()

            # Obtém o número de chapeus (hat) do joystick
            hats = joystick.get_numhats()
            text_print.tprint(screen, f"Número de chapeus: {hats}")
            text_print.indent()

            # Exibe a posição atual de cada chapéu
            for i in range(hats):
                hat = joystick.get_hat(i)
                text_print.tprint(screen, f"Chapéu {i} valor: {str(hat)}")
            text_print.unindent()

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