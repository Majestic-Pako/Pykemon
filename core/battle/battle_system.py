"""
Sistema de Batalla estilo Pokémon Esmeralda
============================================
Este módulo maneja toda la lógica de batalla del juego.
Se integra sin modificar el código existente de player.py o map.py.
"""

import pygame
import random
from core.system.config import *

class Move:
    """
    Representa un movimiento de Pokémon.
    
    Atributos:
        name: Nombre del movimiento
        power: Poder base del ataque
        acc: Precisión (0-100)
        pp: Puntos de poder actuales
        max_pp: PP máximos
        category: 'physical' o 'special'
        effect: Función opcional para efectos especiales
    """
    def __init__(self, name, power, acc, pp, category='physical', effect=None):
        self.name = name
        self.power = power
        self.acc = acc
        self.pp = pp
        self.max_pp = pp
        self.category = category
        self.effect = effect


class BattleSystem:
    """
    Sistema principal de batalla.
    
    Controla toda la lógica, UI y flujo de una batalla Pokémon.
    Cuando está activo (self.active = True), toma control completo
    de inputs y renderizado.
    """
    
    # === SINGLETON PATTERN ===
    # Permite acceder al sistema de batalla desde cualquier lugar
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Devuelve la única instancia del sistema de batalla"""
        if cls._instance is None:
            raise Exception("BattleSystem no ha sido inicializado")
        return cls._instance
    
    def __init__(self, screen_width, screen_height):
        """
        Inicializa el sistema de batalla.
        
        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        # Guardar instancia singleton
        BattleSystem._instance = self
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("arial", 18)
        
        # Estado de la batalla
        self.active = False  # ← IMPORTANTE: Controla si hay batalla activa
        self.player_pkm = None
        self.enemy_pkm = None
        
        # Estado del menú y UI
        self.state = {
            'phase': 'menu',        # Fase actual: 'menu', 'choose_move', 'anim', 'message', 'end'
            'menu_index': 0,        # Índice del menú principal
            'move_index': 0,        # Índice del menú de movimientos
            'message': '',          # Mensaje actual en pantalla
            'anim': None,           # Estado de animación actual
            'turn_order': [],       # Orden de ejecución de turnos
            'player_move': None,    # Movimiento elegido por el jugador
            'enemy_move': None,     # Movimiento elegido por el enemigo
        }
        
        self.message_timer = 0
        self.battle_result = None  # 'win', 'lose', 'escape', None
    
    # ========== CONTROL DE BATALLA ==========
    
    def iniciar_batalla(self, pokemon_jugador, pokemon_enemigo):
        """
        Inicia una batalla entre dos Pokémon.
        
        Args:
            pokemon_jugador: Instancia del Pokémon del jugador
            pokemon_enemigo: Instancia del Pokémon enemigo
        """
        self.active = True
        self.player_pkm = pokemon_jugador
        self.enemy_pkm = pokemon_enemigo
        self.battle_result = None
        
        # Asegurar que ambos Pokémon tengan movimientos
        if not hasattr(pokemon_jugador, 'movimientos') or not pokemon_jugador.movimientos:
            pokemon_jugador.movimientos = self._crear_movimientos_default()
        
        if not hasattr(pokemon_enemigo, 'movimientos') or not pokemon_enemigo.movimientos:
            pokemon_enemigo.movimientos = self._crear_movimientos_default()
        
        # Resetear estado de la batalla
        self.state = {
            'phase': 'menu',
            'menu_index': 0,
            'move_index': 0,
            'message': '',
            'anim': None,
            'turn_order': [],
            'player_move': None,
            'enemy_move': None,
        }
        
        # Mostrar mensaje de inicio
        self.set_message(f"¡Apareció {pokemon_enemigo.nombre} salvaje!", 1400)
    
    def terminar_batalla(self):
        """
        Finaliza la batalla y retorna al juego normal.
        
        Returns:
            str: Resultado de la batalla ('win', 'lose', 'escape')
        """
        self.active = False
        return self.battle_result
    
    def _crear_movimientos_default(self):
        """
        Crea movimientos por defecto para Pokémon sin movimientos.
        
        Returns:
            list: Lista de objetos Move
        """
        return [
            Move("Tackle", 40, 100, 35, 'physical'),
            Move("Scratch", 40, 100, 35, 'physical'),
            Move("Growl", 0, 100, 40, 'physical'),
            Move("Quick Attack", 40, 100, 30, 'physical')
        ]
    
    # ========== CÁLCULO DE DAÑO ==========
    
    def calc_damage(self, attacker, defender, move):
        """
        Calcula el daño de un movimiento usando la fórmula de Gen III.
        
        Args:
            attacker: Pokémon atacante
            defender: Pokémon defensor
            move: Movimiento usado
            
        Returns:
            tuple: (daño_causado, estado) donde estado puede ser 'miss' o 'hit'
        """
        # Verificar precisión del movimiento
        if random.randint(1, 100) > move.acc:
            return 0, "miss"
        
        # Calcular golpe crítico (6.25% de probabilidad)
        crit = 1.5 if random.random() < 0.0625 else 1.0
        
        # Elegir stats según categoría del movimiento
        if move.category == 'physical':
            A = attacker.stats_actuales.get('ataque', 50)
            D = defender.stats_actuales.get('defensa', 50)
        else:  # special
            A = attacker.stats_actuales.get('ataque_especial', 50)
            D = defender.stats_actuales.get('defensa_especial', 50)
        
        # Fórmula de daño Gen III simplificada
        level_factor = (2 * attacker.nivel) / 5 + 2
        base = ((level_factor * move.power * (A / max(1, D))) / 50) + 2
        
        # Modificador aleatorio (0.85 - 1.00) y crítico
        modifier = crit * random.uniform(0.85, 1.0)
        damage = int(base * modifier)
        damage = max(1, damage)  # Mínimo 1 de daño
        
        return damage, "hit"
    
    # ========== EJECUCIÓN DE ACCIONES ==========
    
    def execute_action(self, actor, move):
        """
        Ejecuta una acción de batalla (usar un movimiento).
        
        Args:
            actor: 'player' o 'enemy'
            move: Objeto Move a ejecutar
            
        Returns:
            str: Mensaje descriptivo del resultado
        """
        # Determinar atacante y defensor
        if actor == 'player':
            attacker = self.player_pkm
            defender = self.enemy_pkm
        else:
            attacker = self.enemy_pkm
            defender = self.player_pkm
        
        if move is None:
            return f"{attacker.nombre} no tiene movimiento."
        
        # Verificar que haya PP disponible
        if move.pp <= 0:
            return f"No hay PP para {move.name}!"
        
        # Consumir PP
        move.pp -= 1
        
        # Calcular y aplicar daño
        damage, status = self.calc_damage(attacker, defender, move)
        
        if status == 'miss':
            return f"{attacker.nombre} usó {move.name}... ¡Falló!"
        else:
            # Reducir PS del defensor
            defender.ps_actual = max(0, defender.ps_actual - damage)
            return f"{attacker.nombre} usó {move.name} y causó {damage} puntos de daño."
    
    # ========== IA DEL ENEMIGO ==========
    
    def enemy_choose_move(self):
        """
        IA simple: el enemigo elige un movimiento aleatorio con PP disponible.
        
        Returns:
            Move: Movimiento elegido, o None si no hay movimientos disponibles
        """
        if not hasattr(self.enemy_pkm, 'movimientos') or not self.enemy_pkm.movimientos:
            return None
        
        # Filtrar movimientos con PP disponible
        choices = [m for m in self.enemy_pkm.movimientos if m.pp > 0]
        
        if not choices:
            return None
        
        return random.choice(choices)
    
    # ========== ORDEN DE TURNOS ==========
    
    def decide_turns(self):
        """
        Decide el orden de los turnos basado en la velocidad de los Pokémon.
        El más rápido ataca primero. En caso de empate, se elige al azar.
        """
        player_speed = self.player_pkm.stats_actuales.get('velocidad', 50)
        enemy_speed = self.enemy_pkm.stats_actuales.get('velocidad', 50)
        
        if player_speed > enemy_speed:
            # Jugador es más rápido
            self.state['turn_order'] = [
                ('player', self.state['player_move']), 
                ('enemy', self.state['enemy_move'])
            ]
        elif player_speed < enemy_speed:
            # Enemigo es más rápido
            self.state['turn_order'] = [
                ('enemy', self.state['enemy_move']), 
                ('player', self.state['player_move'])
            ]
        else:
            # Misma velocidad: elegir al azar
            first = random.choice(['player', 'enemy'])
            if first == 'player':
                self.state['turn_order'] = [
                    ('player', self.state['player_move']), 
                    ('enemy', self.state['enemy_move'])
                ]
            else:
                self.state['turn_order'] = [
                    ('enemy', self.state['enemy_move']), 
                    ('player', self.state['player_move'])
                ]
    
    # ========== MENSAJES ==========
    
    def set_message(self, text, time=1400):
        """
        Muestra un mensaje en pantalla por un tiempo determinado.
        
        Args:
            text: Texto del mensaje
            time: Duración en milisegundos
        """
        self.state['phase'] = 'message'
        self.state['message'] = text
        self.message_timer = pygame.time.get_ticks() + time
    
    # ========== MANEJO DE INPUT ==========
    
    def manejar_input(self, event):
        """
        Maneja la entrada del jugador durante la batalla.
        Solo procesa eventos KEYDOWN.
        
        Args:
            event: Evento de pygame
        """
        if event.type != pygame.KEYDOWN:
            return
        
        # === MENÚ PRINCIPAL ===
        if self.state['phase'] == 'menu':
            if event.key == pygame.K_DOWN:
                # Navegar hacia abajo
                self.state['menu_index'] = (self.state['menu_index'] + 1) % 4
            
            elif event.key == pygame.K_UP:
                # Navegar hacia arriba
                self.state['menu_index'] = (self.state['menu_index'] - 1) % 4
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_z:
                # Confirmar selección
                if self.state['menu_index'] == 0:  # Fight
                    self.state['phase'] = 'choose_move'
                    self.state['move_index'] = 0
                
                elif self.state['menu_index'] == 1:  # Bag
                    self.set_message("No tenés objetos. (Demo)", 1200)
                
                elif self.state['menu_index'] == 2:  # Pokémon
                    self.set_message("No podés cambiar en este demo.", 1200)
                
                elif self.state['menu_index'] == 3:  # Run (Escapar)
                    self.set_message("¡Escapaste de la batalla!", 1200)
                    self.battle_result = 'escape'
        
        # === MENÚ DE MOVIMIENTOS ===
        elif self.state['phase'] == 'choose_move':
            if not hasattr(self.player_pkm, 'movimientos'):
                return
            
            if event.key == pygame.K_DOWN:
                # Navegar hacia abajo
                self.state['move_index'] = (self.state['move_index'] + 1) % len(self.player_pkm.movimientos)
            
            elif event.key == pygame.K_UP:
                # Navegar hacia arriba
                self.state['move_index'] = (self.state['move_index'] - 1) % len(self.player_pkm.movimientos)
            
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_x:
                # Volver al menú principal
                self.state['phase'] = 'menu'
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_z:
                # Confirmar movimiento
                chosen_move = self.player_pkm.movimientos[self.state['move_index']]
                self.state['player_move'] = chosen_move
                
                # Enemigo elige su movimiento
                self.state['enemy_move'] = self.enemy_choose_move()
                
                # Decidir orden de turnos
                self.decide_turns()
                
                # Iniciar animación de ejecución
                self.state['phase'] = 'anim'
                self.state['anim'] = {'index': 0, 'sub': 0}
        
        # === PANTALLA FINAL ===
        elif self.state['phase'] == 'end':
            if event.key == pygame.K_RETURN or event.key == pygame.K_z:
                # Cerrar batalla
                self.terminar_batalla()
    
    # ========== ACTUALIZACIÓN ==========
    
    def actualizar(self):
        """
        Actualiza la lógica de la batalla cada frame.
        Maneja timers, animaciones y transiciones de estado.
        """
        if not self.active:
            return
        
        # === TIMER DE MENSAJES ===
        if self.state['phase'] == 'message':
            if pygame.time.get_ticks() > self.message_timer:
                # El mensaje terminó de mostrarse
                
                # Verificar si algún Pokémon se debilitó
                if self.player_pkm.esta_debilitado() or self.enemy_pkm.esta_debilitado():
                    self.state['phase'] = 'end'
                    
                    if self.player_pkm.esta_debilitado():
                        self.battle_result = 'lose'
                        self.set_message("Perdiste. Tus Pokémon se debilitaron.", 3000)
                    else:
                        self.battle_result = 'win'
                        self.set_message("¡Ganaste la batalla!", 3000)
                else:
                    # Volver al menú principal
                    self.state['phase'] = 'menu'
        
        # === ANIMACIONES DE TURNO ===
        if self.state['phase'] == 'anim' and self.state['anim'] is not None:
            anim = self.state['anim']
            
            # Verificar si quedan acciones por ejecutar
            if anim['index'] < len(self.state['turn_order']):
                who, mv = self.state['turn_order'][anim['index']]
                
                if anim['sub'] == 0:
                    # Ejecutar acción y mostrar resultado
                    result_text = self.execute_action(who, mv)
                    self.set_message(result_text, 1200)
                    anim['sub'] = 1
                else:
                    # Esperar a que termine el mensaje
                    if self.state['phase'] == 'message' and pygame.time.get_ticks() > self.message_timer:
                        # Pasar a la siguiente acción
                        anim['index'] += 1
                        anim['sub'] = 0
                        self.state['phase'] = 'anim'
            else:
                # Todas las acciones fueron ejecutadas
                self.state['anim'] = None
                
                # Verificar estado de los Pokémon
                if self.enemy_pkm.esta_debilitado():
                    self.set_message(f"{self.enemy_pkm.nombre} se debilitó!", 1500)
                elif self.player_pkm.esta_debilitado():
                    self.set_message(f"{self.player_pkm.nombre} se debilitó!", 1500)
                else:
                    # Continuar batalla
                    self.set_message("¿Qué harás?", 800)
                
                # Resetear movimientos elegidos
                self.state['player_move'] = None
                self.state['enemy_move'] = None
    
    # ========== RENDERIZADO ==========
    
    def draw_text(self, surface, text, x, y, color=(0, 0, 0)):
        """Dibuja texto en pantalla"""
        surf = self.font.render(text, True, color)
        surface.blit(surf, (x, y))
    
    def draw_hp_bar(self, surface, x, y, w, h, current, maximum):
        """
        Dibuja una barra de HP con color según porcentaje.
        
        Args:
            surface: Superficie de pygame donde dibujar
            x, y: Posición
            w, h: Ancho y alto de la barra
            current: PS actuales
            maximum: PS máximos
        """
        ratio = max(0, current) / maximum
        inner_w = int(w * ratio)
        
        # Fondo gris
        pygame.draw.rect(surface, (200, 200, 200), (x, y, w, h))
        
        # Color según porcentaje de vida
        if ratio > 0.5:
            color = (70, 200, 70)  # Verde
        elif ratio > 0.2:
            color = (230, 200, 60)  # Amarillo
        else:
            color = (220, 50, 50)  # Rojo
        
        pygame.draw.rect(surface, color, (x, y, inner_w, h))
        
        # Texto con PS actual/máximo
        self.draw_text(surface, f"{current}/{maximum}", x + w + 8, y)
    
    def dibujar(self, surface):
        """
        Dibuja toda la interfaz de batalla.
        
        Args:
            surface: Superficie de pygame donde dibujar (la pantalla completa)
        """
        if not self.active:
            return
        
        # === FONDO ===
        surface.fill((150, 200, 255))  # Cielo azul
        
        # === CAJA DEL POKÉMON ENEMIGO (arriba derecha) ===
        pygame.draw.rect(surface, WHITE, (430, 20, 340, 140), border_radius=6)
        self.draw_text(surface, f"{self.enemy_pkm.nombre} Lv{self.enemy_pkm.nivel}", 440, 28)
        self.draw_hp_bar(surface, 440, 56, 220, 20, 
                        self.enemy_pkm.ps_actual, 
                        self.enemy_pkm.stats_actuales['ps'])
        
        # Placeholder sprite enemigo (reemplazar con sprite real)
        pygame.draw.rect(surface, BLUE, (660, 35, 80, 80))
        
        # === CAJA DEL POKÉMON DEL JUGADOR (abajo izquierda) ===
        pygame.draw.rect(surface, WHITE, (20, 220, 360, 160), border_radius=6)
        self.draw_text(surface, f"{self.player_pkm.nombre} Lv{self.player_pkm.nivel}", 30, 228)
        self.draw_hp_bar(surface, 30, 256, 220, 20, 
                        self.player_pkm.ps_actual, 
                        self.player_pkm.stats_actuales['ps'])
        
        # Placeholder sprite jugador (reemplazar con sprite real)
        pygame.draw.rect(surface, RED, (220, 250, 100, 100))
        
        # === CAJA DE MENSAJE ===
        pygame.draw.rect(surface, WHITE, (20, 390, 760, 70), border_radius=6)
        if self.state['phase'] == 'message':
            self.draw_text(surface, self.state['message'], 32, 404)
        else:
            self.draw_text(surface, "¿Qué harás?", 32, 404)
        
        # === MENÚ PRINCIPAL (Fight/Bag/Pokémon/Run) ===
        if self.state['phase'] == 'menu':
            mx, my = 420, 230
            w, h = 360, 150
            pygame.draw.rect(surface, WHITE, (mx, my, w, h), border_radius=6)
            
            options = ["Fight", "Bag", "Pokémon", "Run"]
            for i, opt in enumerate(options):
                x = mx + 12
                y = my + 12 + i * 30
                # Resaltar opción seleccionada en azul
                color = (0, 0, 0) if i != self.state['menu_index'] else BLUE
                self.draw_text(surface, opt, x, y, color)
        
        # === MENÚ DE MOVIMIENTOS ===
        elif self.state['phase'] == 'choose_move':
            if hasattr(self.player_pkm, 'movimientos') and self.player_pkm.movimientos:
                mx, my = 420, 230
                w, h = 360, 150
                pygame.draw.rect(surface, WHITE, (mx, my, w, h), border_radius=6)
                
                for i, mv in enumerate(self.player_pkm.movimientos):
                    x = mx + 12
                    y = my + 12 + i * 30
                    # Resaltar movimiento seleccionado en azul
                    color = (0, 0, 0) if i != self.state['move_index'] else BLUE
                    self.draw_text(surface, f"{mv.name}  PP:{mv.pp}/{mv.max_pp}", x, y, color)
        
        # === INDICADORES DE DEBILITADO ===
        if self.player_pkm.esta_debilitado():
            self.draw_text(surface, f"{self.player_pkm.nombre} debilitado", 30, 300, RED)
        
        if self.enemy_pkm.esta_debilitado():
            self.draw_text(surface, f"{self.enemy_pkm.nombre} debilitado", 440, 120, RED)
