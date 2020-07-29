import os
import shutil
import subprocess
import sys
import tempfile

IS_WINDOWS = sys.platform == "win32"


def try_remove_tree(path):
	try:
		if os.path.isdir(path):
			shutil.rmtree(path)
		else:
			os.remove(path)
	except FileNotFoundError:
		pass


def call(args, **kwargs):
	print("running: {}".format(args))
	retcode = subprocess.call(args, shell=IS_WINDOWS, **kwargs) # use shell on windows
	if retcode != 0:
		raise SystemExit(retcode)


def zip(input_path, output_filename):
	try_remove_tree(output_filename)
	call(["7z", "a", output_filename, input_path])


def download(url, output_path):
	# -L makes curl follow redirects
	call(["curl", "-L", url, "-o", output_path])


def create_umineko_script_zip(branch, script_path, output_path):
	temp_folder = tempfile.mkdtemp()

	shutil.copy(script_path, os.path.join(temp_folder, '0.u'))

	# Zip the script
	zip(f'{temp_folder}/*', output_path)

	print(f"Archive saved to: {os.path.abspath(output_path)}")

print(f"Start Umineko Question Build: Python {sys.version}")
print(f"Script running from {os.getcwd()}")



create_umineko_script_zip('master', 'InDevelopment/ManualUpdates/0.utf', 'script-full.7z')
create_umineko_script_zip('voice_only', 'InDevelopment/ManualUpdates/0.utf', 'script-voice-only.7z')
