import time
import datetime


class WorkSheet:
    """Класс реализует рабочий табель и интерфейс для взаимодействия с ним"""
    def __init__(self):
        self.start_work_time = 0
        self.start_pause_time = 0
        self.hours_worked = 0
        self.project = None
        self.hourly_rate = 0
        self.count_pause_time = 0
        self.count_work_time = 0
        self.work_status = False
        self.pause_status = False

    async def convert_time(self):
        """Конвертируем секунды в часы и минуты"""
        count_time = await self.get_worked_time_count()
        convert_time = f'*_{count_time // 3600} ч\. {(count_time % 3600) // 60} мин\. {(count_time % 3600) % 60} сек\._*'
        return convert_time

    async def info_string(self):
        info_str = f'Текущий проект: {self.project}\n'
        info_str += f'Отработано за сегодня: {await self.convert_time()}' if self.work_status else ''
        return info_str

    async def start_work(self):
        """Запуск отсчета рабочего времени"""
        if not self.work_status:
            self.start_work_time = time.time()
            self.work_status = True

    async def start_pause(self):
        """Запуск паузы"""
        if self.work_status:
            self.pause_status = True
            self.start_pause_time = time.time()

    async def stop_pause(self):
        """Остановка паузы"""
        if self.work_status:
            self.pause_status = False
            self.count_pause_time += time.time() - self.start_pause_time

    async def stop_work(self):
        """Остановка отсчета рабочего времени, вычет и сброс общего времени паузы"""
        if not self.pause_status:
            self.count_work_time = int(time.time() - self.start_work_time - self.count_pause_time)
        else:
            self.count_work_time = int(time.time() - self.start_work_time - self.count_pause_time - (time.time() - self.start_pause_time))

        self.count_pause_time = 0
        self.work_status = False
        self.pause_status = False
        return f'*_{self.count_work_time // 3600} ч\. {(self.count_work_time % 3600) // 60} мин\. {(self.count_work_time % 3600) % 60} сек\._*'

    async def get_work_status(self):
        """Возвращает статус работы"""
        return self.work_status

    async def get_pause_status(self):
        """Возвращает статус паузы"""
        return self.pause_status

    async def get_worked_time_count(self):
        """Возвращает количество отработанного времени за сегодня на текущий момент"""
        if not self.pause_status:
            return int(time.time() - self.start_work_time - self.count_pause_time)
        else:
            return int(time.time() - self.start_work_time - self.count_pause_time - (time.time() - self.start_pause_time))

work_sheet = WorkSheet()
