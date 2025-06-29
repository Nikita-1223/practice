import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import matplotlib.pyplot as plt                                                                                         #type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg                                                         #type: ignore
import time


class Plant:
    def __init__(self, plant_id, x, y):
        self.__id = plant_id
        self.__x = x
        self.__y = y
        self.__radius = random.uniform(5, 15)
        self.__height = random.uniform(1, 5)
        self.__health = 100
        self.__resources = {"light": 0, "water": 0, "nutrients": 0}
        self.__color = "#32CD32"
        self.__growth_rate = 0.05
        self.__aggressiveness = 0.5
        self.__light_pref = "sun"
        self.__max_radius = 50
        self.__max_height = 20
        self.__species = "Растение"
        self.__selected = False

    def get_id(self):
        return self.__id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_radius(self):
        return self.__radius

    def get_height(self):
        return self.__height

    def get_health(self):
        return self.__health

    def get_resources(self):
        return self.__resources

    def get_color(self):
        return self.__color

    def get_species(self):
        return self.__species

    def is_selected(self):
        return self.__selected

    def set_selected(self, value):
        self.__selected = value

    def grow(self, resources):
        self.__resources = resources

        growth_factor = min(
            min(self.__resources["light"], 100) / 100,
            min(self.__resources["water"], 100) / 100,
            min(self.__resources["nutrients"], 100) / 100
        )

        if self.__light_pref == "sun" and self.__resources["light"] < 70:
            growth_factor *= 0.8
        elif self.__light_pref == "shade" and self.__resources["light"] > 80:
            growth_factor *= 0.9

        radius_growth = self.__growth_rate * growth_factor * (self.__max_radius - self.__radius)
        height_growth = self.__growth_rate * growth_factor * (self.__max_height - self.__height)

        self.__radius = min(self.__radius + radius_growth, self.__max_radius)
        self.__height = min(self.__height + height_growth, self.__max_height)

        if growth_factor < 0.5:
            self.__health -= 2
        elif growth_factor > 0.6:
            self.__health = min(100, self.__health + 1)

    def get_info(self):
        return (
            f"Вид: {self.__species}\n"
            f"Радиус: {self.__radius:.1f}/{self.__max_radius}\n"
            f"Высота: {self.__height:.1f}/{self.__max_height}\n"
            f"Здоровье: {int(self.__health)}%\n"
            f"Ресурсы: Свет={min(int(self.__resources['light']), 100)}%, "
            f"Вода={min(int(self.__resources['water']), 100)}%, "
            f"Питание={min(int(self.__resources['nutrients']), 100)}%"
        )


class Tree(Plant):
    def __init__(self, plant_id, x, y):
        super().__init__(plant_id, x, y)
        self._Plant__max_radius = 60
        self._Plant__max_height = 30
        self._Plant__growth_rate = 0.04
        self._Plant__aggressiveness = 0.6
        self._Plant__species = "Дерево"
        self._Plant__color = "#228B22"


class Shrub(Plant):
    def __init__(self, plant_id, x, y):
        super().__init__(plant_id, x, y)
        self._Plant__max_radius = 40
        self._Plant__max_height = 10
        self._Plant__growth_rate = 0.08
        self._Plant__aggressiveness = 0.5
        self._Plant__light_pref = "shade"
        self._Plant__species = "Кустарник"
        self._Plant__color = "#32CD32"


class Flower(Plant):
    def __init__(self, plant_id, x, y):
        super().__init__(plant_id, x, y)
        self._Plant__max_radius = 25
        self._Plant__max_height = 5
        self._Plant__growth_rate = 0.12
        self._Plant__aggressiveness = 0.7
        self._Plant__light_pref = "sun"
        self._Plant__species = "Цветок"
        self._Plant__color = "#FF69B4"


class Fern(Plant):
    def __init__(self, plant_id, x, y):
        super().__init__(plant_id, x, y)
        self._Plant__max_radius = 35
        self._Plant__max_height = 8
        self._Plant__growth_rate = 0.09
        self._Plant__aggressiveness = 0.4
        self._Plant__light_pref = "shade"
        self._Plant__species = "Папоротник"
        self._Plant__color = "#20B2AA"


