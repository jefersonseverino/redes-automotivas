**Projeto da disciplina de redes automotivas** (**IF747**)

Esse projeto consiste em um sistema de detecção de intrusão para uma rede CAN virtual.

Arquivos: 

`data`: Diretório que contém os datasets de treino e de teste com logs CAN.

`models`: Contém modelos treinados de IsolationForest e OCSVM.

`model.py`: Arquivo responsável por treinar o modelo de detecção de anomalias e por avaliar o modelo no conjunto de teste

`listen_and_save.py`: Responsável por ouvir o barramento CAN e salvar os dados para geração de datasets

`listen_and_detect.py`: Responsável por ouvir o barramento CAN, dar como entrada as mensagens CAN para o modelo de detecção e sinalizar anomalias

`attack.py`: Implementação de ataques e mensagens maliciosas na rede CAN. São implementados os ataques de replay, injection, Dos e spoofing.