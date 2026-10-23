# Circuita

Circuita e um prototipo desktop open source para desenhar e testar circuitos eletricos didaticamente. O projeto usa Python e Tkinter, ambos sem dependencias de terceiros para executar o aplicativo.

## Requisitos

- Python 3.10 ou mais recente
- Tkinter (normalmente incluido na instalacao de Python para Windows)

## Como executar

No Windows, abra um terminal nesta pasta e execute:

```powershell
py main.py
```

Se o comando `py` nao estiver disponivel:

```powershell
python main.py
```

## Como gerar o executavel Windows

Com Python instalado, execute `build_exe.bat` na pasta do projeto. O script instala o PyInstaller se necessario e compila o app em modo janela, sem abrir um console separado. O arquivo resultante fica em:

```text
dist\Circuita.exe
```

O executavel e para Windows. O primeiro inicio pode demorar alguns segundos enquanto os arquivos sao preparados. Para distribuir, envie o executavel junto com as instrucoes de seguranca deste projeto.

## Creditos

Desenvolvimento: **@Hikaru_Labs** no [Instagram](https://www.instagram.com/Hikaru_Labs/).

## Primeiro teste

1. Clique em **Manual** e escolha uma das aulas praticas.
2. Leia os materiais e a secao de seguranca antes de montar qualquer circuito real.
3. Clique em **Montar projeto da aula** para colocar o circuito correspondente no quadro.
4. Siga as ligacoes numeradas. A fonte real deve ficar desconectada enquanto os fios sao alterados.
5. Use **Simular** para observar o modelo e **Salvar** para guardar o projeto `.circuita`.
6. Na biblioteca esquerda, role a roda do mouse mesmo quando o ponteiro estiver sobre um botao; a barra lateral tambem pode ser arrastada.

O manual dentro do aplicativo contem estes projetos:

1. LED (que ja e um tipo de diodo), resistor e suporte de tres pilhas AA (4,5 V). Nao se adiciona um segundo diodo a esta aula.
2. Botao liga/desliga em serie com o LED.
3. Carga de capacitor atraves de resistor, com verificacao por multimetro.
4. Potenciometro como divisor de tensao na entrada analogica A0.
5. LED com resistor controlado pelo pino D13 do Arduino Uno.
6. Tela LCD 16x2 por I2C.
7. Buzzer ativo de baixa tensao.
8. Motor DC de 3 V com diodo de protecao.
9. Lampada incandescente de lanterna de 3 V, em soquete e com supervisao adulta.
10. Resistores em serie e divisao de tensao.
11. Resistores em paralelo e divisao de corrente.
12. LEDs em paralelo com resistores independentes.
13. LEDs em serie.
14. Diodo retificador, anodo, catodo e conducao.
15. Polaridade do LED e tensao reversa segura.
16. Botoes em serie e logica AND.
17. Botoes em paralelo e logica OR.
18. Potenciometro e diferentes leituras analogicas em A0.
19. Lei de Ohm e escolha do resistor limitador de LED.
10. Dois resistores em serie e divisao de tensao.
11. Resistores em paralelo e corrente nos ramos.
12. Dois LEDs em paralelo, cada um com resistor proprio.
13. Dois LEDs em serie.
14. Diodo retificador, anodo, catodo e polaridade.
15. LED invertido e limites de tensao reversa.
16. Dois botoes em serie: logica AND.
17. Dois botoes em paralelo: logica OR.
18. Potenciometro e leitura analogica em diferentes posicoes.
19. Lei de Ohm e comparacao de resistores para LED.

As instrucoes identificam explicitamente quais partes do projeto sao apenas representacoes do simulador e quais necessitam de uma placa ou componente real. O comando de teste rapido do Circuita nao envia codigo para um Arduino conectado.

## Seguranca eletrica

- Estes projetos sao para ensino com pilhas pequenas ou USB de baixa tensao e supervisao adulta quando houver criancas.
- Nunca ligue protoboard, componente, pilha ou Arduino a uma tomada, fio residencial ou fonte de tensao desconhecida.
- Desconecte a alimentacao antes de mover fios e confira valores, polaridade e fichas tecnicas dos componentes reais.
- Use resistor em serie com LED. Nao ligue LED diretamente a uma pilha, conjunto de pilhas ou pino de saida.
- O LED e um diodo emissor de luz. O componente separado "Diodo" da biblioteca e usado em outra aula; nao o acrescente ao projeto do modulo 1.
- Capacitores eletroliticos sao polarizados: respeite o terminal negativo marcado e descarregue atraves de resistor, nao por curto.
- Nunca ligue motor diretamente a um pino de saida do Arduino. E necessario um estagio driver dimensionado para o motor.
- Interrompa imediatamente o teste se qualquer componente, fio ou pilha aquecer, apresentar cheiro ou fumaca.

## Comandos do teste rapido

O painel aceita um comando por linha:

```text
DIGITAL_WRITE 13 HIGH
DISPLAY Oi, circuito!
READ A0
WAIT 1000
```

- `DIGITAL_WRITE 13 HIGH|LOW`: controla o pino D13 do Arduino Uno.
- `DISPLAY texto`: escreve ate 32 caracteres na primeira tela LCD.
- `READ A0`: mede a tensao do pino analogico e informa o valor equivalente de 0 a 1023.
- `WAIT ms`: registra uma espera logica, sem bloquear a interface.
- Linhas iniciadas com `#` sao ignoradas.

O editor nao executa codigo Python arbitrario. Isso mantem os testes limitados aos comandos suportados.

## Pilhas A, AA e AAA

**A, AA e AAA sao formatos/tamanhos de pilhas individuais**. No Circuita, o componente da biblioteca e chamado **Pilha / conjunto**: ele representa uma pilha ou um suporte/conjunto de pilhas ligadas em serie. Escolha o tamanho de cada pilha e a quantidade em serie. Neste modelo didatico, cada pilha alcalina contribui 1,5 V nominais: 3 pilhas AA, por exemplo, formam um conjunto de 4,5 V. O tamanho fisico nao altera a tensao nominal. Pilhas recarregaveis NiMH normalmente sao 1,2 V por celula, e pilhas reais variam durante a descarga; confira sempre a embalagem. A selecao de formato serve para identificar o modelo e nao garante compatibilidade mecanica com qualquer suporte real.

## Componentes disponiveis

Pilha ou conjunto de pilhas em serie (formato A, AA ou AAA), resistor, capacitor, LED, diodo, botao, tela LCD, Arduino Uno, potenciometro, buzzer, motor DC e lampada. Resistencias, quantidade e formato das pilhas, queda direta de diodos/LEDs e posicao do cursor do potenciometro podem ser editados no painel de propriedades. Os componentes podem ser arrastados, ligados por seus terminais, removidos com **Delete** e guardados em projetos JSON `.circuita`.

## Limites atuais

A simulacao eletrica e uma aproximacao DC didatica: resistores, fontes com pequena resistencia interna, LED/diodo por modelo linear simplificado, potenciometro, lampada, buzzer, motor DC e botao aberto/fechado. Capacitores aparecem e podem ser configurados, mas ainda nao ha simulacao temporal de carga/descarga. A placa Arduino e um modelo visual simplificado com alimentacao de 5 V, pinos D13/A0/A4/A5 e um modelo de entrada analogica de alta impedancia. A tela LCD 16x2 mostra `DISPLAY`, mas o app nao interpreta bibliotecas nem executa firmware Arduino. A biblioteca pode ser rolada para acessar todos os componentes.

Este prototipo nao substitui ferramentas de engenharia eletronica nem validacao de hardware real. Verifique os calculos antes de montar circuitos fisicos.
