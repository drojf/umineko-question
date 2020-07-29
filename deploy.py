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


def create_umineko_script_zip(url, output_path):
	temp_folder = tempfile.mkdtemp()

	download(url, os.path.join(temp_folder, '0.u'))

	# Zip the script
	zip(f'{temp_folder}/*', output_path)

	print(f"Archive saved to: {os.path.abspath(output_path)}")



print(f"Start Umineko Question Build: Python {sys.version}")
print(f"Script running from {os.getcwd()}")

create_umineko_script_zip('https://github.com/07th-mod/umineko-question/raw/master/InDevelopment/ManualUpdates/0.utf', './output/script-full.7z')
create_umineko_script_zip('https://github.com/07th-mod/umineko-question/raw/voice_only/InDevelopment/ManualUpdates/0.utf', './output/script-voice-only.7z')

print("contents of .")
for file in os.listdir('.'):
	print(file)

print("contents of output")
for file in os.listdir('./output'):
	print(file)