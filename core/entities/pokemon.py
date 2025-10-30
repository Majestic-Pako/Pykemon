import pygame
import json

class Pokemon:
    def __init__(self, nombre_pokemon, nivel=5, pokemon_data=None):
        # Cargar datos base si no se proveen
        if pokemon_data is None:
            with open("data/pokemon.json", "r", encoding="utf-8") as f:
                todos_pokemon = json.load(f)
                # Buscar en el diccionario usando la key
                pokemon_data = todos_pokemon.get(nombre_pokemon.lower())
                if not pokemon_data:
                    raise ValueError(f"Pokémon '{nombre_pokemon}' no encontrado en el JSON")
        
        # Datos permanentes
        self.nombre = pokemon_data["nombre"]
        
        # Adaptar tipos (tu JSON usa tipo1/tipo2)
        self.tipos = [pokemon_data["tipo1"]]
        if pokemon_data["tipo2"]:
            self.tipos.append(pokemon_data["tipo2"])
        
        self.sprite = pokemon_data["sprite_id"]
        self.descripcion = pokemon_data["descripcion"]
        
        # Datos que escalan con nivel
        self.nivel = nivel
        self.stats_base = pokemon_data["stats"]  # Tu JSON usa "stats" no "estadisticas"
        self.stats_actuales = self.calcular_stats()
        self.ps_actual = self.stats_actuales["ps"]  # Tu JSON usa "ps" 
        
        # Movimientos
        self.movimientos = []
        self.cargar_movimientos()
        
        # Experiencia
        self.exp = 0
        self.exp_siguiente_nivel = self.calcular_exp_requerida()
    
    def calcular_stats(self):
        """Fórmula simple para calcular stats según nivel"""
        stats = {}
        for stat, base in self.stats_base.items():
            # Fórmula básica: stat = base + (nivel * factor)
            factor = 0.5 if stat == "ps" else 0.3  
            stats[stat] = int(base + (self.nivel * base * factor))
        return stats
    
    def cargar_movimientos(self):
        try:
            with open("data/movset.json", "r", encoding="utf-8") as f:
                movsets = json.load(f)

            # localizar movset para este Pokémon (soporta dict o lista)
            movset = None
            if isinstance(movsets, dict):
                movset = movsets.get(self.nombre.lower()) or movsets.get(self.nombre)
            elif isinstance(movsets, list):
                movset = next(
                    (m for m in movsets
                        if (m.get("pokemon","").lower() == self.nombre.lower()) or (m.get("pokemon","") == self.nombre)),
                    None
                )

            if not movset:
                return

            # extraer la lista de movimientos según la estructura encontrada
            if isinstance(movset, dict):
                if "movimientos" in movset and isinstance(movset["movimientos"], list):
                    mov_list = movset["movimientos"]
                elif "moves" in movset and isinstance(movset["moves"], list):
                    mov_list = movset["moves"]
                elif isinstance(movset.get("movimientos"), list):
                    mov_list = movset.get("movimientos")
                else:
                    # si movset mismo ya es una lista de movimientos
                    mov_list = movset if isinstance(movset, list) else []
            elif isinstance(movset, list):
                mov_list = movset
            else:
                return

            if not mov_list:
                return

            with open("data/movements.json", "r", encoding="utf-8") as f:
                todos_movimientos = json.load(f)

            for mov_data in mov_list:
                # soportar varias formas de nombrar los campos
                nivel_req = mov_data.get("nivel") or mov_data.get("level") or 0
                nombre_mov = mov_data.get("nombre") or mov_data.get("move") or mov_data.get("nombre_mov") or ""

                if nivel_req > self.nivel:
                    continue

                mov_info = None
                if isinstance(todos_movimientos, dict):
                    mov_info = todos_movimientos.get(nombre_mov.lower()) or todos_movimientos.get(nombre_mov)
                else:
                    mov_info = next(
                        (m for m in todos_movimientos
                            if (m.get("nombre","").lower() == nombre_mov.lower()) or (m.get("nombre","") == nombre_mov)),
                        None
                    )

                if mov_info:
                    self.movimientos.append(mov_info)
                if len(self.movimientos) >= 4:
                    break
        except FileNotFoundError:
            # archivos faltantes: no romper la ejecución, dejar lista vacía
            return
    
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
    
    def curar(self, cantidad):
        self.ps_actual = min(self.ps_actual + cantidad, self.stats_actuales["ps"]) 
    
    def esta_debilitado(self):
        return self.ps_actual <= 0