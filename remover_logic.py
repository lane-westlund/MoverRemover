
from camera4kivy import Preview
from threading import Timer
from datetime import datetime
from PIL import Image
import time as time
import numpy as np
import os
from kivy.clock import Clock
from androidstorage4kivy import SharedStorage
from android import autoclass

Environment = autoclass('android.os.Environment')

class RemoverLogic:

    def __init__(self, button, preview, status_text):
        self.capture_button = button
        self.preview = preview
        self.status_text = status_text
        self.save_requested = False
        self.shared = SharedStorage()

        self.capture_button.on_press = self.capture_press

        self.capture_state = "live"

    def connect_camera(self,dt):
        self.preview.connect_camera(filepath_callback=self.file_callback)

    def set_status(self, txt):
        if txt != "":
            txt = f'{len(self.files_list)} Photos\n' + txt
        self.status_text.text = txt

    def file_callback(self, filepath):
        self.capture_state = "processing"
        print("captured " + filepath)
        self.files_list.append(filepath)
        prev = self.get_transformed_image(self.files_list)[0]
        self.preview.make_thread_safe(prev.tobytes('raw', 'RGB'), (prev.width,prev.height))
        self.capture_state = "done"

    def get_transformed_image(self, images_paths):
        print("starting transform")
        self.set_status("processing")
        image_np_arrays = []
        exif_data = None
        exif_bytes = None
        for count, path in enumerate(images_paths):
            self.set_status(f'processing\nImage: {count+1}')
            with Image.open(path) as img:
                if exif_data is None:
                    exif_data = img._getexif()
                    exif_bytes = exif_data and img.info.get('exif') or None
                #img = img.resize(self.size) # TODO, make a paramter for preview or real
                if img.mode == 'RGB':
                    image_np_arrays.append(np.array(img))
                else:
                    image_np_arrays.append(np.array(img.convert('RGB')))
        file_path = images_paths[0][:-7]
        print("save loc: " + file_path)

        print("converting images:" + str(len(image_np_arrays)))

        # Stack the numpy arrays along the 4th (RGBA) axis
        stacked_np_array = np.stack(image_np_arrays, axis=3)

        # Compute the median along the 4th axis
        self.set_status(f'processing\nmedian')
        median_np_array = np.median(stacked_np_array, axis=3)
        self.set_status(f'processing\nmean')
        mean_np_array = np.mean(stacked_np_array, axis=3)

        # Convert the median numpy array back to a PIL Image object
        median_image = Image.fromarray(median_np_array.astype(np.uint8))
        mean_image = Image.fromarray(mean_np_array.astype(np.uint8))

        print("ending transform")
        return median_image, mean_image, exif_bytes, file_path

    def capture_photo(self):
        self.t = Timer(10, self.capture_photo)
        self.t.start()
        self.timer_start = time.time()
        if self.capture_state == "processing":
            self.set_status("processing\ncapture skipped")
            print("process queue overrun, skipping")
            return
        self.set_status("capturing")
        self.capture_state = "capturing"
        file_name = self.file_name_root + f'_{len(self.files_list):03d}'
        print("capturing " + file_name)
        #private: /data/user/0/org.example.slo_cam/files/DCIM/2023_02_22/09_07_17_800882_002.jpg
        self.preview.capture_photo(name=file_name, location='private')


    def stop_photo_capture(self, dt):
        while self.capture_state != "done":
            pass
        median, mean, exif_data, file_save_base = self.get_transformed_image(self.files_list)
        self.set_status("saving")

        # save photos
        median_file = file_save_base + "median.jpg"
        print("saving median: " + median_file)
        median.save(median_file, quality=100, exif=exif_data)

        mean_file = file_save_base + "mean.jpg"
        print("saving mean: " + mean_file)
        mean.save(mean_file, quality=100, exif=exif_data)

        print("moving first:")
        new_name = file_save_base + "first.jpg"
        os.rename(self.files_list[0], new_name)
        self.files_list[0] = new_name
        self.shared.copy_to_shared(self.files_list[0], collection=Environment.DIRECTORY_DCIM)
        print("moving median:")
        self.shared.copy_to_shared(median_file, collection=Environment.DIRECTORY_DCIM)
        print("moving mean:")
        self.shared.copy_to_shared(mean_file, collection=Environment.DIRECTORY_DCIM)

        print("deleting median")
        os.remove(median_file)
        print("deleting mean")
        os.remove(mean_file)

        for file in self.files_list:
            print("deleting " + file)
            os.remove(file)
        self.capture_button.background_normal = 'icons/camera_white.png'
        self.capture_state = "live"
        self.capture_button.disabled = False
        self.set_status("")
        self.preview.live_preview()  # TEST?
        print("stop is done")

    def capture_press(self):
        print("PRESS SEEN")
        if self.capture_state == "live":
            self.files_list = []
            self.capture_start_datetime = datetime.now()
            self.file_name_root = self.capture_start_datetime.strftime('%H_%M_%S_%f')
            self.capture_photo()
        else:
            print("setting red")
            self.t.cancel()
            self.capture_button.disabled = True
            self.capture_button.background_normal = 'icons/camera_red.png'
            Clock.schedule_once(self.stop_photo_capture)
