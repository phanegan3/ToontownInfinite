import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--panda3d-dir', default='C:/Panda3D-1.9.0',
                    help='The path to the Panda3D build to use for this distribution.')
parser.add_argument('--main-module', default='infinite.base.ClientStartDist',
                    help='The path to the instantiation module.')
parser.add_argument('--build-secret', default='dev',
                    help='The secret that will be used to encrypt the build.')
parser.add_argument('modules', nargs='*', default=['shared', 'infinite'],
                    help='The Toontown Infinite modules to be included in the build.')
args = parser.parse_args()

print 'Building the client...'

os.chdir('build')

cmd = os.path.join(args.panda3d_dir, 'python/ppython.exe')  # ppython
cmd += ' -m direct.showutil.pfreeze'  # pfreeze
args.modules.extend(['direct', 'pandac'])
for module in args.modules:
    cmd += ' -i {0}.*.*'.format(module)
cmd += ' -i {0}.*'.format('encodings')
cmd += ' -i {0}'.format('base64')
cmd += ' -i {0}'.format('site')
cmd += ' -o GameData.pyd'  # The filename of the built *.PYD.
cmd += ' {0}'.format(args.main_module)  # "main" module

os.system(cmd)

# TODO: Replace this simple, temporary cipher with something better:
print 'Encrypting GameData.pyd...'
with open('GameData.pyd', 'rb') as f:
    data = f.read()
cipherData = ''
for i, letter in enumerate(data):
    cipherData += chr(ord(letter) ^ ord(args.build_secret[i%len(args.build_secret)]))
with open('GameData.bin', 'wb') as f:
    f.write(cipherData)
for filename in os.listdir('.'):
    if filename.startswith('GameData') and (not filename.endswith('.bin')):
        os.unlink(filename)

print 'Done building the client.'