class Environment:
    def __init__(self, width, height, num_plants):
        self.__width = width
        self.__height = height
        self.__plants = []
        self.__dead_plants_count = 0
        self.__resource_map = {
            "water": np.ones((width, height)) * 150.0,
            "nutrients": np.ones((width, height)) * 150.0
        }
        self.__light_map = np.ones((width, height)) * 100.0
        self.__day_night_cycle = 0
        self.__rain_probability = 0.15
        self.__raining = False
        self.__rain_end_time = 0

        min_margin = 50

        plant_types = [Tree, Shrub, Flower, Fern]
        for i in range(num_plants):
            plant_class = random.choice(plant_types)
            x = random.randint(min_margin, width - min_margin)
            y = random.randint(min_margin, height - min_margin)
            self.__plants.append(plant_class(i, x, y))

    def get_plants(self):
        return self.__plants

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_day_night_cycle(self):
        return self.__day_night_cycle

    def is_raining(self):
        return self.__raining

    def get_dead_plants_count(self):
        return self.__dead_plants_count

    def update_resources(self):
        self.__day_night_cycle = (self.__day_night_cycle + 1) % 24
        daylight = 100 if 6 <= self.__day_night_cycle <= 20 else 10
        self.__light_map = np.ones((self.__width, self.__height)) * daylight

        if random.random() < self.__rain_probability and not self.__raining:
            self.__raining = True
            self.__rain_end_time = time.time() + 3
            rain_amount = random.uniform(20, 40)
            self.__resource_map["water"] = np.minimum(
                np.maximum(self.__resource_map["water"] + rain_amount, 0), 200
            )

        if self.__raining and time.time() > self.__rain_end_time:
            self.__raining = False

        self.__resource_map["water"] = np.minimum(
            np.maximum(self.__resource_map["water"] - 0.5, 0), 200
        )
        self.__resource_map["nutrients"] = np.minimum(
            np.maximum(self.__resource_map["nutrients"] + 0.8, 0), 200
        )

        self.__calculate_shading()

        for plant in self.__plants:
            resources = self.__get_plant_resources(plant)
            plant.grow(resources)

    def __calculate_shading(self):
        sorted_plants = sorted(self.__plants, key=lambda p: p.get_height(), reverse=True)

        shade_mask = np.zeros((self.__width, self.__height), dtype=bool)

        for plant in sorted_plants:
            x, y, r = plant.get_x(), plant.get_y(), plant.get_radius()

            x_min = max(0, int(x - r * 2))
            x_max = min(self.__width, int(x + r * 2))
            y_min = max(0, int(y - r * 2))
            y_max = min(self.__height, int(y + r * 2))

            if x_min >= x_max or y_min >= y_max:
                continue

            x_grid, y_grid = np.meshgrid(
                np.arange(x_min, x_max),
                np.arange(y_min, y_max),
                indexing='ij'
            )

            dist = np.sqrt((x_grid - x) ** 2 + (y_grid - y) ** 2)

            under_plant = dist <= r

            effective_area = under_plant & ~shade_mask[x_min:x_max, y_min:y_max]

            shade_factor = 0.7 if plant.get_height() > 10 else 0.9
            self.__light_map[x_min:x_max, y_min:y_max][effective_area] *= shade_factor

            shade_mask[x_min:x_max, y_min:y_max] |= under_plant

    def __get_plant_resources(self, plant):
        x, y, r = plant.get_x(), plant.get_y(), plant.get_radius()

        x_min = max(0, int(x - r))
        x_max = min(self.__width, int(x + r))
        y_min = max(0, int(y - r))
        y_max = min(self.__height, int(y + r))

        if x_min >= x_max or y_min >= y_max:
            return {"light": 0, "water": 0, "nutrients": 0}

        light_area = self.__light_map[x_min:x_max, y_min:y_max]
        water_area = self.__resource_map["water"][x_min:x_max, y_min:y_max]
        nutrients_area = self.__resource_map["nutrients"][x_min:x_max, y_min:y_max]

        avg_light = np.mean(light_area) if light_area.size > 0 else 0
        avg_water = np.mean(water_area) if water_area.size > 0 else 0
        avg_nutrients = np.mean(nutrients_area) if nutrients_area.size > 0 else 0

        consumption_factor = plant._Plant__aggressiveness * 0.03
        self.__resource_map["water"][x_min:x_max, y_min:y_max] *= (1 - consumption_factor)
        self.__resource_map["nutrients"][x_min:x_max, y_min:y_max] *= (1 - consumption_factor)

        return {
            "light": avg_light,
            "water": avg_water,
            "nutrients": avg_nutrients
        }

    def remove_dead_plants(self):
        dead_count = 0
        new_plants = []
        for p in self.__plants:
            if p.get_health() > 0:
                new_plants.append(p)
            else:
                dead_count += 1
        self.__plants = new_plants
        self.__dead_plants_count += dead_count


