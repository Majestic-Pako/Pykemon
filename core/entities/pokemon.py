import pygame
import json

class Pokemon:
    def __init__(self, nombre_pokemon, nivel=5):
        pokemon_id = nombre_pokemon.lower().strip()
        
        with open("data/pokemon.json", "r", encoding="utf-8") as f:
            todos_pokemon = json.load(f)
        
        if pokemon_id not in todos_pokemon:
            raise ValueError(f"Pokémon '{nombre_pokemon}' no encontrado en pokemon.json")
        
        pokemon_data = todos_pokemon[pokemon_id]
        
        self.id = pokemon_id  
        self.nombre = pokemon_data["nombre"]  
        self.tipos = [pokemon_data["tipo1"]]
        if pokemon_data["tipo2"]:
            self.tipos.append(pokemon_data["tipo2"])
        self.sprite = pokemon_data["sprite_id"]
        self.descripcion = pokemon_data["descripcion"]
        self.nivel = nivel
        self.stats_base = pokemon_data["stats"]
        self.stats_actuales = self.calcular_stats()
        self.ps_actual = self.stats_actuales["ps"]
        self.movimientos = []
        self.cargar_movimientos()
        self.exp = 0
        self.exp_siguiente_nivel = self.calcular_exp_requerida()
    
    def calcular_stats(self):
        stats = {}
        for stat, base in self.stats_base.items():
            factor = 0.5 if stat == "ps" else 0.3
            stats[stat] = int(base + (self.nivel * base * factor))
        return stats
    
    def cargar_movimientos(self):
        try:
            with open("data/movset.json", "r", encoding="utf-8") as f:
                movsets = json.load(f)
            
            movset = movsets.get(self.id)
            
            if not movset:
                print(f"! No se encontró moveset para '{self.id}' en movset.json")
                return
            
            with open("data/movements.json", "r", encoding="utf-8") as f:
                todos_movimientos = json.load(f)
            
            self.movimientos = []
            for mov_data in movset:
                nivel_req = mov_data.get("nivel", 0)
                
                if nivel_req > self.nivel:
                    continue
                
                nombre_mov = mov_data.get("movimiento", "").lower()
                
                mov_info = todos_movimientos.get(nombre_mov)
                
                if mov_info:
                    movimiento_instancia = mov_info.copy()
                    movimiento_instancia["pp_actual"] = mov_info["pp"]
                    self.movimientos.append(movimiento_instancia)
                
                if len(self.movimientos) >= 4:
                    break
            
            if self.movimientos:
                print(f"[OK] {self.nombre} aprendió: {[m['nombre'] for m in self.movimientos]}")
            else:
                print(f"[WARN] {self.nombre} no tiene movimientos disponibles en nivel {self.nivel}")
        
        except FileNotFoundError as e:
            print(f"[WARN] Error cargando movimientos: {e}")
        except Exception as e:
            print(f"[ERROR] Error en cargar_movimientos: {e}")
    
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
        self.ps_actual = self.stats_actuales["ps"]
        
        self.cargar_movimientos()
        print(f"[OK] {self.nombre} subió al nivel {self.nivel}!")
    
    def curar(self, cantidad):
        self.ps_actual = min(self.ps_actual + cantidad, self.stats_actuales["ps"])
        return self.ps_actual  
    
    def esta_debilitado(self):
        return self.ps_actual <= 0
    
    def restaurar_pp(self):
        for movimiento in self.movimientos:
            movimiento["pp_actual"] = movimiento["pp"]
    
    def obtener_ruta_sprite(self, es_enemigo=True):
        carpeta = "back" if es_enemigo else "front"
        return f"assets/pokemon/{carpeta}/{self.id}.png"