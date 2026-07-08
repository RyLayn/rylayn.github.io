# ⚡ Tabla de Tipos Pokémon — Referencia universal

**🔗 Página en vivo: [rylayn.github.io](https://rylayn.github.io)**

Herramienta interactiva de consulta de tipos Pokémon en **español latinoamericano**, hecha para usarse en plena batalla desde el celular o la PC. Funciona **sin internet**, cubre **todas las generaciones** y se **actualiza sola** con un botón.

---

## ✨ Características

### 🔍 El lente de tipos
Toca cualquiera de los 18 tipos y toda la tabla reacciona: se iluminan en **verde** los tipos a los que les gana y en **rojo** los que le ganan a él. La ficha muestra el detalle completo al atacar (×2, ×½, ×0) y al defender (débil, resiste, inmune).

### 🎮 Selector de generación
La tabla de tipos es universal desde 2013, pero cambió dos veces en la historia — y esta página las cubre todas:

| Modo | Juegos | Diferencias |
|---|---|---|
| **Juegos modernos** (por defecto) | X/Y, Sol/Luna, Espada/Escudo, Escarlata/Púrpura, Leyendas Arceus, **Leyendas Z-A**, Champions | Tabla actual de 18 tipos |
| **Oro/Plata → Blanco/Negro 2** | 2.ª a 5.ª generación | Sin tipo Hada; el Acero resistía Fantasma y Siniestro |
| **Rojo/Azul/Amarillo** | 1.ª generación | 15 tipos; Insecto y Veneno se ganaban mutuamente; Fantasma no dañaba a Psíquico (bug histórico); el Fuego no resistía Hielo |

### 🐉 Buscador de Pokémon (1,241 entradas)
Escribe —o **dicta con voz** 🎤— el nombre de cualquier Pokémon y te dice:

- **Cómo atacarlo**: qué tipos le pegan ×4 (letal) y ×2, qué resiste y a qué es inmune.
- **Cómo ataca él**: contra qué tipos son fuertes sus ataques, contra cuáles son poco eficaces y a cuáles no daña.
- **Modo batalla con Megas**: pastillas para alternar entre Forma base / Mega / Mega X / Mega Y / Mega Z, con aviso cuando la Mega **cambia de tipo** (ej. Gyarados pasa a Agua/Siniestro y sus debilidades ya no son las mismas).

Incluye **todas las formas**: las 48 Megaevoluciones clásicas, las **Megas nuevas de Leyendas Z-A** (Mega Dragonite, Mega Feraligatr, Mega Excadrill, las formas Z y más), formas regionales de Alola/Galar/Hisui/Paldea, los 5 Rotom, las máscaras de Ogerpon, etc. Cada forma con **su propio icono**.

### 📊 Matriz completa 18×18
La tabla clásica de ataque vs. defensa, con encabezados fijos y optimizada para deslizar en el celular.

### 🧠 Trucos para memorizarla
Los triángulos básicos (Fuego → Planta → Agua), la lógica cotidiana de cada relación y las 8 inmunidades.

### 🔄 Botón "Actualizar datos"
Descarga el Pokédex más reciente de **Pokémon Showdown**, con barra de progreso por etapas, lista de novedades ("+N Pokémon/formas nuevas") y guardado en el dispositivo. A prueba de fallos: todo lo descargado pasa una **validación estricta** antes de aplicarse — si algo llega mal o no hay internet, los datos actuales quedan intactos. Incluye enlace para restablecer los originales.

### 📴 Funciona sin internet
Los iconos de los 1,241 Pokémon van **incrustados dentro del propio HTML** (una sola hoja de sprites en base64). Sin conexión solo se pierden las fuentes decorativas y los sprites grandes; todo lo demás funciona igual.

---

## 📱 Cómo usarla

1. Abre **[rylayn.github.io](https://rylayn.github.io)** en cualquier navegador.
2. En Android: menú ⋮ → **"Agregar a pantalla principal"** para tenerla como app.
3. La búsqueda por voz pide permiso de micrófono la primera vez (requiere abrirla desde la dirección web, no como archivo local).

---

## 🛠️ Tecnología

- **Un solo archivo HTML** — sin frameworks, sin dependencias, sin build.
- Datos de Pokémon y formas: [Pokémon Showdown](https://play.pokemonshowdown.com) (Smogon).
- Reconocimiento de voz: Web Speech API (es-MX).
- Todas las animaciones respetan la preferencia de **movimiento reducido** del sistema.
- Tema oscuro puro, optimizado para pantallas AMOLED.

---

## ✍️ Autor y licencia

**Hecho por AC - RyLayn** — [github.com/RyLayn](https://github.com/RyLayn)

© 2026 AC - RyLayn. Esta herramienta es de **uso libre y gratuito** para todos los usuarios. Queda **prohibido usurpar la autoría**, retirar los créditos o redistribuir la página modificada haciéndola pasar como propia.

Proyecto de fans sin fines de lucro. Pokémon es una marca de Nintendo / Creatures Inc. / GAME FREAK Inc.
