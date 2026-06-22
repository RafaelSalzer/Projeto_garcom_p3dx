#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# Banco de dados das coordenadas do restaurante
# Valores capturados do RViz via /move_base_simple/goal
mesas = {
    "1": {"nome": "Mesa 1", "x": 0.40, "y": 1.52, "z": 0.015, "w": 1.0},
    "2": {"nome": "Mesa 2", "x": 0.48, "y": 0.01, "z": 0.003, "w": 1.0},
    "3": {"nome": "Mesa 3", "x": 0.43, "y": -1.50, "z": -0.01, "w": 1.0},
    "balcao": {"nome": "Balcão (Cozinha)", "x": -1.13, "y": -0.01, "z": -1.0, "w": 0.002}
}

def enviar_robo_para_mesa(id_mesa):
    # Cria o cliente de ação para conversar com o motor de navegação (move_base)
    cliente = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    
    rospy.loginfo("Aguardando o servidor move_base...")
    cliente.wait_for_server()
    
    # Monta a mensagem de destino (Goal) com o formato exigido pelo ROS
    destino = MoveBaseGoal()
    destino.target_pose.header.frame_id = "map"
    destino.target_pose.header.stamp = rospy.Time.now()
    
    # Preenche as coordenadas com os dados do nosso banco de dados
    destino.target_pose.pose.position.x = mesas[id_mesa]["x"]
    destino.target_pose.pose.position.y = mesas[id_mesa]["y"]
    
    # Preenche a orientação (Quatérnio)
    destino.target_pose.pose.orientation.z = mesas[id_mesa]["z"]
    destino.target_pose.pose.orientation.w = mesas[id_mesa]["w"]
    
    rospy.loginfo(f"Enviando o robô para: {mesas[id_mesa]['nome']}")
    cliente.send_goal(destino)
    
    # Trava o script e aguarda o robô chegar fisicamente ao destino
    espera = cliente.wait_for_result()
    
    if not espera:
        rospy.logerr("O servidor falhou ao processar a rota.")
    else:
        resultado = cliente.get_state()
        if resultado == 3: # Estado 3 significa SUCESSO na biblioteca actionlib
            rospy.loginfo(f"Sucesso! O garçom chegou no destino: {mesas[id_mesa]['nome']}")
        else:
            rospy.logwarn("O robô não conseguiu alcançar o destino. Caminho bloqueado?")

if __name__ == '__main__':
    try:
        # Inicia o nó ROS
        rospy.init_node('despacho_pedidos')
        
        while not rospy.is_shutdown():
            print("\n" + "="*40)
            print("        SISTEMA DO ROBÔ GARÇOM")
            print("="*40)
            print("Destinos disponíveis: 1, 2, 3, balcao")
            print("Digite 'sair' para encerrar o sistema.")
            
            escolha = input("\nPara onde o robô deve ir? ").lower().strip()
            
            if escolha == 'sair':
                break
            elif escolha in mesas:
                enviar_robo_para_mesa(escolha)
            else:
                print("Destino inválido! Digite apenas 1, 2, 3 ou balcao.")
                
    except rospy.ROSInterruptException:
        rospy.loginfo("Sistema de despacho encerrado pelo usuário.")
