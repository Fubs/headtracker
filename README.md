# headtracker

nvim plugin to move the cursor with a vive tracker attached to your head


![out](https://user-images.githubusercontent.com/17634481/165172518-e888428e-3566-4839-9132-cf5698a5a3b3.gif)

If you have a vive tracker and want to try it out, here's some (linux) install instructions:
1. install, setup and calibrate libsurvive (including pysurvive): https://github.com/cntools/libsurvive
2. optionally install pygame to use the calibration dot tool
3. clone this repo
4. make the rplugin directory for nvim, and add a link to nvim_headtracker.py 
```
mkdir -p ~/.config/nvim/rplugin/python3
ln -s nvim_headtracker.py ~/.config/nvim/rplugin/python3/nvim_headtracker.py
```

5. open nvim_headtracker.py in nvim, and do :UpdateRemotePlugins
6. use calibration_dot.py to get calibration numbers cx, cy, sx, sy. Edit bg.py and put the new cx, cy, sx, sy into it.
7. put a keybind in your .vimrc to toggle the head tracking cursor on/off. I use the s key:
```
noremap <nowait><silent> s :ToggleTracking<CR>
```
8. run bg.py in the background before starting nvim
