# Hexa Res - Fortnite Resolution Editor

Hexa Res is a simple, user-friendly application that allows Fortnite players to easily modify their game resolution settings without manually editing configuration files.

## Features

- Set custom resolutions for Fortnite
- Quick preset buttons for common resolutions
- Automatic aspect ratio calculation
- Reset to default resolution (1920x1080)
- Dark mode support
- Frameless window with custom title bar

## How It Works

Hexa Res directly modifies the `GameUserSettings.ini` file located in your Fortnite configuration folder. It updates both the `[ScalabilityGroups]` and `[/Script/FortniteGame.FortGameUserSettings]` sections to ensure compatibility.

## Usage

1. Run the `hexa_res.py` script.
2. Enter your desired width and height in the input fields.
3. Alternatively, use one of the preset resolution buttons.
4. Click "Save Resolution" to apply the changes.
5. Restart Fortnite for the changes to take effect.

## Requirements

- Python 3.6+
- pywebview

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/HH3X4/fortnite-resolution-changer.git
   ```
2. Install the required dependencies:
   ```
   pip install pywebview
   ```
3. Run the script:
   ```
   python hexa_res.py
   ```

## Important Notes

- Always make sure to close Fortnite before changing the resolution.
- The script temporarily makes the configuration file writable to apply changes, then sets it back to read-only.
- Use at your own risk. Modifying game files may violate the game's terms of service.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/HH3X4/fortnite-resolution-changer/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
