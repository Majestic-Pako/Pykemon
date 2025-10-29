import pygame
import json

class Pokemon:
    def __init__(self, nombre_pokemon, nivel=5, pokemon_data=None):
        # Cargar datos base si no se proveen
        if pokemon_data is None:
            with open("data/pokemon.json", "r", encoding="utf-8") as f:
                todos_pokemon = json.load(f)
                pokemon_data = next(p for p in todos_pokemon if p["nombre"] == nombre_pokemon)
        
        # Datos permanentes
        self.nombre = pokemon_data["nombre"]
        self.tipos = pokemon_data["tipos"]
        self.sprite = pokemon_data["sprite"]
        self.descripcion = pokemon_data["descripcion"]
        
        # Datos que escalan con nivel
        self.nivel = nivel
        self.stats_base = pokemon_data["estadisticas"]
        self.stats_actuales = self.calcular_stats()
        self.hp_actual = self.stats_actuales["hp"]
        
        # Movimientos
        self.movimientos = []  # Se carga desde movset.json
        self.cargar_movimientos()
        
        # Experiencia
        self.exp = 0
        self.exp_siguiente_nivel = self.calcular_exp_requerida()
    
    def calcular_stats(self):
        """Fórmula simple para calcular stats según nivel"""
        stats = {}
        for stat, base in self.stats_base.items():
            # Fórmula básica: stat = base + (nivel * factor)
            factor = 0.5 if stat == "hp" else 0.3
            stats[stat] = int(base + (self.nivel * base * factor))
        return stats
    
    def cargar_movimientos(self):
        with open("data/movset.json", "r", encoding="utf-8") as f:
            movsets = json.load(f)
        movset = next((m for m in movsets if m["pokemon"] == self.nombre), None)
        if not movset:
            return
        
        with open("data/movements.json", "r", encoding="utf-8") as f:
            todos_movimientos = json.load(f)
        
        for mov_data in movset["movimientos"]:
            if mov_data["nivel"] <= self.nivel:
                mov_info = next(m for m in todos_movimientos if m["nombre"] == mov_data["nombre"])
                self.movimientos.append(mov_info)
                if len(self.movimientos) >= 4:  # Máximo 4 movimientos
                    break
    
    def calcular_exp_requerida(self):
        return int(100 * (self.nivel ** 1.5))
    
    def ganar_exp(self, cantidad):
        self.exp += cantidad
        if self.exp >= self.exp_siguiente_nivel:
            self.subir_nivel()
    
    def subir_nivel(self):
        self.nivel += 1
        self.exp = 0
        self.exp_siguiente_nivel = self.calcular_exp_requerida()
        self.stats_actuales = self.calcular_stats()
        self.hp_actual = self.stats_actuales["hp"]
        # Verificar nuevos movimientos
        self.cargar_movimientos()
    
    def curar(self, cantidad):
        self.hp_actual = min(self.hp_actual + cantidad, self.stats_actuales["hp"])
    
    def esta_debilitado(self):
        return self.hp_actual <= 0