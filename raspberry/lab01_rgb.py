import queue
import tkinter as tk


def main():
    import RPi.GPIO as GPIO

    channels = [(7, 31, 'RED', 'red'), (11, 35, 'GREEN', 'green'), (13, 37, 'BLUE', 'blue')]
    events = queue.SimpleQueue()
    states = {button: False for button, *_ in channels}
    root = tk.Tk()
    root.title('Lab 1 - RGB LED')
    root.geometry('900x500')
    label = tk.Label(root, text='Press a hardware button', font=('Arial', 32))
    label.pack(expand=True)

    def on_edge(channel):
        events.put(channel)

    def drain():
        while True:
            try:
                pin = events.get_nowait()
            except queue.Empty:
                break
            for button, led, name, color in channels:
                if button == pin:
                    states[button] = not states[button]
                    GPIO.output(led, states[button])
                    label.config(text=f'{name}: {"ON" if states[button] else "OFF"}', fg=color)
                    print(name, states[button], flush=True)
        root.after(30, drain)

    GPIO.setmode(GPIO.BOARD)
    try:
        for button, led, *_ in channels:
            GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(button, GPIO.RISING, callback=on_edge, bouncetime=25)
        root.after(30, drain)
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
