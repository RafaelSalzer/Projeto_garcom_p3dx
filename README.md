# 🤖 Projeto Garçom Autônomo - Pioneer 3DX

Este projeto implementa um sistema completo de robótica de serviço para restaurantes. Utilizando o **ROS (Robot Operating System)** e o simulador **Gazebo**, o robô **Pioneer 3DX** atua como um garçom autônomo, recebendo pedidos através de uma interface web (tablet) e navegando de forma inteligente, desviando de obstáculos até as mesas.

---

## 📋 Arquitetura do Sistema

O projeto é dividido nos seguintes pacotes principais:

### 📦 `garcom_gazebo`

Contém o ambiente físico 3D do restaurante e o modelo do robô.

### 📦 `garcom_mapping`

Responsável pela geração de mapas utilizando **SLAM (Gmapping)**.

### 📦 `garcom_navigation`

Cérebro da movimentação do robô. Configura:

* **AMCL** (localização)
* **Move Base** (planejamento de rotas)
* Campos de força para evitar colisões

### 📦 `garcom_core`

Contém os scripts Python de alto nível responsáveis por orquestrar toda a lógica de atendimento.

### 🌐 Interface Web

Aplicativo HTML/JavaScript executado no navegador que se comunica com o ROS através de WebSockets.

---

## ⚙️ Pré-requisitos e Instalação

Antes de executar o projeto, certifique-se de possuir:

* Ubuntu com **ROS Noetic** instalado;
* Simulador Gazebo;
* Pacote `rosbridge_suite` para comunicação entre o ROS e a interface web.

### Instalação do Rosbridge

```bash
sudo apt-get install ros-noetic-rosbridge-suite
```

---

# 🚀 Como Executar o Projeto

Para iniciar todo o ecossistema do robô, abra **5 terminais diferentes**.

---

## 🖥️ Terminal 1 — Iniciar o Mundo Físico (Gazebo)

Inicia o ambiente do restaurante e posiciona o robô no cenário.

```bash
roslaunch garcom_gazebo simulacao.launch
```

---

## 🧭 Terminal 2 — Iniciar o Sistema de Navegação

Carrega:

* Mapa estático do ambiente;
* Campos de força das mesas;
* Algoritmo de planejamento de trajetórias.

```bash
roslaunch garcom_navigation navegacao.launch
```

---

## 👀 Terminal 3 — Iniciar o RViz

Abre a interface de visualização do ROS.

```bash
rviz
```

### ⚠️ Etapa Obrigatória

Assim que o RViz abrir:

1. Clique na ferramenta **"2D Pose Estimate"** (botão verde superior);
2. Clique no mapa indicando a posição inicial do robô;
3. Arraste para definir sua orientação.

Essa etapa é fundamental para calibrar corretamente o sistema de localização (**AMCL**).

---

## 📡 Terminal 4 — Iniciar a Comunicação WebSocket

Inicia a ponte de comunicação entre a interface web e o ROS na porta **9090**.

```bash
roslaunch rosbridge_server rosbridge_websocket.launch
```

---

## 🧠 Terminal 5 — Iniciar o Gerenciador de Pedidos

Executa o nó responsável por receber pedidos enviados pela interface web.

```bash
rosrun garcom_core enviar_pedido.py
```

---

# 📱 Utilizando o Tablet do Cliente

Com todos os serviços em execução:

1. Abra o arquivo `interface_garcom.html` utilizando a extensão **Live Server** do VS Code;
2. Na tela inicial, selecione a mesa desejada (ex.: **Mesa 1**);
3. Verifique o campo de IP:

   * Utilize `localhost` para testes locais;
   * Ou informe o IP da máquina na rede;
4. Clique em **Conectar**;
5. Aguarde o botão ficar verde indicando **"SISTEMA ONLINE"**;
6. Clique em **Iniciar Atendimento**.

---

## 🍽️ Fluxo de Atendimento

Após realizar um pedido no cardápio digital, o sistema executará automaticamente as seguintes etapas:

1. Simulação do tempo de preparo da cozinha;
2. Envio do robô ao balcão para retirada do pedido;
3. Espera de alguns segundos para simular o carregamento da refeição;
4. Navegação autônoma até a mesa selecionada;
5. Entrega do pedido ao cliente.

---

## 🎯 Funcionalidades

* ✅ Navegação autônoma com ROS Navigation Stack
* ✅ Localização utilizando AMCL
* ✅ Planejamento de trajetórias com Move Base
* ✅ Desvio de obstáculos em tempo real
* ✅ Integração com interface web
* ✅ Comunicação via WebSockets (Rosbridge)
* ✅ Simulação completa no Gazebo
* ✅ Visualização e monitoramento pelo RViz

---

## 🛠️ Tecnologias Utilizadas

* ROS Noetic
* Gazebo
* RViz
* AMCL
* Move Base
* Gmapping
* Python
* HTML
* CSS
* JavaScript
* Rosbridge Suite

---

## 📌 Observação

O sistema foi desenvolvido para fins acadêmicos e demonstra a integração completa entre simulação robótica, navegação autônoma e interfaces web para aplicações de robótica de serviço.

