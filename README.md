CINEMATIC MOVIE SEAT BOOKING UI
===============================

A beautifully designed, interactive movie theater seat booking application built entirely with Python and the Flet framework. This project highlights programmatic UI generation, dynamic state management, and modern dark-mode aesthetics, all while remaining 100% compliant with strict static type checkers like Pylance.

FEATURES
--------
* Programmatic Grid Generation: Uses Python 'for' loops to automatically render the theater layout, seamlessly injecting a central aisle and randomly pre-reserving seats to simulate real-world app conditions.
* Ambient Lighting & Design: Features a glowing projector screen effect achieved by layering Flet's 'LinearGradient' and heavily blurred 'BoxShadow' properties, entirely without external image assets.
* Interactive Micro-Animations: Clicking an available seat triggers a satisfying 1.1x scale "pop" animation using Flet's 'EASE_OUT_BACK' curve, changing the seat to a vibrant Neon Blue.
* Dynamic State Engine: Real-time math calculates the total ticket price as seats are toggled. Clicking "BOOK TICKETS" scans the global state, converts selected seats to locked/reserved, and resets the counters.
* Pylance Optimized: Written with explicit typing and variable isolation to completely eliminate "Control | None" and strict-mode static checker errors.

TECH STACK
----------
* Language: Python 3.8+
* Framework: Flet (v0.80.0+)
* Key Concepts: List Iteration, Matrix UI Layouts, Global State Mutations, Transform Animations

HOW TO RUN
----------
1. Ensure Flet is installed on your machine:
   pip install flet
2. Run the application from your terminal:
   python booking.py

HOW TO USE
----------
1. Look at the generated theater grid. Red seats are taken; dark gray seats are available.
2. Click any dark gray seat to select it. Watch it pop and turn neon blue.
3. Notice the bottom checkout bar instantly calculating the total price based on a $15 per-seat rate.
4. Click "BOOK TICKETS" to finalize the reservation. The button will flash "SUCCESS!", your selected seats will permanently turn red, and the total price will reset to $0.
