# 🧮 Computacao Movel TP1 - Scientific Calculator with History

A cross platform scientific calculator built with **Python** and **Flet**. This calculator combines symbolic mathematics with a modern, responsive UI and a robust history persistency system.

---

## ✨ Key Features

* **Advanced Mathematics:** Powered by `SymPy` for accurate evaluation of trigonometry ($\sin, \cos, \tan$), logarithms ($\ln$), square roots ($\sqrt{}$), and powers ($x^y$).
* **Persistent History:** To ensure the calculations aren't lost it uses `DuckDB` and `Parquet` to store the history locally for quick access.
* **Dynamic UI:**
    * 🌗 **Theme Toggle:** Support for switching between Dark and Light modes.
    * 📱 **Dynamic Design:** Optimized for both Desktop and Mobile layouts.
    * 📋 **Clipboard Integration:** Copy results instantly from your history.
* **User Experience:**
    * **Keyboard Support:** Fully mapped for keyboard use.
    * **History Management:** Individual entry deletion or bulk viewing.

---

## 🛠️ Technologies

| Library | Purpose |
| :--- | :--- |
| **Flet** | Flutter-based UI framework for Python. |
| **SymPy** | Symbolic mathematics for high-precision calculations. |
| **DuckDB** | In-process analytical database for persistent history. |
| **Pyperclip** | Cross-platform clipboard management. |

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.8 or higher installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/calc-pro.git](https://github.com/yourusername/calc-pro.git)
cd calc-pro
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Launch the App
```bash
python main.py
```
---

## 📄 Project Info

This project was developed for the class **Computação Móvel** as the  **(TP1)** . It serves as an exercise to learn the use of flet and integrating software development with mobile platforms..

**Authors:** [Juan Pablo Mahecha Ortiz, Martin Mahecha Ortiz ]

