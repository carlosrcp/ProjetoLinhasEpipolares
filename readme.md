Bibliotecas:

* tkinter
* numpy
* cv2
* matplotlib


Use imagens com prefixo "image1" e "image2" na pasta imagens e edite o suffix no começo do código como estão nos exemplos.

Imagens com resoluções muito grandes podem gerar problemas no ajuste de tela.


projeto_setup.py (configuração)

- Você pode escolher o ponto que está sendo editado usando os botões < ou >
- Você pode criar um novo par de pontos ou editar um já existente
- O botão Salvar grava o arquivo json que guarda os pares de pontos para serem lidos pelos outros


projeto_vis.py (visualização)

- Com os 8 par de pontos definidos no setup, ao rodar esse código você poderá visualizar os resultados das linhas epipolares geradas pelos pontos pares de pontos definidos.

projeto_pontos.py (visualização interativa)

- Com os 8 par de pontos definidos no setup, ao rodar esse código você poderá clicar em uma das imagens para ver definir um ponto e ver a reta epipolar desse ponto na outra imagem.
- Aperte a tecla 'q' para fechar.
