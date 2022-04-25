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
        if self.tracking: self.vim.async_call(self.jump_fn, self.tracking)

    def jump_fn(self, *args):
        if not os.path.exists(self.fifo1):
            self.vim.command("echo 'fifo file not found, bg script not running?'")
            return
        f = open(self.fifo1, 'r')
        while self.tracking:
            line = f.readline()
            self.head_x = math.floor(float(line.split(',')[0]) / self.cell_width)
            self.head_y = math.floor(float(line.split(',')[1]) / self.cell_height)

            if self.head_y < 0: 
                self.vim.command('normal! k') #scroll up a line if at top
                self.head_y = 0
            if self.head_y > self.cell_rows:
                self.vim.command('normal! j') #scroll down a line if at bottom
                self.head_y = self.cell_rows

            if self.head_x < 0: self.head_x = 0
            if self.head_x > self.cell_cols: self.head_x = self.cell_cols

            top_visible_line = int(self.vim.command_output('echo line("w0")'))
            self.vim.command('echo "Tracking: {} -- {} -- {},{}"'.format(self.tracking, line, self.head_x, self.head_y))
            jumpstr = str(top_visible_line+self.head_y) + 'G' + str(self.head_x) + '|'
            self.vim.command('normal! ' + jumpstr)
        f.close()
