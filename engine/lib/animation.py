from pygame import Vector2, image, rect, surface

class Animation:
    def __init__(self, file_path: str, location: Vector2, fram_with: int, loop: bool=True) -> None:
        self._loop = loop
        self._image_sheet = image.load(file_path)
        self._fram_with = fram_with
        self.location = location
        self._fram_number = self._image_sheet.get_width() / fram_with
        self._current_fram = 1
        self._counter = 0
        self._frequency = 6

    def _get_curren_fram_area(self) -> rect.Rect:
        return rect.Rect(self._current_fram*self._fram_with, 0, self._fram_with, self._image_sheet.get_height())

    def play(self) -> None:
        self._counter += 1
        if self._counter % self._frequency == 0:
            if self._current_fram < self._fram_number:
                self._current_fram += 1
            if self._current_fram % self._fram_number == 0 and self._loop:
                self._current_fram = 1

    def update(self) -> None:
        self.play()

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self._image_sheet, self.location, self._get_curren_fram_area())
