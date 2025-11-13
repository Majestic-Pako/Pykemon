import pygame
import json

class Pokemon:
    def __init__(self, nombre_pokemon, nivel=5):
        """
        Crea un Pokémon desde su ID (key del JSON)
        Args:
            nombre_pokemon: ID del pokemon (ej: "treecko", "mudkip")
            nivel: Nivel inicial del pokemon
        """
        # Normalizar nombre a minúsculas para búsqueda
        pokemon_id = nombre_pokemon.lower().strip()
        
        # Cargar datos del Pokémon
        with open("data/pokemon.json", "r", encoding="utf-8") as f:
            todos_pokemon = json.load(f)
        
        if pokemon_id not in todos_pokemon:
            raise ValueError(f"Pokémon '{nombre_pokemon}' no encontrado en pokemon.json")
        
        pokemon_data = todos_pokemon[pokemon_id]
        
        # Datos permanentes
        self.id = pokemon_id  # Guardar ID para cargar sprites
        self.nombre = pokemon_data["nombre"]  # Nombre con mayúscula
        
        # Tipos
        self.tipos = [pokemon_data["tipo1"]]
        if pokemon_data["tipo2"]:
            self.tipos.append(pokemon_data["tipo2"])
        
        self.sprite = pokemon_data["sprite_id"]
        self.descripcion = pokemon_data["descripcion"]
        
        # Stats y nivel
        self.nivel = nivel
        self.stats_base = pokemon_data["stats"]
        self.stats_actuales = self.calcular_stats()
        self.ps_actual = self.stats_actuales["ps"]
        
        # Movimientos
        self.movimientos = []
        self.cargar_movimientos()
        
        # Experiencia
        self.exp = 0
        self.exp_siguiente_nivel = self.calcular_exp_requerida()
    
    def calcular_stats(self):
        """Calcula stats según nivel usando fórmula simple"""
        stats = {}
        for stat, base in self.stats_base.items():
            factor = 0.5 if stat == "ps" else 0.3
            stats[stat] = int(base + (self.nivel * base * factor))
        return stats
    
    def cargar_movimientos(self):
        """
        Carga movimientos desde movset.json según el nivel actual
        Formato esperado en movset.json:
        {
            "treecko": [
                {"movimiento": "placaje", "nivel": 1},
                {"movimiento": "absorber", "nivel": 6}
            ]
        }
        """
        try:
            # Cargar moveset del Pokémon
            with open("data/movset.json", "r", encoding="utf-8") as f:
                movsets = json.load(f)
            
            # Buscar moveset usando el ID
            movset = movsets.get(self.id)
            
            if not movset:
                print(f"⚠️ No se encontró moveset para '{self.id}' en movset.json")
                return
            
            # Cargar datos de movimientos
            with open("data/movements.json", "r", encoding="utf-8") as f:
                todos_movimientos = json.load(f)
            
            # Filtrar movimientos según nivel y agregar hasta 4
            self.movimientos = []
            for mov_data in movset:
                nivel_req = mov_data.get("nivel", 0)
                
                # Solo movimientos que el Pokémon puede aprender en su nivel actual
                if nivel_req > self.nivel:
                    continue
                
                nombre_mov = mov_data.get("movimiento", "").lower()
                
                # Buscar info del movimiento
                mov_info = todos_movimientos.get(nombre_mov)
                
                if mov_info:
                    # ✅ CREAR UNA COPIA del movimiento con pp_actual
                    movimiento_instancia = mov_info.copy()
                    movimiento_instancia["pp_actual"] = mov_info["pp"]  # Inicializar PP actual
                    self.movimientos.append(movimiento_instancia)
                
                # Máximo 4 movimientos
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
        """Calcula experiencia necesaria para subir de nivel"""
        return int(100 * (self.nivel ** 1.5))
    
    def ganar_exp(self, cantidad):
        """Agrega experiencia y sube de nivel si corresponde"""
        self.exp += cantidad
        if self.exp >= self.exp_siguiente_nivel:
            self.subir_nivel()
    
    def subir_nivel(self):
        """Sube un nivel y recalcula stats"""
        self.nivel += 1
        self.exp = 0
        self.exp_siguiente_nivel = self.calcular_exp_requerida()
        self.stats_actuales = self.calcular_stats()
        self.ps_actual = self.stats_actuales["ps"]
        
        # Recargar movimientos por si aprende nuevos
        self.cargar_movimientos()
        print(f"[OK] {self.nombre} subió al nivel {self.nivel}!")
    
    def curar(self, cantidad):
        """Restaura PS sin exceder el máximo"""
        self.ps_actual = min(self.ps_actual + cantidad, self.stats_actuales["ps"])
        return self.ps_actual  # Retorna PS actual para feedback
    
    def esta_debilitado(self):
        """Verifica si el Pokémon está fuera de combate"""
        return self.ps_actual <= 0
    
    def restaurar_pp(self):
        """Restaura todos los PP de los movimientos al máximo"""
        for movimiento in self.movimientos:
            movimiento["pp_actual"] = movimiento["pp"]
    
    def obtener_ruta_sprite(self, es_enemigo=True):
        """
        Genera la ruta del sprite según si es enemigo o jugador
        Args:
            es_enemigo: True = back/ (vista espalda), False = front/ (vista frente)
        Returns:
            String con la ruta del sprite
        """
        carpeta = "back" if es_enemigo else "front"
        return f"assets/pokemon/{carpeta}/{self.id}.png"