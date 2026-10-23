"""Beginner electronics lessons and their matching Circuita projects."""


LESSONS = [
    {
        "title": "Modulo 1 - LED, resistor e pilhas",
        "goal": "Acender um LED com uma fonte pequena e entender por que o resistor fica em serie.",
        "parts": "Suporte com 3 pilhas AA alcalinas (4,5 V), LED vermelho, resistor de 220 ohms / 1/4 W e fios. Este circuito nao usa um diodo separado: o LED ja e um tipo de diodo.",
        "safety": "Use pilhas AA em um suporte fechado. Nunca ligue este circuito a tomada, fonte sem identificacao ou bateria retangular de 9 V. Confirme a polaridade do LED antes de alimentar. Nao adicione outro componente da biblioteca chamado Diodo nesta aula.",
        "steps": [
            "Com a fonte desconectada, identifique o polo + e o polo - do suporte.",
            "Ligue o polo + ao primeiro terminal do resistor de 220 ohms. O resistor nao tem lado certo.",
            "Ligue o outro terminal do resistor a perna longa do LED (anodo, A).",
            "Ligue a perna curta do LED (catodo, K; geralmente o lado achatado do encapsulamento) ao polo -.",
            "Confira todas as ligacoes. So entao coloque as pilhas.",
        ],
        "observe": "O LED acende. Estimativa: (4,5 V - 2,0 V) / 220 ohms = 0,011 A, ou cerca de 11 mA. O resistor transforma parte da energia em calor e limita a corrente.",
        "real": "No projeto visual, siga + -> resistor A/B -> LED A/K -> -. O LED ja e um diodo que emite luz; nao coloque um segundo diodo em serie nesta aula. O diodo separado da biblioteca e usado no modulo do motor. Pecas reais variam: use o valor de Vf da ficha tecnica quando disponivel. Para este LED vermelho comum, 220 ohms / 1/4 W e uma escolha conservadora neste circuito de 4,5 V.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 135, "y": 225, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 360, "y": 225, "resistance": 220.0},
                {"id": 3, "type": "led", "x": 590, "y": 225},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 2 - Botao liga/desliga",
        "goal": "Abrir e fechar o circuito com um botao em serie.",
        "parts": "Suporte com 3 pilhas AA (4,5 V), LED vermelho, resistor de 220 ohms / 1/4 W, botao normalmente aberto de 4 terminais e fios.",
        "safety": "Mantenha as pilhas fora do suporte durante a montagem. Botoes tact de 4 terminais costumam ter dois pares de pernas ja conectados internamente. Use o multimetro em continuidade para identificar os pares; modelos diferem.",
        "steps": [
            "Identifique com o multimetro quais pernas do botao pertencem ao mesmo lado. Ao pressionar, o botao conecta um lado ao outro.",
            "Ligue o polo + do suporte ao resistor de 220 ohms.",
            "Ligue o resistor a perna longa (A) do LED.",
            "Ligue a perna curta (K) do LED a um lado do botao.",
            "Ligue o outro lado do botao ao polo - do suporte. Recoloque as pilhas e pressione o botao.",
        ],
        "observe": "O LED acende enquanto o caminho de + ate - estiver fechado. No quadro, clique no desenho do botao para alternar entre aberto e fechado.",
        "real": "Circuito: + -> resistor -> LED A/K -> botao -> -. No botao virtual, os terminais A e B representam os dois lados eletricos do interruptor, nao as quatro pernas fisicas do tact.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 115, "y": 230, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 310, "y": 230, "resistance": 220.0},
                {"id": 3, "type": "led", "x": 500, "y": 230},
                {"id": 4, "type": "button", "x": 690, "y": 230, "closed": False},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "4:A"], ["4:B", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 3 - Capacitor e carga",
        "goal": "Observar que um capacitor armazena carga por um tempo e aprender a respeitar sua polaridade.",
        "parts": "Suporte com 3 pilhas AA (4,5 V), capacitor eletrolitico de 470 uF com tensao nominal de pelo menos 10 V, resistor de 1 kohm / 1/4 W e multimetro.",
        "safety": "Confira a faixa no corpo do capacitor: ela geralmente marca o terminal negativo. Nunca exceda a tensao nominal, nao inverta a polaridade e nao coloque o capacitor em curto. Com as pilhas retiradas, descarregue-o atraves do resistor de 1 kohm e confirme perto de 0 V no multimetro. Nao o descarregue ligando as pernas diretamente.",
        "steps": [
            "Com o suporte desligado, ligue + ao resistor de 1 kohm.",
            "Ligue o outro lado do resistor ao terminal + do capacitor.",
            "Ligue o terminal - do capacitor ao polo - do suporte.",
            "Coloque as pilhas. Meça a tensao entre as pernas do capacitor; ela sobe gradualmente.",
            "Retire as pilhas. Encoste os dois terminais do resistor de 1 kohm nos dois terminais do capacitor para descarrega-lo atraves do resistor; nunca use um fio direto. Meça novamente para confirmar que esta perto de 0 V.",
        ],
        "observe": "O resistor limita a corrente inicial. O tempo caracteristico aproximado e R x C: 1.000 ohms x 470 uF = 0,47 s. O valor real e influenciado pelas tolerancias e pelo multimetro.",
        "real": "O quadro mostra a ligacao, mas ainda calcula apenas regime DC e nao anima a carga/descarga. Portanto, use um multimetro para observar este modulo fisicamente; a simulacao nao deve ser interpretada como uma previsao temporal.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 130, "y": 240, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 370, "y": 240, "resistance": 1000.0},
                {"id": 3, "type": "capacitor", "x": 620, "y": 240, "capacitance": 470.0},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:B", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 4 - Potenciometro e entrada A0",
        "goal": "Usar um potenciometro como divisor de tensao e ler o cursor com a entrada analogica do Arduino.",
        "parts": "Arduino Uno, potenciometro de 10 kohms e fios. Prefira componentes de laboratorio e a alimentacao USB normal do Arduino.",
        "safety": "Este exemplo usa somente o 5 V regulado da placa. Nunca injete 9 V, tensao da tomada ou sinal acima de 5 V em A0. Identifique as pernas do seu potenciometro com a ficha tecnica ou multimetro: a perna central e normalmente o cursor, mas nao confie apenas na posicao.",
        "steps": [
            "Com o Arduino desconectado do computador, ligue uma extremidade do potenciometro ao 5V/VCC da placa.",
            "Ligue a outra extremidade ao GND.",
            "Ligue a perna central (cursor W) a A0.",
            "Revise as ligacoes e so entao conecte o Arduino ao USB.",
            "Execute READ A0. Gire o potenciometro e repita a leitura; o valor deve variar de perto de 0 a perto de 1023.",
        ],
        "observe": "O cursor produz uma tensao entre 0 e 5 V. A leitura de 10 bits do Uno representa essa faixa com valores aproximados de 0 a 1023.",
        "real": "No quadro, Arduino VCC representa o pino fisico 5V. A leitura e uma aproximacao; o simulador nao representa ruido, tolerancias nem todos os limites da placa.",
        "project": {
            "components": [
                {"id": 1, "type": "arduino", "x": 245, "y": 240, "pin13": 5.0},
                {"id": 2, "type": "potentiometer", "x": 570, "y": 240, "resistance": 10000.0, "wiper": 50.0},
            ],
            "wires": [["1:VCC", "2:A"], ["2:B", "1:GND"], ["2:W", "1:A0"]],
            "script": "READ A0",
        },
    },
    {
        "title": "Modulo 5 - Arduino e LED no D13",
        "goal": "Controlar um LED usando uma saida digital, mantendo um resistor de protecao em serie.",
        "parts": "Arduino Uno, LED vermelho, resistor de 220 ohms / 1/4 W, protoboard e fios. Use o pino GND da propria placa.",
        "safety": "Desconecte o USB antes de alterar fios. Nunca ligue um LED diretamente entre um pino e GND. Evite curtos entre 5V e GND. Mantenha a corrente do pino dentro dos limites recomendados pelo fabricante da placa.",
        "steps": [
            "Com o USB desconectado, ligue D13 ao resistor de 220 ohms.",
            "Ligue o outro lado do resistor a perna longa (A) do LED.",
            "Ligue a perna curta (K) do LED a GND do Arduino.",
            "Confira que o resistor esta em serie e so entao conecte o USB.",
            "No quadro, execute DIGITAL_WRITE 13 HIGH para acender e DIGITAL_WRITE 13 LOW para apagar.",
        ],
        "observe": "Com HIGH o pino fornece um sinal logico e a corrente percorre o resistor e o LED ate GND. O resistor de 220 ohms mantem a corrente em uma faixa adequada para este LED comum.",
        "real": "Para uma placa real, carregue um sketch na Arduino IDE. Exemplo minimo:\\n\\nvoid setup() { pinMode(13, OUTPUT); }\\nvoid loop() { digitalWrite(13, HIGH); delay(500); digitalWrite(13, LOW); delay(500); }\\n\\nO comando DIGITAL_WRITE do Circuita funciona apenas na simulacao; ele nao envia codigo para a placa.",
        "project": {
            "components": [
                {"id": 1, "type": "arduino", "x": 175, "y": 250, "pin13": 5.0},
                {"id": 2, "type": "resistor", "x": 415, "y": 210, "resistance": 220.0},
                {"id": 3, "type": "led", "x": 650, "y": 210},
            ],
            "wires": [["1:D13", "2:A"], ["2:B", "3:A"], ["3:K", "1:GND"]],
            "script": "DIGITAL_WRITE 13 HIGH",
        },
    },
    {
        "title": "Modulo 6 - Tela LCD I2C",
        "goal": "Conectar uma tela LCD 16x2 com adaptador I2C e entender alimentacao e sinais.",
        "parts": "Arduino Uno, modulo LCD 16x2 com adaptador I2C compativel com 5 V, fios. O endereco I2C depende do modulo.",
        "safety": "Desconecte o USB antes de ligar ou retirar os fios. Confira no modulo se VCC aceita 5 V: alguns displays usam 3,3 V. Inverter VCC/GND pode danificar o modulo.",
        "steps": [
            "Ligue VCC do adaptador ao pino 5V do Uno e GND a GND.",
            "Ligue SDA a SDA do Uno (A4 no Uno classico) e SCL a SCL (A5 no Uno classico).",
            "Revise o modelo do seu Uno e do adaptador; placas ou modulos diferentes podem ter pinos identificados de outro modo.",
            "Ajuste cuidadosamente o pequeno controle de contraste do adaptador, se a tela acender mas os caracteres nao aparecerem.",
            "No Circuita, execute DISPLAY Ola, circuito! para ver o texto no modelo de tela.",
        ],
        "observe": "VCC/GND alimentam o display; SDA/SCL transportam dados e clock pelo barramento I2C. O desenho mostra as conexoes, mas a tela simulada nao emula o firmware ou o endereco I2C fisico.",
        "real": "Para um LCD real e necessario carregar um sketch pela Arduino IDE e instalar/selecionar uma biblioteca compativel com o adaptador. DISPLAY no Circuita altera somente a tela virtual.",
        "project": {
            "components": [
                {"id": 1, "type": "arduino", "x": 230, "y": 255},
                {"id": 2, "type": "display", "x": 590, "y": 255, "text": "Ola, circuito!"},
            ],
            "wires": [
                ["1:VCC", "2:VCC"],
                ["1:GND", "2:GND"],
                ["1:A4", "2:SDA"],
                ["1:A5", "2:SCL"],
            ],
            "script": "DISPLAY Ola, circuito!",
        },
    },
    {
        "title": "Modulo 7 - Buzzer ativo",
        "goal": "Reconhecer a diferenca entre um buzzer ativo e um piezo passivo antes de ligar.",
        "parts": "Suporte de 2 pilhas AA (3 V), buzzer ativo com tensao nominal de 3 V e consumo compativel com o componente, fios.",
        "safety": "Leia a ficha tecnica do buzzer: alguns sao de 3 V, outros de 5 V ou mais; a polaridade e a corrente tambem variam. Use um buzzer ativo identificado e uma fonte com tensao compatível. Nao conecte buzzer desconhecido ao pino do Arduino.",
        "steps": [
            "Com as pilhas fora do suporte, confira a tensao e a polaridade nominal do buzzer no proprio componente/ficha tecnica.",
            "Ligue o polo + do suporte de 3 V ao terminal + do buzzer ativo de 3 V.",
            "Ligue o terminal - do buzzer ao polo - do suporte.",
            "Confira a polaridade e coloque as pilhas por um instante para testar.",
            "Desligue a fonte antes de guardar ou trocar o buzzer.",
        ],
        "observe": "Um buzzer ativo normalmente gera um tom quando recebe a alimentacao especificada. Um piezo passivo pode precisar de um sinal alternado e nao tocar com corrente continua.",
        "real": "O simulador representa o buzzer como uma carga resistiva indicativa; ele nao reproduz som, frequencia, consumo de partida nem o circuito interno do modulo.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 245, "y": 240, "voltage": 3.0, "format": "AA", "cells": 2},
                {"id": 2, "type": "buzzer", "x": 530, "y": 240, "resistance": 100.0},
            ],
            "wires": [["1:+", "2:+"], ["2:-", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 8 - Motor DC e diodo de protecao",
        "goal": "Ligar um pequeno motor DC a uma fonte adequada e conhecer a funcao do diodo de protecao.",
        "parts": "Motor DC pequeno explicitamente especificado para 3 V, suporte de 2 pilhas AA (3 V), diodo 1N4001 a 1N4007, fios e supervisao adulta.",
        "safety": "Use apenas um motor rotulado para 3 V e nunca prenda o eixo. Motores podem consumir muito mais corrente ao partir ou travar; pilhas AA podem aquecer se houver curto. Desligue antes de mexer. NAO acione o motor direto pelo pino do Arduino: para controle digital e necessario estagio de transistor/MOSFET, resistor de comando e diodo adequados, projetados para aquele motor.",
        "steps": [
            "Com as pilhas fora, fixe o motor para que o eixo possa girar livremente.",
            "Ligue + da fonte de 3 V ao terminal + do motor; ligue o outro terminal do motor ao -.",
            "Coloque o diodo em paralelo com o motor, reversamente polarizado durante o funcionamento: faixa do diodo (catodo) no lado + e anodo no lado -.",
            "Confira o sentido da faixa no diodo, as tensoes nominais e que nao ha fios desencapados em contato.",
            "Coloque as pilhas por um instante e retire-as se o motor, fios ou pilhas aquecerem.",
        ],
        "observe": "O motor gira quando a corrente passa. Ao desligar uma carga indutiva, o diodo oferece um caminho para a corrente gerada pela bobina e ajuda a proteger o circuito.",
        "real": "A simulacao e apenas resistiva: nao modela o giro, a corrente de partida nem a protecao transitoria. O diodo desenhado mostra a ligacao reversa recomendada, mas nao certifica o dimensionamento do componente.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 150, "y": 260, "voltage": 3.0, "format": "AA", "cells": 2},
                {"id": 2, "type": "motor", "x": 450, "y": 210, "resistance": 100.0},
                {"id": 3, "type": "diode", "x": 450, "y": 340},
            ],
            "wires": [
                ["1:+", "2:+"],
                ["2:-", "1:-"],
                ["3:K", "1:+"],
                ["3:A", "1:-"],
            ],
            "script": "",
        },
    },
    {
        "title": "Modulo 9 - Lampada de baixa tensao",
        "goal": "Aprender a alimentar uma lampada com a tensao nominal correta e distinguir sua carga de um LED.",
        "parts": "Lampada incandescente de lanterna rotulada para 3 V, soquete compativel, suporte fechado de 2 pilhas AA (3 V) e fios. Supervisao adulta.",
        "safety": "Use uma lampada e um soquete que correspondam exatamente a tensao da fonte. Lampadas incandescentes podem aquecer e consumir bastante corrente; nao toque no bulbo aceso. Pilhas AA podem aquecer se houver curto. Nao teste com a lampada fora do soquete nem use fonte desconhecida.",
        "steps": [
            "Confira no bulbo ou na embalagem que a lampada e especificada para 3 V.",
            "Com as pilhas fora, encaixe a lampada no soquete adequado.",
            "Ligue um terminal do soquete ao polo + do suporte de 2 pilhas AA.",
            "Ligue o outro terminal do soquete ao polo - do suporte.",
            "Revise os fios e teste por poucos segundos. Desligue e deixe esfriar antes de tocar.",
        ],
        "observe": "A lampada acende enquanto houver uma ligacao fechada. Diferente do LED, a lampada incandescente nao tem polaridade; seu filamento converte energia em luz e calor.",
        "real": "A lampada no simulador e uma resistencia fixa e nao estima a corrente real de uma lampada. Use o valor de corrente especificado no componente real; nao use o simulador para dimensionar a bateria ou o soquete.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 225, "y": 240, "voltage": 3.0, "format": "AA", "cells": 2},
                {"id": 2, "type": "lamp", "x": 525, "y": 240, "resistance": 100.0},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 10 - Dois resistores em serie",
        "goal": "Comparar a resistencia total e a tensao dividida entre componentes em serie.",
        "parts": "Suporte fechado de 3 pilhas AA alcalinas (4,5 V), resistores de 220 ohms e 330 ohms, protoboard e multimetro.",
        "safety": "Monte com as pilhas retiradas. Use somente resistores em bom estado e confira os valores pelo codigo de cores ou multimetro. Nunca meca resistencia em um circuito alimentado.",
        "steps": [
            "Com o suporte sem pilhas, ligue o polo + ao resistor de 220 ohms.",
            "Ligue o resistor de 220 ohms ao resistor de 330 ohms.",
            "Ligue o resistor de 330 ohms ao polo - do suporte.",
            "Com tudo desligado, confirme as conexoes.",
            "Coloque as pilhas e, se souber usar o multimetro, meca a tensao em cada resistor usando a escala de tensao DC.",
        ],
        "observe": "Em serie, as resistencias somam: 220 + 330 = 550 ohms. A corrente ideal aproximada e 4,5 / 550 = 8,2 mA. As quedas de tensao somam aproximadamente 4,5 V.",
        "real": "No quadro, conecte os dois resistores em uma unica cadeia entre + e -. Nunca use a escala de corrente para medir tensao; se nao conhecer o multimetro, peca ajuda ao professor.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 120, "y": 250, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 355, "y": 250, "resistance": 220.0},
                {"id": 3, "type": "resistor", "x": 590, "y": 250, "resistance": 330.0},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:B", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 11 - Resistores em paralelo",
        "goal": "Entender como dois caminhos em paralelo dividem a corrente da fonte.",
        "parts": "Suporte de 3 pilhas AA alcalinas (4,5 V), dois resistores de 470 ohms / 1/4 W, protoboard e fios.",
        "safety": "Desconecte as pilhas antes de refazer os fios. Confira os valores nominais dos resistores. Este projeto e apenas uma demonstracao de baixa tensao; nao ligue a protoboard a tomada.",
        "steps": [
            "Ligue o polo + do suporte a uma fileira livre da protoboard.",
            "Coloque o primeiro resistor entre essa fileira positiva e uma fileira negativa.",
            "Coloque o segundo resistor nas mesmas duas fileiras: cada resistor deve ter um lado ligado ao + e o outro ao -.",
            "Ligue a fileira negativa ao polo - do suporte.",
            "Confira que nenhum fio liga + diretamente a -, depois coloque as pilhas.",
        ],
        "observe": "Os dois resistores ficam sujeitos a 4,5 V e cada ramo conduz cerca de 9,6 mA no modelo ideal. A fonte fornece a soma das correntes dos ramos, aproximadamente 19 mA.",
        "real": "Os terminais A dos resistores ficam no mesmo no positivo e os B no mesmo no negativo. A resistencia equivalente e menor que a de cada resistor. Verifique as trilhas internas da sua protoboard.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 110, "y": 300, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 400, "y": 220, "resistance": 470.0},
                {"id": 3, "type": "resistor", "x": 400, "y": 380, "resistance": 470.0},
            ],
            "wires": [
                ["1:+", "2:A"], ["1:+", "3:A"],
                ["2:B", "1:-"], ["3:B", "1:-"],
            ],
            "script": "",
        },
    },
    {
        "title": "Modulo 12 - Dois LEDs em paralelo",
        "goal": "Montar dois ramos de LED em paralelo, cada um com seu proprio resistor limitador.",
        "parts": "Suporte de 3 pilhas AA alcalinas (4,5 V), dois LEDs vermelhos, dois resistores de 470 ohms / 1/4 W e fios.",
        "safety": "A fonte deve ficar desconectada durante a montagem. Cada LED precisa de seu proprio resistor em serie. Nao ligue os LEDs diretamente em paralelo sem resistores individuais.",
        "steps": [
            "Monte o primeiro ramo: polo +, resistor de 470 ohms, perna longa A do LED e perna curta K ligada ao polo -.",
            "Monte um segundo ramo separado com o outro resistor de 470 ohms e o segundo LED, tambem entre + e -.",
            "Revise se os dois ramos tem seus proprios resistores e se os LEDs estao na polaridade correta.",
            "Coloque as pilhas e observe os dois LEDs.",
        ],
        "observe": "Os dois LEDs devem acender. Cada resistor limita a corrente do seu ramo a aproximadamente (4,5 - 2) / 470 = 5,3 mA. Os ramos compartilham a fonte, mas cada LED tem seu limitador.",
        "real": "Conecte as entradas dos dois resistores ao mesmo positivo e os catodos dos LEDs ao mesmo negativo. Nao use um unico resistor compartilhado entre LEDs em paralelo: diferencas entre LEDs podem dividir a corrente de forma desigual.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 110, "y": 300, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 340, "y": 210, "resistance": 470.0},
                {"id": 3, "type": "led", "x": 560, "y": 210},
                {"id": 4, "type": "resistor", "x": 340, "y": 390, "resistance": 470.0},
                {"id": 5, "type": "led", "x": 560, "y": 390},
            ],
            "wires": [
                ["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "1:-"],
                ["1:+", "4:A"], ["4:B", "5:A"], ["5:K", "1:-"],
            ],
            "script": "",
        },
    },
    {
        "title": "Modulo 13 - Dois LEDs em serie",
        "goal": "Observar como as quedas de tensao dos LEDs se somam em uma unica cadeia.",
        "parts": "Suporte de 4 pilhas AA alcalinas (6 V), dois LEDs vermelhos e resistor de 330 ohms / 1/4 W.",
        "safety": "Desconecte a fonte enquanto monta. Confirme a polaridade de cada LED e mantenha o resistor em serie. Nao adicione pilhas para tentar forcar um LED a acender.",
        "steps": [
            "Ligue + do suporte ao resistor de 330 ohms.",
            "Ligue o resistor a perna longa A do primeiro LED.",
            "Ligue o catodo K do primeiro LED ao anodo A do segundo LED.",
            "Ligue o catodo K do segundo LED ao polo -.",
            "Revise toda a cadeia antes de colocar as pilhas.",
        ],
        "observe": "As quedas diretas dos LEDs se somam, aproximadamente 2 V + 2 V. A corrente ideal fica perto de (6 - 4) / 330 = 6 mA. Se um LED for invertido, a cadeia deixa de conduzir.",
        "real": "Os dois LEDs e o resistor formam um unico caminho. Use valores de Vf da ficha tecnica; LEDs azuis ou brancos podem ter queda maior e nao devem ser tratados como LEDs vermelhos.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 110, "y": 250, "voltage": 6.0, "format": "AA", "cells": 4},
                {"id": 2, "type": "resistor", "x": 310, "y": 250, "resistance": 330.0},
                {"id": 3, "type": "led", "x": 500, "y": 250},
                {"id": 4, "type": "led", "x": 690, "y": 250},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "4:A"], ["4:K", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 14 - Diodo e sentido da corrente",
        "goal": "Reconhecer anodo e catodo de um diodo retificador e testar a conducao em um circuito de baixa tensao.",
        "parts": "Suporte fechado de 3 pilhas AA alcalinas (4,5 V), diodo 1N4001 a 1N4007, resistor de 470 ohms / 1/4 W e multimetro em continuidade (opcional).",
        "safety": "Desligue as pilhas antes de inverter o diodo. A faixa no corpo costuma identificar o catodo (K), mas confirme a folha de dados. Mantenha o resistor em serie. Esta aula nao usa tensao da tomada.",
        "steps": [
            "Com o suporte sem pilhas, identifique a faixa do diodo: ela normalmente marca o catodo K.",
            "Ligue + ao resistor de 470 ohms.",
            "Ligue o resistor ao anodo A, o lado sem a faixa.",
            "Ligue o catodo K, lado com a faixa, ao polo -.",
            "Coloque as pilhas; retire-as antes de inverter o diodo e observar que a corrente cai.",
        ],
        "observe": "Com o diodo no sentido A para K, o modelo conduz e a queda direta aproximada e 0,7 V. Invertido, ele bloqueia a corrente no modelo simplificado.",
        "real": "A faixa do componente fisico e o catodo. Um diodo retificador nao emite luz; o LED e outro tipo de diodo com comportamento proprio. A queda real depende da corrente e do componente.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 110, "y": 250, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 335, "y": 250, "resistance": 470.0},
                {"id": 3, "type": "diode", "x": 570, "y": 250},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 15 - LED invertido (polaridade)",
        "goal": "Entender por que um LED tem polaridade e comparar o circuito correto com um LED invertido.",
        "parts": "Suporte de 2 pilhas AA alcalinas (3 V), LED vermelho, resistor de 470 ohms / 1/4 W e fios.",
        "safety": "Use somente 3 V neste teste e desconecte as pilhas antes de inverter o LED. Nunca tente este experimento com 9 V: LEDs comuns suportam pouca tensao reversa e podem ser danificados.",
        "steps": [
            "Monte a cadeia com +, resistor de 470 ohms, catodo K do LED e depois anodo A de volta ao polo - (LED invertido).",
            "Confira que a fonte tem apenas duas pilhas AA alcalinas (3 V).",
            "Coloque as pilhas por um instante e observe que o LED normalmente fica apagado.",
            "Retire as pilhas, inverta o LED e volte a conectar o anodo A depois do resistor e o catodo K ao negativo.",
            "Recoloque as pilhas e compare. Nao aumente a tensao para forcar o LED invertido.",
        ],
        "observe": "No modelo, o LED invertido bloqueia corrente e fica apagado; na orientacao correta ele acende. Componentes reais tem limites reversos; o teste deve permanecer em 3 V.",
        "real": "A perna longa costuma ser o anodo A e a curta/corpo achatado costuma indicar o catodo K. Essas pistas variam se as pernas foram cortadas; consulte a ficha tecnica.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 110, "y": 250, "voltage": 3.0, "format": "AA", "cells": 2},
                {"id": 2, "type": "resistor", "x": 335, "y": 250, "resistance": 470.0},
                {"id": 3, "type": "led", "x": 570, "y": 250},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:K"], ["3:A", "1:-"]],
            "script": "",
        },
    },
    {
        "title": "Modulo 16 - Dois botoes em serie (E)",
        "goal": "Montar uma logica simples em que os dois botoes precisam estar fechados para acender o LED.",
        "parts": "Suporte de 3 pilhas AA alcalinas (4,5 V), LED vermelho, resistor de 470 ohms / 1/4 W, dois botoes normalmente abertos e fios.",
        "safety": "Identifique com multimetro os pares internos de cada botao de quatro pernas. Monte sem pilhas. Um botao tact pode ser conectado internamente em pares diferentes conforme o modelo.",
        "steps": [
            "Ligue + ao resistor de 470 ohms, depois ao anodo A do LED.",
            "Ligue o catodo K do LED ao lado A do primeiro botao.",
            "Ligue o lado B do primeiro botao ao lado A do segundo botao.",
            "Ligue o lado B do segundo botao ao polo -.",
            "Coloque as pilhas e alterne os botoes: os dois precisam estar fechados para a corrente passar.",
        ],
        "observe": "A corrente percorre uma unica cadeia apenas quando os dois interruptores fecham. Isto demonstra uma funcao logica AND simples.",
        "real": "No Circuita, clique em cada botao para abrir ou fechar. Em um botao tact real, use os pares corretos de pernas identificados pelo multimetro; os terminais virtuais A/B representam os lados eletricos.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 105, "y": 260, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 290, "y": 260, "resistance": 470.0},
                {"id": 3, "type": "led", "x": 460, "y": 260},
                {"id": 4, "type": "button", "x": 625, "y": 260, "closed": False},
                {"id": 5, "type": "button", "x": 790, "y": 260, "closed": False},
            ],
            "wires": [
                ["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "4:A"],
                ["4:B", "5:A"], ["5:B", "1:-"],
            ],
            "script": "",
        },
    },
    {
        "title": "Modulo 17 - Botoes em paralelo (OU)",
        "goal": "Entender um circuito em que qualquer um de dois botoes pode completar o caminho da corrente.",
        "parts": "Suporte de 3 pilhas AA alcalinas (4,5 V), LED vermelho, resistor de 470 ohms / 1/4 W, dois botoes normalmente abertos e fios.",
        "safety": "Retire as pilhas antes de alterar os fios. Use o resistor em serie com o LED. Identifique os pares de terminais de botoes tact reais com um multimetro.",
        "steps": [
            "Ligue + ao resistor de 470 ohms e depois ao anodo A do LED.",
            "Ligue o catodo K do LED a um lado de cada um dos dois botoes.",
            "Ligue o outro lado dos dois botoes ao polo -; os botoes compartilham os mesmos dois nos.",
            "Coloque as pilhas. Feche o primeiro botao e depois o segundo, testando cada caminho.",
            "Abra ambos: o LED apaga. Qualquer um fechado, sozinho ou junto com o outro, permite a corrente.",
        ],
        "observe": "Basta fechar um dos ramos paralelos para completar o circuito: isso representa uma funcao logica OR simples.",
        "real": "Os botoes estao em paralelo entre o catodo do LED e o polo negativo. Compare com a aula anterior: botoes em serie exigem que todos fechem; em paralelo basta um.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 105, "y": 300, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 295, "y": 300, "resistance": 470.0},
                {"id": 3, "type": "led", "x": 485, "y": 300},
                {"id": 4, "type": "button", "x": 715, "y": 230, "closed": False},
                {"id": 5, "type": "button", "x": 715, "y": 370, "closed": False},
            ],
            "wires": [
                ["1:+", "2:A"], ["2:B", "3:A"],
                ["3:K", "4:A"], ["3:K", "5:A"],
                ["4:B", "1:-"], ["5:B", "1:-"],
            ],
            "script": "",
        },
    },
    {
        "title": "Modulo 18 - Variando a leitura do A0",
        "goal": "Observar como a leitura analogica muda quando a posicao do cursor do potenciometro muda.",
        "parts": "Arduino Uno, potenciometro linear de 10 kohms, fios e computador com USB para usar a placa real.",
        "safety": "Desconecte o USB antes de mudar a fiação. As extremidades do potenciometro vao somente a 5V e GND; o cursor vai a A0. Nunca aplique 9 V ou tensao da tomada a uma entrada do Arduino.",
        "steps": [
            "Ligue uma extremidade do potenciometro a 5V e a outra a GND.",
            "Ligue o cursor W a A0. Confira as ligacoes com o Arduino desconectado.",
            "Conecte o USB e execute READ A0 no Circuita; o ponto inicial esta ajustado para cerca de 25%.",
            "No quadro, selecione o potenciometro e mude Posicao do cursor para 50%; aplique o valor e execute READ A0 de novo.",
            "Repita com 75% e compare as leituras, sempre mantendo 5V como limite maximo da entrada.",
        ],
        "observe": "A leitura devera aumentar conforme o cursor se aproxima de 5V: aproximadamente 256 em 25%, 512 em 50% e 767 em 75%, dependendo de arredondamentos.",
        "real": "O simulador usa um modelo ideal de 10 bits. Uma placa real sofre variacoes, tolerancias e ruido; neste Uno classico, A0 aceita de GND ate a tensao de referencia, normalmente 5V.",
        "project": {
            "components": [
                {"id": 1, "type": "arduino", "x": 245, "y": 245},
                {"id": 2, "type": "potentiometer", "x": 570, "y": 245, "resistance": 10000.0, "wiper": 25.0},
            ],
            "wires": [["1:VCC", "2:B"], ["2:A", "1:GND"], ["2:W", "1:A0"]],
            "script": "READ A0",
        },
    },
    {
        "title": "Modulo 19 - Lei de Ohm e resistor do LED",
        "goal": "Usar a lei de Ohm para estimar a corrente do LED e comparar valores de resistor com seguranca.",
        "parts": "Suporte de 3 pilhas AA alcalinas (4,5 V), LED vermelho, resistores de 220, 330 e 470 ohms / 1/4 W e multimetro (opcional).",
        "safety": "Desconecte as pilhas antes de trocar resistores. Sempre mantenha um resistor em serie com o LED. Use apenas a fonte de 4,5 V especificada nesta aula e componentes em bom estado.",
        "steps": [
            "Monte + -> resistor de 330 ohms -> anodo A do LED -> catodo K -> -.",
            "No Circuita, selecione o resistor, altere o valor e clique em Aplicar valores.",
            "Compare 220, 330 e 470 ohms; use Simular para observar a corrente estimada.",
            "Com uma montagem fisica, retire as pilhas antes de trocar o resistor e repita a montagem.",
            "Calcule cada caso usando I = (Vfonte - VLED) / R; use 2 V como aproximacao inicial para este LED vermelho.",
        ],
        "observe": "Para 4,5 V e Vf de 2 V: 220 ohms dao cerca de 11,4 mA; 330 ohms, 7,6 mA; 470 ohms, 5,3 mA. Aumentar a resistencia reduz a corrente e costuma diminuir o brilho.",
        "real": "O resultado real depende da bateria, da cor e da ficha tecnica do LED. A dissipacao do resistor neste exemplo e baixa para um resistor de 1/4 W. Valores calculados sao estimativas, nao substituem as especificacoes do componente.",
        "project": {
            "components": [
                {"id": 1, "type": "battery", "x": 120, "y": 240, "voltage": 4.5, "format": "AA", "cells": 3},
                {"id": 2, "type": "resistor", "x": 355, "y": 240, "resistance": 330.0},
                {"id": 3, "type": "led", "x": 590, "y": 240},
            ],
            "wires": [["1:+", "2:A"], ["2:B", "3:A"], ["3:K", "1:-"]],
            "script": "",
        },
    },
]


SAFETY_INTRO = (
    "Para todas as aulas: trabalhe somente com pilhas pequenas ou alimentacao USB de baixa tensao, "
    "com um adulto/professor acompanhando criancas. Nunca abra fontes, carregadores ou aparelhos ligados "
    "a tomada; nunca ligue nada da protoboard a rede eletrica. Nao tente recarregar pilhas descartaveis. "
    "Desconecte a fonte antes de alterar fios, "
    "confira a polaridade e pare se algum componente, fio ou pilha aquecer, cheirar estranho ou soltar fumaca. "
    "Em caso de duvida, nao alimente o circuito."
)

BREADBOARD_INTRO = (
    "Dica sobre protoboard: em muitos modelos, grupos de cinco furos de cada lado da canaleta central "
    "sao conectados internamente; a canaleta separa os dois lados. As trilhas de alimentacao podem ser "
    "interrompidas no meio. O desenho muda entre modelos: confira o esquema da sua protoboard e use um "
    "multimetro em continuidade para confirmar antes de ligar a alimentacao."
)
