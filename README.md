# Run with arm64

## Install Miniforge (with default arm64)

```
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
# For Apple Silicon (arm64) builds
source ~/miniforge3/bin/activate
# should show arm64
python -c "import platform; print(platform.machine())"
```

```
conda create -n pc python=3.10
python -m pip install -r requirements.txt
```

```
mkdir build
cd build
cmake .. -DCMAKE_OSX_ARCHITECTURES=arm64
make -j4
```