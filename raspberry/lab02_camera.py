import tkinter as tk
from pathlib import Path
from time import sleep


def main():
    import RPi.GPIO as GPIO
    from PIL import Image, ImageTk
    from picamera2 import Picamera2

    camera = None
    servo = None
    servo_angle = 0
    root = tk.Tk()
    root.title('Spying Eye')
    filename = Path(__file__).resolve().with_name('image.png')
    buttons = tk.Frame(root)
    buttons.pack(padx=10, pady=10)
    picture = tk.Label(root, text='Press TAKE PICTURE', width=100, height=30)
    picture.pack(padx=10, pady=10)

    def set_angle(angle):
        nonlocal servo_angle
        servo_angle = max(0, min(160, angle))
        servo.ChangeDutyCycle(servo_angle / 18 + 2)
        sleep(1)
        servo.ChangeDutyCycle(0)
        print('Angle:', servo_angle, flush=True)

    def left():
        set_angle(servo_angle - 10)

    def right():
        set_angle(servo_angle + 10)

    def take_picture():
        try:
            camera.capture_file(str(filename))
            with Image.open(filename) as captured:
                image = ImageTk.PhotoImage(captured.copy(), master=root)
            picture.config(image=image, text='', width=0, height=0)
            picture.image = image
            print('Saved:', filename, flush=True)
        except Exception as exc:
            print('Camera error:', exc, flush=True)

    tk.Button(buttons, text='LEFT', width=18, command=left).grid(row=0, column=0, padx=5)
    tk.Button(buttons, text='TAKE PICTURE', width=24, command=take_picture).grid(row=0, column=1, padx=5)
    tk.Button(buttons, text='RIGHT', width=18, command=right).grid(row=0, column=2, padx=5)

    GPIO.setmode(GPIO.BOARD)
    try:
        GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
        servo = GPIO.PWM(12, 50)
        servo.start(0)
        camera = Picamera2()
        camera.configure(camera.create_still_configuration(main={'size': (800, 600)}))
        camera.start()
        sleep(1)
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()
    except Exception:
        root.destroy()
        raise
    finally:
        try:
            if camera is not None:
                camera.close()
        finally:
            try:
                if servo is not None:
                    servo.stop()
            finally:
                GPIO.cleanup()


if __name__ == '__main__':
    main()
