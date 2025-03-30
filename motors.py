from gpiozero import Motor
motor1=Motor(12,13)
motor2=Motor(18,19)


def motor_forward(s):
    print(f"Fwd {s}")
    motor1.forward(s*1.05)
    motor2.forward(s)

def stop():
    print("Stopped motor")
    motor1.stop()
    motor2.stop()

def motor_backward(s):
    print(f"Bwd {s}")
    motor1.backward(s*1.05)
    motor2.backward(s)


