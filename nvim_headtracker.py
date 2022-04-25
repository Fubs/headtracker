import os, math
import pynvim

@pynvim.plugin
class HeadTracker(object):
    def __init__(self, vim):
        self.fifo1 = "/tmp/nvim_tracker_f1"
        self.vim = vim
        self.buf = self.vim.current.buffer
        self.tracking = False
        self.head_x = 0
        self.head_y = 0
        self.cell_cols = self.vim.current.window.width
        self.cell_rows = self.vim.current.window.height
        self.screen_pixels_width = 2560
        self.screen_pixels_height = 1440
        self.cell_width = self.screen_pixels_width / self.cell_cols
        self.cell_height = self.screen_pixels_height / self.cell_rows
        self.next_cmd = None

    @pynvim.command('ToggleTracking', range='', nargs='*', sync=True)
    def toggle_cmd(self, args, range):
        self.tracking = not self.tracking
        self.vim.async_call(self.jump_fn, self.tracking)

    def jump_fn(self, *args):
        while self.tracking:
            with open(self.fifo1, 'r') as f:
                line = f.readline()
                f.close()
            self.head_x = math.floor(float(line.split(',')[0]) / self.cell_width)
            self.head_y = math.floor(float(line.split(',')[1]) / self.cell_height)
            if self.head_x < 0: self.head_x = 0
            if self.head_y < 0: self.head_y = 0
            if self.head_x > self.cell_cols: self.head_x = self.cell_cols
            if self.head_y > self.cell_rows: self.head_y = self.cell_rows
            top_visible = int(self.vim.command_output('echo line("w0")'))
            cursor_line = int(self.vim.command_output('echo line(".")'))
            cursor_col = int(self.vim.command_output('echo col(".")'))
            self.vim.command('echo "Tracking: {} -- {} -- {},{}"'.format(self.tracking, line, self.head_x, self.head_y))
            jumpstr = '^' + 'k'*(cursor_line-top_visible) + 'j'*self.head_y + 'l'*self.head_x
            self.vim.command('normal! ' + jumpstr)
            self.vim.command('redraw!')
