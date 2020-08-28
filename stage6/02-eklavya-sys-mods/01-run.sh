#!/bin/bash -e

# Enabling the camera by default
log "Enabling the camera by default"

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

log "Enabling integrated CSI Camera"
set_config_var start_x 1 $CONFIG
CUR_GPU_MEM=$(get_config_var gpu_mem $CONFIG)
if [ -z "$CUR_GPU_MEM" ] || [ "$CUR_GPU_MEM" -lt 128 ]; then
  set_config_var gpu_mem 128 $CONFIG
fi
sed $CONFIG -i -e "s/^startx/#startx/"
sed $CONFIG -i -e "s/^fixup_file/#fixup_file/"
