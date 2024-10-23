import webview
import configparser
import os
import time
import json
import shutil

ini_file_path = os.path.join(os.environ['LOCALAPPDATA'], "FortniteGame", "Saved", "Config", "WindowsClient", "GameUserSettings.ini")

class ResolutionAPI:
    def saveResolution(self, width, height):
        try:
            width = int(width)
            height = int(height)
            
            if width <= 0 or height <= 0:
                return "Invalid resolution values. Please enter positive integers."

            self.make_file_writable(ini_file_path)
            config = configparser.ConfigParser()
            config.optionxform = str  # Preserve case sensitivity

            # Read the existing file
            with open(ini_file_path, 'r') as configfile:
                config.read_file(configfile)

            # Update ScalabilityGroups section
            if 'ScalabilityGroups' in config:
                config.set('ScalabilityGroups', 'ResolutionSizeX', str(width))
                config.set('ScalabilityGroups', 'ResolutionSizeY', str(height))

            # Update /Script/FortniteGame.FortGameUserSettings section
            if '/Script/FortniteGame.FortGameUserSettings' in config:
                config.set('/Script/FortniteGame.FortGameUserSettings', 'ResolutionSizeX', str(width))
                config.set('/Script/FortniteGame.FortGameUserSettings', 'ResolutionSizeY', str(height))

            # Write the updated config back to the file
            with open(ini_file_path, 'w') as configfile:
                config.write(configfile)

            self.make_file_readonly(ini_file_path)
            return "Resolution settings saved successfully and file set to read-only!"
        except Exception as e:
            return f"An error occurred while saving the resolution: {str(e)}"

    def make_file_writable(self, file_path):
        try:
            os.chmod(file_path, 0o666)
        except Exception as e:
            print(f"Error making file writable: {str(e)}")

    def make_file_readonly(self, file_path):
        try:
            os.chmod(file_path, 0o444)
        except Exception as e:
            print(f"Error making file read-only: {str(e)}")

    def reset_to_default(self):
        default_width = 1920
        default_height = 1080
        return self.saveResolution(default_width, default_height)

    def check_file_status(self):
        try:
            if os.access(ini_file_path, os.R_OK) and not os.access(ini_file_path, os.W_OK):
                return "Read-only"
            else:
                return "Writable"
        except Exception as e:
            print(f"Error checking file status: {str(e)}")
            return "Unknown"

    def close_window(self):
        window.destroy()

    def move_window(self, delta_x, delta_y):
        current_x, current_y = window.x, window.y
        window.move(current_x + delta_x, current_y + delta_y)


def get_html():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hexa Res - FortniteResolution Editor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        input, select {
            color: black;
            background-color: white;
        }
        input::placeholder {
            color: #888;
        }
    </style>
</head>
<body class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-white transition-colors duration-300">
    <div id="titlebar" class="bg-gray-800 text-white p-2 flex justify-between items-center cursor-move">
        <span>Hexa Res - Resolution Editor</span>
        <div>
            <button id="closeButton" class="px-2 hover:bg-red-500">&times;</button>
        </div>
    </div>
    <div class="container mx-auto px-4 py-8 max-w-3xl">
        <h1 class="text-4xl font-bold mb-8 text-center">Hexa Res</h1>
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
            <div class="mb-6">
                <h2 class="text-xl font-semibold mb-2">Set New Resolution</h2>
                <div class="flex space-x-4">
                    <input type="number" id="width" placeholder="Width" class="w-1/2 p-2 border rounded" style="background-color: white; color: black;">
                    <input type="number" id="height" placeholder="Height" class="w-1/2 p-2 border rounded" style="background-color: white; color: black;">
                </div>
                <p id="aspectRatio" class="mt-2 text-sm text-gray-600 dark:text-gray-400"></p>
            </div>
            <div class="grid grid-cols-3 gap-4 mb-6">
                <button onclick="setResolution(1024, 768)" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">1024×768</button>
                <button onclick="setResolution(1280, 960)" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">1280×960</button>
                <button onclick="setResolution(1440, 1080)" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">1440×1080</button>
            </div>
            <div class="flex space-x-4 mb-6">
                <button onclick="saveResolution()" class="w-1/2 bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded">Save Resolution</button>
                <button onclick="resetToDefault()" class="w-1/2 bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-4 rounded">Reset to Default</button>
            </div>
            <div id="message" class="mt-4 p-4 rounded hidden"></div>
        </div>
    </div>

    <script>
        function setResolution(width, height) {
            document.getElementById('width').value = width;
            document.getElementById('height').value = height;
        }

        function saveResolution() {
            let width = document.getElementById('width').value;
            let height = document.getElementById('height').value;
            window.pywebview.api.saveResolution(width, height).then(response => {
                displayMessage(response);
            });
        }

        function resetToDefault() {
            window.pywebview.api.reset_to_default().then(response => {
                displayMessage(response);
                updateResolutionAndStatus();
            });
        }

        function displayMessage(message) {
            const messageBox = document.getElementById('message');
            messageBox.innerText = message;
            messageBox.classList.remove('hidden');
            setTimeout(() => {
                messageBox.classList.add('hidden');
            }, 4000);
        }

        document.getElementById('closeButton').addEventListener('click', function() {
            window.pywebview.api.close_window();
        });

        // Make the window draggable
        let isDragging = false;
        let startX, startY;

        document.getElementById('titlebar').addEventListener('mousedown', function(e) {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
        });

        document.addEventListener('mousemove', function(e) {
            if (isDragging) {
                const deltaX = e.clientX - startX;
                const deltaY = e.clientY - startY;
                window.pywebview.api.move_window(deltaX, deltaY);
            }
        });

        document.addEventListener('mouseup', function() {
            isDragging = false;
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    api = ResolutionAPI()
    window = webview.create_window('Hexa Res - Resolution Editor', html=get_html(), js_api=api, width=600, height=525, resizable=False, frameless=True)
    webview.start()
