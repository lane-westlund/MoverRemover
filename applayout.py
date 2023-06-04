from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from remover_preview import RemoverPreview

class AppLayout(FloatLayout):
    remover_preview = ObjectProperty()
        
class ButtonsLayout(RelativeLayout):
    normal = StringProperty()
    down = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            self.normal = 'icons/cellphone-screenshot_white.png'
            self.down   = 'icons/cellphone-screenshot_red.png'
        else:
            self.normal = 'icons/monitor-screenshot_white.png'
            self.down   = 'icons/monitor-screenshot_red.png'
  
    def on_size(self, layout, size):
        if platform == 'android':
            self.ids.camera_button.min_state_time = 0.3
        else:
            self.ids.camera_button.min_state_time = 1
        if Window.width < Window.height:
            self.pos = (0 , 0)
            self.size_hint = (1 , 0.2)
            self.ids.camera_button.pos_hint  = {'center_x':.5,'center_y':.5}
            self.ids.camera_button.size_hint = (.2, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2 , 1)
            self.ids.camera_button.pos_hint  = {'center_x':.5,'center_y':.5}
            self.ids.camera_button.size_hint = (None, .2)


Builder.load_string("""
<AppLayout>:
    remover_preview: self.ids.preview
    capture_button: self.ids.buttons.ids.camera_button
    status_text: self.ids.status
    RemoverPreview:
        aspect_ratio: '4:3'
        id:preview
    ButtonsLayout:
        id:buttons
    Label:
        id: status
        text: ""
        size_hint: None, None
        size: self.texture_size
        pos_hint: {"x": 0, "top": 1}

<ButtonsLayout>:
    normal:
    down:
    Button:
        id:camera_button
        on_press:
        height: self.width
        width: self.height
        background_normal: 'icons/camera_white.png'
        background_down:   'icons/camera_red.png'
        background_disabled_normal: 'icons/camera_red.png'
        background_disabled_down: 'icons/camera_red.png'
""")

            
