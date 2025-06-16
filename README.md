# 🗣️ Traductor con Audio y Descarga

Este proyecto es una aplicación web construida con **Streamlit** que permite traducir texto o audio a diferentes idiomas, generar audio con la traducción y practicar con ejercicios interactivos. Ideal para aprender idiomas de forma dinámica y entretenida.

---

## 🚀 Funcionalidades

- 🎙️ **Transcripción y traducción de audio (.mp3/.wav)** usando Whisper.
- ✍️ **Traducción manual de texto** con soporte multilenguaje.
- 🔊 **Generación de audio de la traducción** con descarga incluida (usando gTTS).
- 🧩 **Ejercicios automáticos** para practicar:
  - Elegir la traducción correcta.
  - Completar una frase.
  - Ordenar las palabras.

---

## 🛠️ Tecnologías utilizadas

- [Streamlit](https://streamlit.io/) — para la interfaz web.
- [OpenAI] - para la traduccion del Texto
- [Googletrans](https://pypi.org/project/googletrans/) — traducción automática.
- [gTTS](https://pypi.org/project/gTTS/) — generación de audio con texto traducido.
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) — modelo de transcripción automática.
- Otros: `tempfile`, `base64`, `random`, etc.

---

## 📦 Instalación

> Requisitos: Python 3.8 a 3.11, `pip`, y opcionalmente `virtualenv`.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv traductor_env
# Activar el entorno
# Windows:
.\traductor_env\Scripts\activate
# macOS/Linux:
source traductor_env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> ⚠️ Si tenés problemas con `openai-whisper` o `googletrans`, podés instalar así:

```bash
pip install git+https://github.com/openai/whisper.git
pip install googletrans==4.0.0rc1
```

---

## ▶️ Cómo ejecutar

Ejecutá el siguiente comando en la raíz del proyecto:

```bash
streamlit run app.py
```

Se abrirá una pestaña en tu navegador con la app en `http://localhost:8501`.

---

## 🌍 Idiomas Soportados

- 🇪🇸 Español
- 🇬🇧 Inglés
- 🇫🇷 Francés
- 🇩🇪 Alemán
- 🇮🇹 Italiano
- 🇵🇹 Portugués
- 🇷🇺 Ruso
- 🇨🇳 Chino (simplificado)

---

## 📁 Estructura del Proyecto

```
├── app.py                # Código principal de la app
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
```

---
