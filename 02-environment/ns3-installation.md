# ns-3 Installation (ns-3.48)

> **Purpose**: Install ns-3.48 on Windows + WSL2 (Ubuntu 24.04) for IEEE 802.11be UORA research (mainly using the `wifi` module).
>
> **References**:
> - ns-3 official site: https://www.nsnam.org/
> - Installation Guide: https://www.nsnam.org/docs/installation/
> - Repo: https://gitlab.com/nsnam/ns-3-dev

## Environment

| Item | Version |
|---|---|
| OS | Ubuntu 24.04.4 LTS (WSL2 on Windows) |
| Kernel | 6.18.33.2-microsoft-standard-WSL2 |
| g++ | 13.3.0 |
| CMake | 3.28.3 |
| Python | 3.12.3 |
| ns-3 | ns-3.48 (git tag) |

## Step 0: Install WSL2 + Ubuntu 24.04

Run in PowerShell (as Administrator):

    wsl --install -d Ubuntu-24.04

Troubleshooting:
- If the Ubuntu window does not pop up automatically after reboot, open it manually from the Start menu, or run `wsl` in PowerShell.
- If `wsl` reports "no installed distributions", WSL itself is installed but the Ubuntu download failed. Verify the name with `wsl --list --online`, then re-run the install. If the network is unstable, install via the Microsoft Store instead.
- On first launch, set a UNIX username and password (the screen shows nothing while typing the password, which is normal).

Verify version:

    lsb_release -a
    uname -r

## Step 1: Update package list

    sudo apt update

## Step 2: Install core dependencies

    sudo apt install -y g++ python3 python3-dev cmake ninja-build git ccache

- g++: C++ compiler (requires >= 11)
- cmake + ninja-build: build system
- git: download source, push notes
- ccache: speeds up rebuilds

Verify:

    g++ --version      # 13.3.0
    cmake --version    # 3.28.3
    python3 --version  # 3.12.3

## Step 3: Download the ns-3 source

    cd ~
    mkdir ns3-workspace
    cd ns3-workspace
    git clone https://gitlab.com/nsnam/ns-3-dev.git
    cd ns-3-dev
    git checkout ns-3.48

Troubleshooting:
- If cloning prompts for a GitHub username, the URL was truncated. The ns-3 repo is on GitLab, not GitHub. Cancel, remove the incomplete folder, and paste the full command again.
- The `detached HEAD` message after checkout is normal, not an error.

## Step 4: Configure

    ./ns3 configure --enable-examples --enable-tests

Confirm the wifi module is included:

    ./ns3 show config | grep -i wifi

## Step 5: Build

    ./ns3 build

The first full build takes about 15-40 minutes. Later builds are incremental.

Troubleshooting:
- If it shows `Killed` or hangs, WSL may be out of memory. Increase the WSL memory limit and rebuild.

## Step 6: Verify the installation

    ./ns3 run hello-simulator
    # Output: Hello Simulator          -> ns-3 core works

    ./ns3 run wifi-simple-infra
    # Output: Received one packet!     -> wifi module works

Both checks passed -> ns-3.48 installed successfully, wifi module ready.

## Cheat Sheet

    cd ~/ns3-workspace/ns-3-dev      # enter the ns-3 directory
    ./ns3 build                      # build after editing code
    ./ns3 run <program>              # run a simulation
    ./ns3 run <program> -- --PrintHelp  # list arguments
    ./test.py                        # run the test suite

Put your own scripts in the `scratch/` folder; do not edit `src/` directly.










