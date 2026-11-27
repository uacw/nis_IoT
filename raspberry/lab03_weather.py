import argparse
import tkinter as tk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=lambda s: int(s, 0), default=0x76)
    args = parser.parse_args()
    import RPi.GPIO as GPIO
    import smbus2

    red, green, blue, alarm = 31, 35, 37, 29
    bus = None
    root = None
    configured_pins = []
    try:
        bus = smbus2.SMBus(1)
        chip_id = bus.read_byte_data(args.address, 0xD0)
        if chip_id == 0x60:
            import bme280

            sensor_name = 'BME280'
            calibration = bme280.load_calibration_params(bus, args.address)

            def read_sensor():
                data = bme280.sample(bus, args.address, calibration)
                return data.temperature, data.pressure, data.humidity

        elif chip_id == 0x58:
            from bmp280 import BMP280

            sensor_name = 'BMP280'
            sensor = BMP280(i2c_addr=args.address, i2c_dev=bus)

            def read_sensor():
                sensor.update_sensor()
                return sensor.temperature, sensor.pressure, None

        else:
            raise RuntimeError(f'Unsupported sensor ID {chip_id:#04x} at {args.address:#04x}.')

        GPIO.setmode(GPIO.BOARD)
        for pin in (red, green, blue, alarm):
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            configured_pins.append(pin)

        root = tk.Tk()
        root.title(f'Lab 3 - Environmental Monitoring ({sensor_name})')
        root.geometry('950x550')
        label = tk.Label(root, justify='left', font=('Arial', 25))
        label.pack(expand=True, padx=20)

        def update():
            try:
                temperature, pressure, humidity = read_sensor()
                mmhg = pressure * 0.750061683
                hot = temperature >= 30
                if pressure >= 1022.69:
                    forecast, rgb = 'Ясно / устойчиво', (True, True, False)
                elif pressure >= 1009.14:
                    forecast, rgb = 'Облачно', (False, True, False)
                else:
                    forecast, rgb = 'Дождливо', (False, False, True)
                for pin, value in zip((red, green, blue), rgb):
                    GPIO.output(pin, value)
                GPIO.output(alarm, hot)
                humidity_text = 'not measured by BMP280' if humidity is None else f'{humidity:.1f} %'
                label.config(text=f'Temperature: {temperature:.1f} C\nHumidity: {humidity_text}\n'
                             f'Pressure: {mmhg:.1f} mmHg ({pressure:.1f} hPa)\n{forecast}\n'
                             f'Over 30 C: {hot}', fg='black')
                print(temperature, humidity_text, mmhg, forecast, flush=True)
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
        if configured_pins:
            GPIO.cleanup(configured_pins)


if __name__ == '__main__':
    main()
