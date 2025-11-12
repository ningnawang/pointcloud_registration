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


## Usage 

Run the script with `src` and `target` meshes in arguments. It would output of the 4x4 **Transformation** matrix (split into 3x3 **Rotation** matrix and 1x3 **Translation** matrix) together with a GUI showing the result. The `target` mesh consideres only the `selected` parts (marked with attribute `vertex_selection` and `face_selection` in the `ply`). 


```
# optional: --samples=20000, default 10000
python open3d_icp.py ../data/mask.obj ../data/max_planck_face.obj 
python open3d_registration_ransac.py ../data/mask.obj ../data/max_planck_face.obj
python open3d_registration_fgr.py ../data/mask.obj ../data/max_planck_face.obj
```