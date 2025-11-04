#Importa las librerias neesarias
import pygame
import json
from core.system.config import *
from core.entities.movement import manejar_movimiento
from core.system.camera import Camera
from core.ui.dialog import DialogoBox
from core.entities.pokemon import Pokemon

#Se declara la clase player con sus atributos
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
        #Se hace un array con posiciones con estos nombres
        "curacion": {},      # {"Poción": 5, "Superpoción": 2}
        "captura": {},     # {"Pokéball": 10, "Superball": 3}
        "debug": {}          # carameloraro 
        }
        #Se abre el objeto si toca tal tecla
        with open("data/objects.json", "r", encoding="utf-8") as f:
            self.objects_data = json.load(f)
        # Pokémon en el equipo para pruebas y objeto despues borrar
        mudkip = Pokemon("mudkip", nivel=5)
        treecko = Pokemon("treecko", nivel=5)
        self.equipo_pokemon.extend([mudkip, treecko])
        self.agregar_objeto("pocion", 5)
        self.agregar_objeto("superpocion", 5)
        self.agregar_objeto("pokeball", 10)
        self.agregar_objeto("caramelo_raro", 10)

    def cargar_sprite(self):
        try:
            # Cambiar por la ruta correcta del sprite
            sprite = pygame.image.load("assets/sprites/player/aca_la_imagen.png")
            sprite = pygame.transform.scale(sprite, (TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            return sprite
        except FileNotFoundError:
            # Testeo con solo el cuadrado
            placeholder = pygame.Surface((TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            placeholder.fill(RED)
            return placeholder
    #Esta funcion limita con los parametros las teclas y se actualiza mediante el juego
    def update(self, teclas):
        self.limitar_limites()
    
    #Marca los limites del mapa y el tamaño
    def limitar_limites(self):
        self.rect.x = max(0, min(self.rect.x, self.ancho_mapa - TAMAÑO_CUADRADO))
        self.rect.y = max(0, min(self.rect.y, self.alto_mapa - TAMAÑO_CUADRADO))
    
    #Dibuja
    def dibujar(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))
        self.dialogo_box.dibujar(superficie)
    #Maneja el dialogo con ciertas teclas
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
    #Testea el combate en acercamiento del personaje cuando se mueve
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
    #Solo puede moverse si el dialogo no esta activo
    def puede_moverse(self):
        return not self.dialogo_box.activo
    
    #Agrega un poquemon de otra instancia
    def agregar_pokemon(self, pokemon_instancia):
        """Agrega un Pokémon al equipo o al almacenamiento"""
        if len(self.equipo_pokemon) < 6:
            self.equipo_pokemon.append(pokemon_instancia)
            return True
        else:
            self.pokemon_storage.append(pokemon_instancia)
            return False  # Enviado al PC

    #Usa el objeto si se abrio tal cosa con una tecla
    def usar_objeto(self, objeto_key, pokemon_objetivo=None):
    # Cargar datos del objeto
        with open("data/objects.json", "r", encoding="utf-8") as f:
            objetos = json.load(f)
    
        if objeto_key not in objetos:
            return {"exito": False, "mensaje": "Objeto no encontrado"}
    
        objeto_data = objetos[objeto_key]
        tipo = objeto_data["tipo"]
    
    # Verificar que tenemos el objeto
        if objeto_key not in self.bolsa[tipo] or self.bolsa[tipo][objeto_key] <= 0:
            return {"exito": False, "mensaje": f"No tienes {objeto_data['nombre']}"}
    
    # Aplicar efecto según tipo
        resultado = {"exito": False, "mensaje": ""}
    
        if objeto_data["efecto"] == "restaurar_ps":
            if not pokemon_objetivo or pokemon_objetivo.esta_debilitado():
                return {"exito": False, "mensaje": "No se puede usar en este Pokémon"}
        
            ps_anterior = pokemon_objetivo.ps_actual
            pokemon_objetivo.curar(objeto_data["valor"])
            ps_curado = pokemon_objetivo.ps_actual - ps_anterior
        
            resultado = {
                "exito": True,
                "mensaje": f"{pokemon_objetivo.nombre} recuperó {ps_curado} PS"
            }
    
        elif objeto_data["efecto"] == "capturar":
        # Esto se usará en el sistema de batalla
            resultado = {
                "exito": True,
                "tasa_captura": objeto_data["valor"],
                "mensaje": f"Usando {objeto_data['nombre']}"
            }
         #Condiciones logicas    
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

        if resultado["exito"]:
            self.bolsa[tipo][objeto_key] -= 1
            if self.bolsa[tipo][objeto_key] <= 0:
                del self.bolsa[tipo][objeto_key]
    
        return resultado
      #Funcion de agregar objeto si cumple lo anterior 
    def agregar_objeto(self, objeto_key, cantidad=1):
        with open("data/objects.json", "r", encoding="utf-8") as f:
            objetos = json.load(f)
    
        if objeto_key not in objetos:
            return False
    
        tipo = objetos[objeto_key]["tipo"]
    
        if objeto_key in self.bolsa[tipo]:
            self.bolsa[tipo][objeto_key] += cantidad
        else:
            self.bolsa[tipo][objeto_key] = cantidad
    
        return True
#Obtiene el pokemon
def obtener_pokemon_activo(self):
    """Devuelve el primer Pokémon no debilitado"""
    for pokemon in self.equipo_pokemon:
        if not pokemon.esta_debilitado():
            return pokemon
    return None