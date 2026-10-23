import argparse
import tkinter as tk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=lambda s: int(s, 0), default=0x76)
    args = parser.parse_args()
    import RPi.GPIO as GPIO
    import smbus2
    import bme280

    red, green, blue, alarm = 31, 35, 37, 29
    bus = None
    root = None
    GPIO.setmode(GPIO.BOARD)
    try:
        bus = smbus2.SMBus(1)
        chip_id = bus.read_byte_data(args.address, 0xD0)
        if chip_id != 0x60:
            raise RuntimeError(f'Expected BME280 (chip ID 0x60), got {hex(chip_id)}. '
                               'BMP280 cannot measure humidity; obtain BME280 or agree a substitution.')
        calibration = bme280.load_calibration_params(bus, args.address)
        for pin in (red, green, blue, alarm):
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        root = tk.Tk()
        root.title('Lab 3 - Environmental Monitoring')
        root.geometry('950x550')
        label = tk.Label(root, justify='left', font=('Arial', 25))
        label.pack(expand=True, padx=20)

        def update():
            try:
                data = bme280.sample(bus, args.address, calibration)
                pressure = data.pressure
                mmhg = pressure * 0.750061683
                hot = data.temperature >= 30
                if pressure >= 1022.69:
                    forecast, rgb = 'Ясно / устойчиво', (True, True, False)
                elif pressure >= 1009.14:
                    forecast, rgb = 'Облачно', (False, True, False)
                else:
                    forecast, rgb = 'Дождливо', (False, False, True)
                for pin, value in zip((red, green, blue), rgb):
                    GPIO.output(pin, value)
                GPIO.output(alarm, hot)
                label.config(text=f'Temperature: {data.temperature:.1f} C\nHumidity: {data.humidity:.1f} %\n'
                             f'Pressure: {mmhg:.1f} mmHg ({pressure:.1f} hPa)\n{forecast}\n'
                             f'Over 30 C: {hot}', fg='black')
                print(data.temperature, data.humidity, mmhg, forecast, flush=True)
            except Exception as exc:
                for pin in (red, green, blue, alarm):
                    GPIO.output(pin, GPIO.LOW)
                label.config(text=f'Sensor error: {exc}', fg='red')
            root.after(1000, update)

        root.after(100, update)
        root.mainloop()
    except KeyboardInterrupt:
        if root is not None:
            root.destroy()
    finally:
        if bus is not None:
            bus.close()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
