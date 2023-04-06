Função main
===========

A função principal do programa é responsável por controlar e exibir informações sobre joysticks conectados. Ela inicializa o ambiente Pygame, carrega recursos e entra em um loop principal que lê eventos de joystick e exibe informações sobre joysticks conectados na tela. O loop principal termina quando o usuário fecha a janela do aplicativo.

A função também desenha um gráfico mostrando a posição dos analógicos e a direção dos direcionais digitais, bem como uma caixa de seleção que permite ao usuário inverter o eixo Y dos analógicos.

.. literalinclude:: ../path/to/your/main_function.py
   :language: python
   :pyobject: main
