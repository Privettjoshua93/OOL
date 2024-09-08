import os
import base64
import mmap

# Generate temporary key
temp_key = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

# Use mmap to store key in RAM (Windows-compatible)
filename = 'dynamic_key'
keys_file_size = 64  # 64 bytes to store the key (32 bytes base64 encoded)

with open(filename, 'wb') as f:
    f.write(b'\0' * keys_file_size)

with open(filename, 'r+b') as f:
    # Memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(), keys_file_size)
    # Write the key to memory
    mm.seek(0)
    mm.write(temp_key.encode('utf-8'))
    mm.seek(0)

print(f"Temporary key written to {filename}. Initialize the app now.")