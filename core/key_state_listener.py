from pynput import keyboard


class KeyStateListener(keyboard.Listener):
    def __init__(self, target_key):
        super(KeyStateListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.target_key = target_key

    def on_press(self, key):
        if key == self.target_key:
            self.key_pressed = True

    def on_release(self, key):
        if key == self.target_key:
            self.key_pressed = False
