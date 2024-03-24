#!/bin/bash

cd gpu-simulator # change to simulator path
unset -f which # a small bug in our singularity image
# setup CUDA environment
export CUDA_INSTALL_PATH=/usr/local/cuda-11
export PATH=$CUDA_INSTALL_PATH/bin:$CUDA_INSTALL_PATH/targets/x86_64-linux/lib:$PATH
# build GPU simulator (stay in gpu-simulator)
source setup_environment.sh release # requires CUDA-11
mkdir -p build-opt

echo "Building GPU simulator for In-order, log to `pwd`/build-in-order.out"
make clean > /dev/null 2>&1
make -j -B > build-in-order.out 2>&1 # in-order
rm -rf bin/release-in-order build/release-in-order gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-in-order gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-in-order
mv bin/release bin/release-in-order
mv build/release build/release-in-order
mv gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-in-order
mv gpgpu-sim/build/gcc-7.5.0/cuda-11060/release gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-in-order

echo "Building GPU simulator for OoO, log to `pwd`/build-ooo.out"
make clean > /dev/null 2>&1
make OoO_ON=1 -j -B > build-ooo.out 2>&1 # OoO-order
rm -rf bin/release-ooo build/release-ooo gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-ooo gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-ooo
mv bin/release bin/release-ooo
mv build/release build/release-ooo
mv gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-ooo
mv gpgpu-sim/build/gcc-7.5.0/cuda-11060/release gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-ooo

echo "Building GPU simulator for Latency, log to `pwd`/build-ldlat.out"
make clean > /dev/null 2>&1
make printLDSTLatency_ON=1 -j -B > build-ldlat.out 2>&1 # SASS fig 3
rm -rf bin/release-ldlat build/release-ldlat gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-ldlat gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-ldlat
mv bin/release bin/release-ldlat
mv build/release build/release-ldlat
mv gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-ldlat
mv gpgpu-sim/build/gcc-7.5.0/cuda-11060/release gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-ldlat

echo "Building GPU simulator for GhOST Precise, log to `pwd`/build-gp.out"
make clean > /dev/null 2>&1
make OoO_ON=1 GhOSTPrecise_ON=1 -j -B > build-gp.out 2>&1 # SASS GP
rm -rf bin/release-gp build/release-gp gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-gp gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-gp
mv bin/release bin/release-gp
mv build/release build/release-gp
mv gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release gpgpu-sim/lib/gcc-7.5.0/cuda-11060/release-gp
mv gpgpu-sim/build/gcc-7.5.0/cuda-11060/release gpgpu-sim/build/gcc-7.5.0/cuda-11060/release-gp

echo "Show built binaries and libs"
pwd
ls -l bin/
ls -l gpgpu-sim/lib/gcc-7.5.0/cuda-11060/
exit