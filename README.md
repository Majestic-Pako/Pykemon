# 🐾 **Pykemon — Aventura estilo Pokémon en Pygame**

<div align="center">

🎮 **Proyecto final inspirado en Pokémon, programado en Python + Pygame**  
🌲 Exploración • 💬 NPCs con diálogos • ⚔️ Combates • 🗺️ Mapas creados con Tiled

---

## 🏷️ **Tecnologías Utilizadas**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5-00cc66?style=for-the-badge&logo=python&logoColor=white)
![Tiled](https://img.shields.io/badge/Tiled_Map_Editor-1.10-blue?style=for-the-badge&logo=tiled&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-Data_Files-000000?style=for-the-badge&logo=json&logoColor=white)

---

## 📦 **Instalación (Dependencias)**

```bash
pip install pygame
```
```bash
pip install pytmx
```

---

</div>

---

# 🗂️ **Estructura Completa del Proyecto**

```
📦 Pykemon
│
├── assets/                     # Recursos visuales del juego
│   ├── images/                 # UI, fondos, presentación
│   ├── maps/                   # Mapas .tmx creados con Tiled
│   ├── pokemon/                # Sprites front y back de los Pokémon
│   │   ├── front/
│   │   └── back/
│   ├── sprites/                # Sprites del jugador y NPCs
│   │   ├── npcs/
│   │   └── player/
│   └── tilesets/               # Tilesets usados dentro de Tiled
│
├── data/                       # Archivos JSON de datos base
│   ├── dialogues.json
│   ├── movements.json
│   ├── movset.json
│   ├── objects.json
│   ├── pokemon.json
│   └── type.json
│
├── core/
│   ├── entities/               # Entidades dinámicas
│   │   ├── movement.py
│   │   ├── npc.py
│   │   ├── player.py
│   │   └── pokemon.py
│   │
│   ├── system/                 # Reglas del juego
│   │   ├── batalla.py
│   │   ├── camera.py
│   │   ├── config.py
│   │   ├── map.py
│   │   └── portal_manager.py
│   │
│   └── ui/                     # Interfaz de usuario
│       ├── batalla_ui.py
│       ├── bolsa_menu.py
│       ├── dialog.py
│       ├── MenuManager.py
│       ├── pantalla_inicio.py
│       ├── pokemon_menu.py
│       └── use_object_menu.py
│
├── main.py                     # Punto de entrada del juego
├── requirements.txt
└── README.md
```

---

# 🧭 **Roadmap del Proyecto**

A continuación, las versiones establecidas durante el desarrollo.

---

## 🧩 **Versión 0.1 – Esqueleto del Juego**

Primer armado técnico del proyecto:

- Carpeta base del motor del juego (`core/`)
- Configuración inicial: tamaño de pantalla, FPS, constantes
- Carga básica del mapa
- Movimiento simple del jugador con colisiones básicas
- Cámara siguiendo al jugador  
- Placeholder para futuras expansiones

---

## 🧱 **Versión 0.2 – Mundo con NPCs y Diálogos**

Expansión del mundo jugable:

- Sistema de NPCs con posiciones definidas en Tiled
- Lectura de diálogos desde `dialogues.json`
- Caja de diálogo animada
- Detección de interacción usando colisiones ampliadas
- Primer comportamiento tipo RPG

---

## ⚙️ **Versión 0.2.5 — Planificación de Inventario y Datos Base**

Diseño de la arquitectura de datos del MVP:

- Definición de **data estática** via JSON: Pokémon, tipos, objetos, movimientos
- Clase `Pokemon` con stats dinámicas y lectura de base stats del JSON
- Inventario mínimo dentro del jugador (cantidades, dinero)
- Simplificación temporal: sin XP real, sin estados alterados
- Base para futuro sistema de combate

---

## ⚔️ **Versión 0.3 — Sistema de Combate Básico**

Primer combate funcional:

- Detección de zonas de encuentro en Tiled
- Pantalla de combate (UI básica)  
- Sistema de turnos: atacar, recibir daño, lógica de KO
- Lectura de ataques desde `movements.json` y `movset.json`
- Retorno al mapa al finalizar el combate

---

## 🏗️ **Versión 0.4 — Mundo funcional (MVP)**

Entrega mínima jugable:

- Exploración completa del mapa inicial
- Combates funcionando
- NPCs interactivos
- Menú Pokémon, inventario y diálogos integrados
- Transiciones entre mapas (portal manager)
- Flujo completo desde inicio hasta exploración + combate

---

# 👥 **Equipo de Desarrollo**

| Miembro | Roles |
|--------|--------|
| **Majestic-Pako (Agustín Choque)** | ![Dev](https://img.shields.io/badge/Programador_Principal-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Arquitectura](https://img.shields.io/badge/Arquitectura_del_Juego-4B7BEC?style=for-the-badge) ![GameDesign](https://img.shields.io/badge/Game_Design-9B59B6?style=for-the-badge) |
| **EstebanRacana (Esteban)** | ![Programador](https://img.shields.io/badge/Programador-2ECC71?style=for-the-badge&logo=python&logoColor=white) |
| **tomy2311 (Thomas)** | ![Programador](https://img.shields.io/badge/Programador-2ECC71?style=for-the-badge) ![Tester](https://img.shields.io/badge/Beta_Tester-F1C40F?style=for-the-badge) |
| **Anthony2080 (ToñoShark)** | ![Diseño](https://img.shields.io/badge/Diseño-FF5733?style=for-the-badge&logo=adobephotoshop&logoColor=white) |

---
