# AAIB_projeto
Projeto Alternativo AAIB

Este projeto tem como objetivo adquirir dados do microfone
do computador, extrair features e dispô-las em uma aplicação na cloud, através do Gitpod.

Para se efetuar a comunicação entre o computador e o Gitpod, foi utilizado o Paho MQTT e para mostrar os dados, o Streamlit.

Funcionamento:

1. Corra o ficheiro pub.py localmente e aguarde até se conectar com o MQTT broker.

2. Corra a aplicação através do URL https://gitpod.io/#github.com/gustavoschliemann/AAIB_project

3. Inicie uma gravação. Ao final, os dados de cada gravação são gravados e podem ser baixados com um ficheiro .csv. 