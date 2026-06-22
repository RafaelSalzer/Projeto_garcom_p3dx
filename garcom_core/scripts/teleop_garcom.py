#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Controle do Robô Garçom - MODO "SEGURE PARA ANDAR"
--------------------------------------------------
Segure a tecla para mover, solte para parar:
        w
   a    s    d

CTRL-C para sair do script
"""

# Adicionamos um parâmetro de 'timeout' na função
def getKey(settings, timeout):
    tty.setraw(sys.stdin.fileno())
    # Aguarda até 'timeout' segundos por um input do teclado
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = '' # Se der o tempo e nada for pressionado, retorna vazio
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('teleop_garcom')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    x = 0.0
    th = 0.0

    try:
        print(msg)
        while not rospy.is_shutdown():
            # Timeout de 0.2 segundos (ideal para evitar "engasgos" da repetição do teclado)
            key = getKey(settings, 0.2)
            
            if key == 'w':
                x = 0.6; th = 0.0
            elif key == 's':
                x = -0.6; th = 0.0
            elif key == 'a':
                x = 0.0; th = 1.0
            elif key == 'd':
                x = 0.0; th = -1.0
            elif key == '\x03': # CTRL+C
                break
            else:
                # Se soltar a tecla (cai no timeout), força os motores a pararem
                x = 0.0
                th = 0.0

            # Publica a velocidade o tempo todo
            twist = Twist()
            twist.linear.x = x
            twist.angular.z = th
            pub.publish(twist)

    except Exception as e:
        print(e)
        
    finally:
        # Medida de segurança final ao fechar o script
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
