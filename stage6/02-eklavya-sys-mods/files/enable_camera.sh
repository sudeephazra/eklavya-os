#!/bin/bash

# This script can be used to enable/disable the integrated camera 
# sudo ./enable_camera.sh 0 (Disable the camera interface)
# sudo ./enable_camera.sh 1 (Enable the camera interface)

CONFIG=${ROOTFS_DIR}/boot/config.txt
FLAG=$1

set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end
if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

get_config_var() {
  lua - "$1" "$2" <<EOF
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
for line in file:lines() do
  local val = line:match("^#?%s*"..key.."=(.*)$")
  if (val ~= nil) then
    print(val)
    break
  end
end
EOF
}

# $1 is 0 to disable camera, 1 to enable it
set_camera() {
  # echo "Parameter: $FLAG"
  # Stop if /boot is not a mountpoint
  if ! mountpoint -q ${ROOTFS_DIR}/boot; then
    echo "The /boot folder is not a mountpoint. Exiting..."
    return 1
  fi

  [ -e $CONFIG ] || touch $CONFIG

  if [ "$FLAG" -eq 0 ]; then # disable camera
    echo "Disabling Camera"
    set_config_var start_x 0 $CONFIG
    sed $CONFIG -i -e "s/^startx/#startx/"
    sed $CONFIG -i -e "s/^start_file/#start_file/"
    sed $CONFIG -i -e "s/^fixup_file/#fixup_file/"
  else # enable camera
    echo "Enabling Camera"
    set_config_var start_x 1 $CONFIG
    CUR_GPU_MEM=$(get_config_var gpu_mem $CONFIG)
    if [ -z "$CUR_GPU_MEM" ] || [ "$CUR_GPU_MEM" -lt 128 ]; then
      set_config_var gpu_mem 128 $CONFIG
    fi
    sed $CONFIG -i -e "s/^startx/#startx/"
    sed $CONFIG -i -e "s/^fixup_file/#fixup_file/"
  fi
}

set_camera
