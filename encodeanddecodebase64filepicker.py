import base64
import os
import subprocess  # For clipboard functionality
import tkinter as tk  # For file dialog
from tkinter import filedialog

def encode_file_to_base64(file_path):
    """
    Encodes a file to Base64.

    Args:
        file_path (str): The path to the file to encode.

    Returns:
        str: The Base64 encoded string, or None on error.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            encoded_string = base64.b64encode(file_content).decode('utf-8')  # Decode bytes to string
            return encoded_string
    except Exception as e:
        print(f"An error occurred during encoding: {e}")
        return None

def decode_base64_to_file(base64_string, output_file_path):
    """
    Decodes a Base64 string to a file.

    Args:
        base64_string (str): The Base64 encoded string.
        output_file_path (str): The path to the file to create.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        decoded_content = base64.b64decode(base64_string)
        with open(output_file_path, "wb") as file:
            file.write(decoded_content)
        print(f"File successfully decoded and saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred during decoding: {e}")

def copy_to_clipboard(text):
    """
    Copies the given text to the system's clipboard.

    Args:
        text (str): The text to copy.
    """
    try:
        if os.name == 'nt':  # Windows
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, text.encode('utf-8'))
            win32clipboard.CloseClipboard()
        elif os.name == 'posix':  # Linux/macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)  # Use pbcopy on macOS, xclip on linux
            process.communicate(text.encode('utf-8'))
        else:
            print("Clipboard functionality not supported on this operating system.")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")

def get_file_path():
    """
    Opens a file picker dialog and returns the selected file path.

    Returns:
        str: The path to the selected file, or an empty string if no file
             is selected.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    root.destroy()  # Clean up
    return file_path

def main():
    """
    Main function to run the script.  Prompts the user for input and performs
    encoding or decoding.
    """
    while True:
        print("\nOptions:")
        print("1. Encode file to Base64")
        print("2. Decode Base64 to file")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            # file_path = input("Enter the path to the file to encode: ")
            file_path = get_file_path() # Use file picker
            if not file_path:
                print("No file selected.")
                continue
            if not os.path.exists(file_path):
                print(f"Error: File not found at {file_path}")
                continue  # Go back to the beginning of the loop
            encoded_string = encode_file_to_base64(file_path)
            if encoded_string:
                output_file_name = os.path.basename(file_path) + ".base64"
                output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)
                # save encoded string to a file.
                try:
                    with open(output_file_path, "w") as f:
                        f.write(encoded_string)
                    print(f"Base64 encoded string saved to {output_file_path}")
                except Exception as e:
                    print(f"Error saving encoded string: {e}")
                copy_choice = input("Copy Base64 to clipboard? (y/n): ").lower()
                if copy_choice == 'y':
                    copy_to_clipboard(encoded_string)
                    print("Base64 string copied to clipboard.")

        elif choice == '2':
            base64_string = input("Enter the Base64 encoded string: ")
            output_file_path = input("Enter the path to save the decoded file (e.g., output.txt): ")
            decode_base64_to_file(base64_string, output_file_path)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
