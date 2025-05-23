import arcade

from config import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE


class SceneManager(arcade.Window):
    def get_clipboard_text(self) -> str:
        pass

    def set_clipboard_text(self, text: str) -> None:
        pass

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.current_scene = None
    
    def change_scene(self, new_scene):
        if self.current_scene:
            pass
        self.current_scene = new_scene
        self.current_scene.setup()
        self.show_view(self.current_scene)
    
    def on_draw(self):
        self.clear()
        pass
        if self.current_scene:
            self.current_scene.on_draw()
    
    def on_update(self, delta_time):
        pass
        if self.current_scene:
            self.current_scene.on_update(delta_time)
    
    def on_key_press(self, key, modifiers):
        pass
        if self.current_scene:
            self.current_scene.on_key_press(key, modifiers)
