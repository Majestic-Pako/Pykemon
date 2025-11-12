import pygame
import json
from core.system.config import *
from core.entities.movement import manejar_movimiento
from core.system.camera import Camera
from core.ui.dialog import DialogoBox
from core.entities.pokemon import Pokemon

class Player(pygame.sprite.Sprite):
    def __init__(self, ancho, alto, ancho_mapa, alto_mapa):
        super().__init__()
        self.image = self.cargar_sprite()
        self.rect = self.image.get_rect(
            center=(ancho // 2, alto // 2)
        )
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.dialogo_activo = False
        self.dialogo_texto = ""
        self.dialogo_npc_id = None
        self.dialogo_box = DialogoBox()
        self._z_held = False
        self.equipo_pokemon = []
        self.bolsa = {
            "curacion": {},
            "captura": {},
            "debug": {}
        }
        with open("data/objects.json", "r", encoding="utf-8") as f:
            self.objects_data = json.load(f)
        
        # Pokémon en el equipo para pruebas (después borrar)
        mudkip = Pokemon("mudkip", nivel=5)
        treecko = Pokemon("treecko", nivel=5)
        self.equipo_pokemon.extend([mudkip, treecko])
        self.agregar_objeto("pocion", 5)
        self.agregar_objeto("superpocion", 5)
        self.agregar_objeto("pokeball", 10)
        self.agregar_objeto("caramelo_raro", 10)

    def cargar_sprite(self):
        try:
            sprite = pygame.image.load("assets/sprites/player/aca_la_imagen.png")
            sprite = pygame.transform.scale(sprite, (TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            return sprite
        except FileNotFoundError:
            placeholder = pygame.Surface((TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            placeholder.fill(RED)
            return placeholder
    
    def update(self, teclas):
        self.limitar_limites()
    
    def limitar_limites(self):
        self.rect.x = max(0, min(self.rect.x, self.ancho_mapa - TAMAÑO_CUADRADO))
        self.rect.y = max(0, min(self.rect.y, self.alto_mapa - TAMAÑO_CUADRADO))
    
    def dibujar(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))
        self.dialogo_box.dibujar(superficie)
    
    def manejar_dialogo(self, teclas, npcs):
        z_now = teclas[pygame.K_z]
        if z_now and not self._z_held:
            if self.dialogo_box.activo:
                self.dialogo_box.cerrar()
                pygame.time.wait(200)
            else:
                area_interaccion = self.rect.inflate(TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)
                for npc in npcs:
                    if area_interaccion.colliderect(npc.rect):
                        metadata = {"NPC ID": getattr(npc, "npc_id", None)}
                        self.dialogo_box.mostrar(getattr(npc, "dialog_id", "Sin dialogo"), metadata)
                        pygame.time.wait(150)
                        break
        self._z_held = z_now

    def testear_combate(self, zonas_combate):
        for zona in zonas_combate:
            if self.rect.colliderect(zona["rect"]):
                import random
                if random.random() < zona["encounter_rate"]:
                    pokemon = random.choice(zona["pokemon_ids"])
                    nivel = zona["min_level"] + random.randint(0, 2)
                    texto = f"Combate! {pokemon.strip()} salvaje (Nv.{nivel})"
                    metadata = {"Zona": "Test", "Rate": zona["encounter_rate"]}
                    self.dialogo_box.mostrar(texto, metadata)
                    return True
        return False
    
    def puede_moverse(self):
        return not self.dialogo_box.activo
    
    # ========== MÉTODOS DE EQUIPO POKÉMON ==========
    
    def obtener_equipo(self):
        """Devuelve la lista completa del equipo"""
        return self.equipo_pokemon
    
    def obtener_pokemon_activo(self):
        """Devuelve el primer Pokémon no debilitado del equipo"""
        for pokemon in self.equipo_pokemon:
            if not pokemon.esta_debilitado():
                return pokemon
        return None
    
    def obtener_pokemon_por_indice(self, indice):
        """Devuelve un Pokémon específico por su índice en el equipo"""
        if 0 <= indice < len(self.equipo_pokemon):
            return self.equipo_pokemon[indice]
        return None
    
    def agregar_pokemon(self, pokemon_instancia):
        """Agrega un Pokémon al equipo (máximo 6)"""
        if len(self.equipo_pokemon) < 6:
            self.equipo_pokemon.append(pokemon_instancia)
            return {"exito": True, "mensaje": f"{pokemon_instancia.nombre} se unió al equipo!"}
        else:
            # Aquí podrías implementar envío al PC
            return {"exito": False, "mensaje": "Equipo lleno! (Enviar a PC pendiente)"}
    
    def quitar_pokemon(self, indice):
        """Remueve un Pokémon del equipo (útil para transferencias)"""
        if 0 <= indice < len(self.equipo_pokemon):
            pokemon = self.equipo_pokemon.pop(indice)
            return {"exito": True, "pokemon": pokemon}
        return {"exito": False, "pokemon": None}
    
    def intercambiar_pokemon(self, indice1, indice2):
        """Intercambia la posición de dos Pokémon en el equipo"""
        if (0 <= indice1 < len(self.equipo_pokemon) and 
            0 <= indice2 < len(self.equipo_pokemon)):
            self.equipo_pokemon[indice1], self.equipo_pokemon[indice2] = \
                self.equipo_pokemon[indice2], self.equipo_pokemon[indice1]
            return True
        return False
    
    def tiene_pokemon_vivos(self):
        """Verifica si hay al menos un Pokémon no debilitado"""
        return any(not p.esta_debilitado() for p in self.equipo_pokemon)
    
    def curar_equipo_completo(self):
        """Cura todos los Pokémon del equipo (para Centros Pokémon)"""
        for pokemon in self.equipo_pokemon:
            pokemon.ps_actual = pokemon.stats_actuales["ps"]
            # Aquí podrías restaurar PP de movimientos si lo implementas
        return True
    
    # ========== MÉTODOS DE BOLSA ==========
    
    def obtener_bolsa(self):
        """Devuelve el diccionario completo de la bolsa"""
        return self.bolsa
    
    def obtener_objetos_por_tipo(self, tipo):
        """Devuelve los objetos de un tipo específico (curacion, captura, debug)"""
        if tipo in self.bolsa:
            return self.bolsa[tipo]
        return {}
    
    def tiene_objeto(self, objeto_key):
        """Verifica si el jugador tiene al menos 1 unidad de un objeto"""
        objeto_data = self.objects_data.get(objeto_key)
        if not objeto_data:
            return False
        
        tipo = objeto_data["tipo"]
        return objeto_key in self.bolsa[tipo] and self.bolsa[tipo][objeto_key] > 0
    
    def contar_objeto(self, objeto_key):
        """Devuelve la cantidad de un objeto específico"""
        objeto_data = self.objects_data.get(objeto_key)
        if not objeto_data:
            return 0
        
        tipo = objeto_data["tipo"]
        return self.bolsa[tipo].get(objeto_key, 0)
    
    def agregar_objeto(self, objeto_key, cantidad=1):
        """Agrega objetos a la bolsa"""
        if objeto_key not in self.objects_data:
            return {"exito": False, "mensaje": "Objeto no encontrado"}
        
        tipo = self.objects_data[objeto_key]["tipo"]
        
        if objeto_key in self.bolsa[tipo]:
            self.bolsa[tipo][objeto_key] += cantidad
        else:
            self.bolsa[tipo][objeto_key] = cantidad
        
        nombre = self.objects_data[objeto_key]["nombre"]
        return {"exito": True, "mensaje": f"Obtenido: {nombre} x{cantidad}"}
    
    def quitar_objeto(self, objeto_key, cantidad=1):
        """Remueve objetos de la bolsa (útil para ventas/drops)"""
        if not self.tiene_objeto(objeto_key):
            return {"exito": False, "mensaje": "No tienes ese objeto"}
        
        objeto_data = self.objects_data[objeto_key]
        tipo = objeto_data["tipo"]
        
        if self.bolsa[tipo][objeto_key] >= cantidad:
            self.bolsa[tipo][objeto_key] -= cantidad
            if self.bolsa[tipo][objeto_key] <= 0:
                del self.bolsa[tipo][objeto_key]
            return {"exito": True, "mensaje": f"Removido: {objeto_data['nombre']} x{cantidad}"}
        else:
            return {"exito": False, "mensaje": "No tienes suficientes"}

    def usar_objeto(self, objeto_key, pokemon_objetivo=None):
        """Usa un objeto en un Pokémon"""
        if objeto_key not in self.objects_data:
            return {"exito": False, "mensaje": "Objeto no encontrado"}
        
        objeto_data = self.objects_data[objeto_key]
        tipo = objeto_data["tipo"]
        
        # Verificar que tenemos el objeto
        if not self.tiene_objeto(objeto_key):
            return {"exito": False, "mensaje": f"No tienes {objeto_data['nombre']}"}
        
        # Aplicar efecto según tipo
        resultado = {"exito": False, "mensaje": ""}
        
        if objeto_data["efecto"] == "restaurar_ps":
            if not pokemon_objetivo:
                return {"exito": False, "mensaje": "Selecciona un Pokémon"}
            
            if pokemon_objetivo.esta_debilitado():
                return {"exito": False, "mensaje": "No se puede usar en este Pokémon"}
            
            ps_anterior = pokemon_objetivo.ps_actual
            pokemon_objetivo.curar(objeto_data["valor"])
            ps_curado = pokemon_objetivo.ps_actual - ps_anterior
            
            if ps_curado <= 0:
                return {"exito": False, "mensaje": f"{pokemon_objetivo.nombre} ya tiene PS al máximo"}
            
            resultado = {
                "exito": True,
                "mensaje": f"{pokemon_objetivo.nombre} recuperó {ps_curado} PS"
            }
        
        elif objeto_data["efecto"] == "capturar":
            # Para usar en combate
            resultado = {
                "exito": True,
                "tasa_captura": objeto_data["valor"],
                "mensaje": f"Usando {objeto_data['nombre']}"
            }
        
        elif objeto_data["efecto"] == "subir_nivel":
            if not pokemon_objetivo:
                return {"exito": False, "mensaje": "Selecciona un Pokémon"}
            
            pokemon_objetivo.nivel += objeto_data["valor"]
            pokemon_objetivo.stats_actuales = pokemon_objetivo.calcular_stats()
            pokemon_objetivo.ps_actual = pokemon_objetivo.stats_actuales["ps"]
            pokemon_objetivo.cargar_movimientos()
            
            resultado = {
                "exito": True,
                "mensaje": f"{pokemon_objetivo.nombre} subió a nivel {pokemon_objetivo.nivel}!"
            }
        
        # Consumir objeto si se usó exitosamente
        if resultado["exito"]:
            self.bolsa[tipo][objeto_key] -= 1
            if self.bolsa[tipo][objeto_key] <= 0:
                del self.bolsa[tipo][objeto_key]
        
        return resultado