class PlantCommunityApp:
    def __init__(self, root):
        self.__root = root
        self.__root.title("Моделирование растительных сообществ")
        self.__root.geometry("1100x700")
        self.__root.minsize(900, 600)

        self.__width = 700
        self.__height = 500
        self.__num_plants = random.randint(15, 25)
        self.__environment = Environment(self.__width, self.__height, self.__num_plants)
        self.__selected_plant = None
        self.__rain_effect_end = 0
        self.__original_bg = '#e8f5e9'

        self.__setup_ui()
        self.__simulation_running = True
        self.__simulation_speed = 1.0

        self.__update_simulation()

        self.__root.protocol("WM_DELETE_WINDOW", self.__on_close)

    def __on_close(self):
        self.__simulation_running = False
        self.__root.destroy()

    def __setup_ui(self):
        main_frame = ttk.Frame(self.__root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="▶ Старт", command=self.__start_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⏸ Пауза", command=self.__stop_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⟳ Перезапуск", command=self.__restart_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📊 Статистика", command=self.__show_stats).pack(side=tk.LEFT, padx=5)

        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(speed_frame, text="Скорость симуляции:").pack(side=tk.LEFT)
        self.__speed_scale = ttk.Scale(
            speed_frame, from_=0.1, to=5.0, value=1.0, length=150,
            command=lambda v: setattr(self, '_PlantCommunityApp__simulation_speed', float(v))
        )
        self.__speed_scale.pack(side=tk.LEFT, padx=5)

        self.__time_label = ttk.Label(
            control_frame,
            text=f"Время: {self.__environment.get_day_night_cycle():02d}:00",
            font=('Arial', 10, 'bold')
        )
        self.__time_label.pack(side=tk.RIGHT, padx=10)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        canvas_frame = ttk.LabelFrame(content_frame, text="Растительное сообщество", padding=10)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.__canvas = tk.Canvas(canvas_container, bg=self.__original_bg, width=self.__width, height=self.__height)
        self.__canvas.pack(fill=tk.BOTH, expand=True)

        info_frame = ttk.LabelFrame(content_frame, text="Информация", padding=10)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        notebook = ttk.Notebook(info_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        plant_tab = ttk.Frame(notebook, padding=10)
        notebook.add(plant_tab, text="Растение")

        self.__info_text = tk.StringVar()
        self.__info_text.set("Выберите растение для просмотра информации")
        info_label = ttk.Label(plant_tab, textvariable=self.__info_text, wraplength=250, justify=tk.LEFT)
        info_label.pack(fill=tk.X)

        stats_tab = ttk.Frame(notebook, padding=10)
        notebook.add(stats_tab, text="Статистика")

        stats_container = ttk.Frame(stats_tab)
        stats_container.pack(fill=tk.BOTH, expand=True)

        self.__stats_label = tk.Text(stats_container, wrap=tk.WORD, font=('Arial', 10), height=15)
        self.__stats_label.pack(fill=tk.BOTH, expand=True)
        self.__stats_label.config(state=tk.DISABLED)

        self.__update_stats_text()

    def __update_stats_text(self):
        plants = self.__environment.get_plants()
        plant_count = len(plants)
        avg_health = sum(p.get_health() for p in plants) / plant_count if plant_count else 0

        type_count = {"Дерево": 0, "Кустарник": 0, "Цветок": 0, "Папоротник": 0}
        for plant in plants:
            species = plant.get_species()
            if species in type_count:
                type_count[species] += 1

        stats = (
            f"Всего растений: {plant_count}\n"
            f"Погибло растений: {self.__environment.get_dead_plants_count()}\n\n"
            f"Типы растений:\n"
            f"- Деревья: {type_count['Дерево']}\n"
            f"- Кустарники: {type_count['Кустарник']}\n"
            f"- Цветы: {type_count['Цветок']}\n"
            f"- Папоротники: {type_count['Папоротник']}\n\n"
            f"Среднее здоровье: {avg_health:.1f}%\n"
            f"Время суток: {'День' if 6 <= self.__environment.get_day_night_cycle() <= 20 else 'Ночь'}\n"
            f"Цикл: {self.__environment.get_day_night_cycle():02d}:00\n"
            f"Погода: {'Дождь' if self.__environment.is_raining() else 'Ясно'}"
        )

        self.__stats_label.config(state=tk.NORMAL)
        self.__stats_label.delete(1.0, tk.END)
        self.__stats_label.insert(tk.END, stats)
        self.__stats_label.config(state=tk.DISABLED)

    def __draw_plants(self):
        self.__canvas.delete("all")

        for plant in self.__environment.get_plants():
            x, y, r = plant.get_x(), plant.get_y(), plant.get_radius()

            if x - r < 0 or x + r > self.__width or y - r < 0 or y + r > self.__height:
                plant._Plant__x = max(r + 10, min(self.__width - r - 10, x))
                plant._Plant__y = max(r + 10, min(self.__height - r - 10, y))
                x, y = plant.get_x(), plant.get_y()

            if plant.get_health() > 70:
                color = plant.get_color()
            elif plant.get_health() > 40:
                color = "#FFA500"
            else:
                color = "#FF0000"

            self.__canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline="#333", width=1, tags=f"plant_{plant.get_id()}"
            )

            self.__canvas.create_text(
                x, y, text=plant.get_species()[0],
                fill="white", font=("Arial", 10, "bold"), tags=f"plant_{plant.get_id()}"
            )

        for plant in self.__environment.get_plants():
            self.__canvas.tag_bind(
                f"plant_{plant.get_id()}", "<Button-1>",
                lambda e, p=plant: self.__show_plant_info(p)
            )

        self.__time_label.config(text=f"Время: {self.__environment.get_day_night_cycle():02d}:00")

        if self.__environment.is_raining():
            self.__canvas.config(bg="#87CEEB")
            self.__rain_effect_end = time.time() + 0.3
        elif time.time() > self.__rain_effect_end:
            self.__canvas.config(bg=self.__original_bg)

    def __show_plant_info(self, plant):
        for p in self.__environment.get_plants():
            p.set_selected(False)

        plant.set_selected(True)
        self.__selected_plant = plant
        self.__info_text.set(plant.get_info())

    def __update_simulation(self):
        if self.__simulation_running:
            try:
                self.__environment.update_resources()
                self.__environment.remove_dead_plants()
                self.__draw_plants()
                self.__update_stats_text()
                self.__root.after(int(300 / self.__simulation_speed), self.__update_simulation)
            except tk.TclError:
                pass

    def __start_simulation(self):
        if not self.__simulation_running:
            self.__simulation_running = True
            self.__update_simulation()

    def __stop_simulation(self):
        self.__simulation_running = False

    def __restart_simulation(self):
        self.__stop_simulation()
        self.__environment = Environment(self.__width, self.__height, random.randint(15, 25))
        self.__selected_plant = None
        self.__info_text.set("Выберите растение для просмотра информации")
        self.__draw_plants()
        self.__update_stats_text()
        self.__simulation_running = True

    def __show_stats(self):
        stats_window = tk.Toplevel(self.__root)
        stats_window.title("Статистика растительного сообщества")
        stats_window.geometry("800x600")
        stats_window.minsize(600, 400)

        main_frame = ttk.Frame(stats_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        species_frame = ttk.Frame(notebook)
        self.__add_species_stats(species_frame)
        notebook.add(species_frame, text="Виды растений")

        health_frame = ttk.Frame(notebook)
        self.__add_health_stats(health_frame)
        notebook.add(health_frame, text="Здоровье растений")

    def __add_species_stats(self, frame):
        type_count = {"Дерево": 0, "Кустарник": 0, "Цветок": 0, "Папоротник": 0}
        for plant in self.__environment.get_plants():
            species = plant.get_species()
            if species in type_count:
                type_count[species] += 1

        if sum(type_count.values()) == 0:
            ttk.Label(frame, text="Нет растений для отображения").pack()
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        types = list(type_count.keys())
        counts = list(type_count.values())

        colors = ["#228B22", "#32CD32", "#FF69B4", "#20B2AA"]

        bars = ax.bar(types, counts, color=colors)
        ax.set_title("Распределение типов растений")
        ax.set_ylabel("Количество")

        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.2)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def __add_health_stats(self, frame):
        plants = self.__environment.get_plants()
        if not plants:
            ttk.Label(frame, text="Нет растений для отображения").pack()
            return

        health_data = [p.get_health() for p in plants]
        type_health = {"Дерево": [], "Кустарник": [], "Цветок": [], "Папоротник": []}

        for plant in plants:
            species = plant.get_species()
            if species in type_health:
                type_health[species].append(plant.get_health())

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.suptitle("Здоровье растений")

        ax1.hist(health_data, bins=[0, 20, 40, 60, 80, 100], color='#2E8B57', edgecolor='black')
        ax1.set_title("Распределение здоровья")
        ax1.set_xlabel("Уровень здоровья (%)")
        ax1.set_ylabel("Количество")
        ax1.grid(True, alpha=0.3)

        types = [t for t in type_health.keys() if type_health[t]]
        avg_health = [np.mean(type_health[t]) for t in types]
        colors = ["#228B22", "#32CD32", "#FF69B4", "#20B2AA"]

        bars = ax2.bar(types, avg_health, color=colors[:len(types)])
        ax2.set_title("Среднее здоровье по типам")
        ax2.set_ylabel("Среднее здоровье (%)")
        ax2.set_ylim(0, 100)

        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f'{height:.1f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')

        plt.tight_layout(pad=2.0)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = PlantCommunityApp(root)
    root.mainloop()