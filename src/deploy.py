import glob
import os
import shutil
from distutils.dir_util import copy_tree
from zipfile import ZipFile

# EXCLUDE = ['cache.xml', 'README.md', 'LICENSE']

# Cleanup compile python files. They're useless to AWS
for file in glob.glob("**/*.pyc", recursive=True):
  os.remove(file)

# Setup zip environment
os.mkdir('tmp')
os.mkdir('tmp/libs')
os.mkdir('tmp/res')

# Copy the goods
copy_tree('libs', 'tmp/libs')
copy_tree('res', 'tmp/res')
shutil.copyfile('src/bot.py', 'tmp/bot.py')
shutil.copyfile('src/lambda.py', 'tmp/lambda.py')
os.unlink('tmp/res/cache.xml')  # delete cache. It'll be retrieved from S3

# move cwd to zip environ
os.chdir('tmp')

# Zip the goods
file_paths = []

for root, directories, files, in os.walk('.'):
  for filename in files:
    filepath = os.path.join(root, filename)
    file_paths.append(filepath)

with ZipFile('wheresjaime.zip', 'w') as zip:
  for file in file_paths:
    zip.write(file)

# Move zip up
shutil.move('wheresjaime.zip', '../wheresjaime.zip')

# Move cwd up
os.chdir('..')

# Delete zip environ
shutil.rmtree('tmp')
