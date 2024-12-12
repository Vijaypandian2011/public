import os
import sys
import subprocess

class ProjectSetup:
    def __init__(self, quiet=False, project_path="."):
        """Initialize the project setup with optional quiet mode for logs and a custom project path."""
        self.libraries = []
        self.folders = []
        self.files_in_folders = {}
        self.os_choice = None
        self.activate_script = None
        self.quiet = quiet
        self.project_path = project_path

    def gather_libraries(self):
        """Ask user for Python libraries to install."""
        libraries_input = input("Enter the Python libraries/packages to install (comma-separated): ")
        self.libraries = [lib.strip() for lib in libraries_input.split(',')] if libraries_input else []
    
    def gather_folder_structure(self):
        """Ask user for desired folder structure."""
        folders_input = input("Enter the desired folder structure (comma-separated, e.g., src/, tests/, assets/): ")
        self.folders = [folder.strip() for folder in folders_input.split(',')]
    
    def gather_files_in_folders(self):
        """Ask user for file names to create in each folder."""
        for folder in self.folders:
            files_input = input(f"Enter file names (comma-separated) to create in {folder}: ")
            self.files_in_folders[folder] = [file.strip() for file in files_input.split(',')]

    def gather_os_choice(self):
        """Ask user for the operating system (Windows or Linux)."""
        os_choice = input("Choose your operating system (Windows/Linux): ").lower()
        if os_choice not in ['windows', 'linux']:
            print("Invalid OS choice. Defaulting to Linux.")
            os_choice = 'linux'
        self.os_choice = os_choice
    
    def gather_project_path(self):
        """Ask user for the directory path to set up the project."""
        project_path = input("Enter the path where you want to set up the project (default is current directory): ").strip()
        if not project_path:
            project_path = os.getcwd()  # Default to current working directory
        if not os.path.exists(project_path):
            print(f"The directory {project_path} does not exist. Creating it...")
            os.makedirs(project_path)
        self.project_path = project_path
        print(f"Project will be set up at: {self.project_path}")
    
    def create_virtual_environment(self):
        """Create the virtual environment based on the selected OS."""
        print(f"Creating virtual environment in {self.project_path}...")
        env_path = os.path.join(self.project_path, 'venv')
        if self.os_choice == 'windows':
            subprocess.run(['python', '-m', 'venv', env_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.activate_script = os.path.join(env_path, 'Scripts', 'activate')
        else:
            subprocess.run(['python3', '-m', 'venv', env_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.activate_script = os.path.join(env_path, 'bin', 'activate')
    
    def install_libraries(self):
        """Install the requested libraries in the virtual environment."""
        if self.libraries:
            print(f"Installing the following libraries: {', '.join(self.libraries)}...")
            self._run_pip_install(self.libraries)
        else:
            print("No libraries to install.")
    
    def _run_pip_install(self, packages):
        """Helper function to run pip install with optional quiet mode."""
        install_command = [sys.executable, '-m', 'pip', 'install'] + packages
        if self.quiet:
            # Redirecting output to suppress verbose logs
            subprocess.run(install_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # Running with standard output to show logs
            subprocess.run(install_command, check=True)
    
    def create_folders_and_files(self):
        """Create the requested folder structure and files."""
        for folder in self.folders:
            folder_path = os.path.join(self.project_path, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            for file in self.files_in_folders.get(folder, []):
                file_path = os.path.join(folder_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        f.write(f"# Created file: {file}")
                    print(f"Created file: {file_path}")

    def display_final_instructions(self):
        """Display final instructions to the user."""
        print("\nSetup complete!")
        print(f"To activate your virtual environment, use the following command:")
        print(f"- On Windows: {self.activate_script}")
        print(f"- On Linux: {self.activate_script}")
        print("\nNow you can start working on your Python project.")
    
    def run(self):
        """Run the complete project setup process."""
        print("Welcome to the Python Project Setup Script!")

        # Step 1: Gather project setup details
        self.gather_project_path()
        
        # Step 2: Gather libraries to install
        self.gather_libraries()

        # Step 3: Gather folder structure
        self.gather_folder_structure()

        # Step 4: Gather files in folders
        self.gather_files_in_folders()

        # Step 5: Gather OS choice (Windows/Linux)
        self.gather_os_choice()

        # Step 6: Create the virtual environment
        self.create_virtual_environment()

        # Step 7: Install libraries in virtual environment
        self.install_libraries()

        # Step 8: Create folders and files
        self.create_folders_and_files()

        # Step 9: Display final instructions
        self.display_final_instructions()


if __name__ == "__main__":
    # Set quiet mode based on the argument or use default as False
    quiet_mode = input("Enable quiet mode for installation logs? (y/n): ").lower() == 'y'
    
    setup = ProjectSetup(quiet=quiet_mode)
    setup.run()
