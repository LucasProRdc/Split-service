# 📂 Flask File Splitter & FTP Uploader  

Este projeto é um **web service** desenvolvido com **Flask** que busca um arquivo de um repositório, divide-o em partes menores e envia essas partes para outro repositório via **FTP**.  

## 🚀 Tecnologias Utilizadas  

- **Python** - Linguagem principal  
- **Flask** - Framework para criação da API  
- **Paramiko** - Biblioteca para conexão e envio via FTP
- **Logging** - Para registrar logs detalhados do processo
- **APScheduler** - Para agendamento e automação de tarefas
- **Gunicorn** - Servidor para implantação eficiente em produção

## 🎯 Funcionalidades  

✅ Busca um arquivo de um repositório remoto/local  
✅ Divide arquivos grandes em partes menores  
✅ Envia os arquivos fragmentados para outro repositório via **FTP**  
✅ API REST para controlar o fluxo do processo
✅ Geração de logs detalhados para monitoramento e depuração
✅ Agendamento automático de tarefas com APScheduler
✅ Implantação otimizada utilizando Gunicorn
