#!/usr/bin/env python3
"""
Boot image extraction and analysis tool for Xiaomi Mi A3 (laurel_sprout)
Extracts kernel, ramdisk, and device tree from Android boot images
"""

import struct
import os
import subprocess
import sys

def extract_boot_image(boot_path, output_dir):
    """
    Extract Android boot image components
    """
    with open(boot_path, 'rb') as f:
        # Read ANDROID! magic
        magic = f.read(8)
        if magic != b'ANDROID!':
            print(f"ERROR: Invalid boot image magic: {magic}")
            return False
        
        # Read header v1 (Android 9+)
        kernel_size = struct.unpack('<I', f.read(4))[0]
        kernel_addr = struct.unpack('<I', f.read(4))[0]
        ramdisk_size = struct.unpack('<I', f.read(4))[0]
        ramdisk_addr = struct.unpack('<I', f.read(4))[0]
        second_size = struct.unpack('<I', f.read(4))[0]
        second_addr = struct.unpack('<I', f.read(4))[0]
        tags_addr = struct.unpack('<I', f.read(4))[0]
        page_size = struct.unpack('<I', f.read(4))[0]
        header_version = struct.unpack('<I', f.read(4))[0]
        os_version = struct.unpack('<I', f.read(4))[0]
        os_patch_level = struct.unpack('<I', f.read(4))[0]
        
        print(f"\n=== BOOT IMAGE ANALYSIS ===")
        print(f"Magic: {magic}")
        print(f"Page size: {page_size}")
        print(f"Header version: {header_version}")
        print(f"OS Version: {os_version >> 11}.{(os_version >> 4) & 0x7F}.{os_version & 0x0F}")
        print(f"Kernel size: {kernel_size} bytes")
        print(f"Ramdisk size: {ramdisk_size} bytes")
        print(f"Second bootloader size: {second_size} bytes")
        print(f"\n=== Addresses ===")
        print(f"Kernel addr: 0x{kernel_addr:08x}")
        print(f"Ramdisk addr: 0x{ramdisk_addr:08x}")
        print(f"Tags addr: 0x{tags_addr:08x}")
        
        # Calculate offsets
        kernel_offset = ((page_size - 1) // page_size + 1) * page_size
        ramdisk_offset = kernel_offset + ((kernel_size + page_size - 1) // page_size) * page_size
        second_offset = ramdisk_offset + ((ramdisk_size + page_size - 1) // page_size) * page_size
        
        # Extract kernel
        f.seek(kernel_offset)
        kernel_data = f.read(kernel_size)
        kernel_path = os.path.join(output_dir, 'kernel')
        with open(kernel_path, 'wb') as kf:
            kf.write(kernel_data)
        print(f"\n✓ Kernel extracted: {kernel_path} ({len(kernel_data)} bytes)")
        
        # Extract ramdisk
        f.seek(ramdisk_offset)
        ramdisk_data = f.read(ramdisk_size)
        ramdisk_path = os.path.join(output_dir, 'ramdisk.cpio.gz')
        with open(ramdisk_path, 'wb') as rf:
            rf.write(ramdisk_data)
        print(f"✓ Ramdisk extracted: {ramdisk_path} ({len(ramdisk_data)} bytes)")
        
        # Try to extract ramdisk contents
        try:
            subprocess.run(['gzip', '-d', ramdisk_path], cwd=output_dir, check=True)
            cpio_path = os.path.join(output_dir, 'ramdisk.cpio')
            ramdisk_out = os.path.join(output_dir, 'ramdisk_extracted')
            os.makedirs(ramdisk_out, exist_ok=True)
            subprocess.run(['cpio', '-iud'], stdin=open(cpio_path, 'rb'), cwd=ramdisk_out, check=True)
            print(f"✓ Ramdisk contents extracted: {ramdisk_out}")
        except Exception as e:
            print(f"⚠ Could not decompress ramdisk: {e}")
        
        return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_boot_img.py <boot.img> [output_dir]")
        sys.exit(1)
    
    boot_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'boot_extract'
    
    os.makedirs(output_dir, exist_ok=True)
    extract_boot_image(boot_path, output_dir)
