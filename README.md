# Tapo Weather Control

This program is designed to control [Tapo](https://www.tapo.com/) devices (plugs and bulbs) based on weather conditions obtained from [OpenWeatherMap](https://openweathermap.org/) API. It allows you to automate the behavior of the Tapo devices based on cloudiness data retrieved for a specific location.

## Prerequisites

- [Python](https://www.python.org/) 3.7 or higher
- Required Python packages: `PyP100`, `python-dotenv`, `astral`, `schedule`

## Installation

1. Clone or download the repository to your local machine.

2. Install the required Python packages using pip:
```console
pip install PyP100 python-dotenv astral schedule
```

3. Set up the configuration file:

- Rename the file `config_example.env` in the `utils` folder to `config.env`.
- Modify the relevant elements in `config.env` with your own values (API keys, coordinates, Tapo devices, etc.).

## Usage

To run the program, navigate to the main folder and execute the `scheduler.py` file:
```console
python scheduler.py
```

The behavior of the Tapo devices (turning on or off) is determined based on the cloudiness data obtained from OpenWeatherMap API. If the cloudiness percentage exceeds the specified breakpoint in the `config.env` file, the devices will be turned on. Otherwise, they will be turned off.

## Scheduler

The `scheduler.py` file is responsible for scheduling the execution of the Tapo device control based on the specified coordinates and sunset time. Here's how it works:

1. The program retrieves the sunset time for the specified coordinates using the `set_sunset_time()` function.

2. The script determines the range of hours during which it needs to be executed based on the current time and the sunset time using the `get_target_range()` function.

3. It schedules the execution of the `start_control()` function to run 1 minute before every hour within the target range using the `schedule_action()` function.

4. The script enters a loop that continuously checks the current hour and executes the pending scheduled events using the `schedule.run_pending()` function.

5. The program waits until the next hour using the `wait_until_next_hour()` function.

6. Steps 4 and 5 are repeated until the current hour exceeds the last hour within the target range.

7. Finally, the program waits until 1:00 AM and repeats the entire process starting from step 1.

## Customization

- To customize the behavior of the program, modify the values in the configuration file (`config.env`).

## Troubleshooting

- If you encounter any issues or errors, please refer to the program's log file `app.log` for detailed error messages and troubleshooting information.

## Contributions

Contributions to this program are welcome. If you find any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This program is licensed under the [Apache 2.0 License](LICENSE).
