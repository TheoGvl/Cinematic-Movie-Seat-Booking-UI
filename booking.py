import flet as ft
import random

def main(page: ft.Page):
    # Setup the main window properties
    page.title = "Cinematic Seat Booking"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0D0D0F" # Deep theater black
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- Application State ---
    TICKET_PRICE = 15
    state = {
        "selected_seats": 0 # Tracks how many seats the user has currently clicked
    }
    
    # List to hold references to all seat objects so we can update them globally later
    all_seats_list = []

    # --- Interactive Logic ---
    
    # This function triggers every time a user clicks a seat container
    def seat_clicked(e):
        seat = e.control
        
        # If the seat is already bought/reserved by someone else, do nothing
        if seat.data == "reserved":
            return
            
        # If the seat is open, select it
        if seat.data == "available":
            seat.bgcolor = "#00D1FF" # Turn Neon Blue
            seat.data = "selected"   # Update internal status
            state["selected_seats"] += 1
            seat.scale = ft.Scale(scale=1.1) # Pop out animation
        
        # If the seat was already selected by the user, un-select it
        else:
            seat.bgcolor = "#2C2C30" # Back to Dark Gray
            seat.data = "available"  # Revert internal status
            state["selected_seats"] -= 1
            seat.scale = ft.Scale(scale=1.0) # Shrink back to normal
            
        # Dynamically calculate and update the checkout bar text
        selected_text.value = f"Selected: {state['selected_seats']} seats"
        total_text.value = f"Total: ${state['selected_seats'] * TICKET_PRICE}"
        
        # Reset the checkout button back to default in case it previously said "SUCCESS!"
        book_btn_text.value = "BOOK TICKETS"
        book_btn.bgcolor = "#00D1FF"
        
        # Tell Flet to redraw the screen with the new changes
        page.update()

    # Helper function to generate individual seat containers
    def create_seat(is_reserved: bool = False):
        color = "#B71C1C" if is_reserved else "#2C2C30" # Red if reserved, Gray if open
        status = "reserved" if is_reserved else "available"
        
        seat_obj = ft.Container(
            width=30,
            height=30,
            bgcolor=color,
            border_radius=8, # Softly rounded edges
            margin=ft.margin.all(4),
            data=status, # Store the status inside the object for easy access
            on_click=seat_clicked,
            
            # Pylance-safe animation initializers
            scale=ft.Scale(scale=1.0),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT), 
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK)
        )
        all_seats_list.append(seat_obj) # Add it to our global tracking list
        return seat_obj

    # --- UI Components ---

    # The Glowing Movie Screen at the top
    screen = ft.Container(
        height=60,
        width=420, 
        # A gradient fading into the background creates a projector light effect
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#00D1FF", "#121212"]
        ),
        border_radius=ft.border_radius.only(top_left=50, top_right=50),
        shadow=ft.BoxShadow(spread_radius=5, blur_radius=50, color="#4D00D1FF")
    )

    # Building the Seat Grid dynamically
    seat_rows = []
    for row in range(7): # 7 Rows deep
        row_seats = []
        for col in range(9): # Reduced to 9 columns for a perfect fit (4 seats, 1 aisle, 4 seats)
            
            # Create a physical "Aisle" down the exact center
            if col == 4:
                row_seats.append(ft.Container(width=25)) 
                
            # Randomly pre-reserve some seats (30% chance) to make it look like a real app
            is_res = random.random() < 0.3 
            row_seats.append(create_seat(is_res))
            
        seat_rows.append(ft.Row(controls=row_seats, alignment=ft.MainAxisAlignment.CENTER))

    # Legend Display mapping colors to meanings
    def create_legend_item(color: str, text: str):
        return ft.Row([
            ft.Container(width=15, height=15, bgcolor=color, border_radius=5),
            ft.Text(text, size=14, color="#8E8E93")
        ])
        
    legend = ft.Row(
        controls=[
            create_legend_item("#2C2C30", "Available"),
            create_legend_item("#B71C1C", "Reserved"),
            create_legend_item("#00D1FF", "Selected")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Checkout Bar UI Elements (isolated variables to satisfy Pylance typing)
    selected_text = ft.Text("Selected: 0 seats", size=14, color="#8E8E93")
    total_text = ft.Text("Total: $0", size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    book_btn_text = ft.Text("BOOK TICKETS", weight=ft.FontWeight.BOLD, color="#000000")
    
    # Logic for when the user finalizes their booking
    def attempt_booking(e):
        if state["selected_seats"] > 0:
            
            # Loop through all seats and lock in the selected ones
            for seat in all_seats_list:
                if seat.data == "selected":
                    seat.bgcolor = "#B71C1C" # Turn them Red (Reserved)
                    seat.data = "reserved"
                    seat.scale = ft.Scale(scale=1.0) # Flatten them out
            
            # Reset the counter and UI text back to zero
            state["selected_seats"] = 0
            selected_text.value = "Selected: 0 seats"
            total_text.value = "Total: $0"
            
            # Visual feedback on the button itself
            book_btn_text.value = "SUCCESS!"
            book_btn.bgcolor = "#34C759" 
        else:
            # Error feedback if no seats were picked
            book_btn_text.value = "NO SEATS!"
            book_btn.bgcolor = "#FF453A" 
            
        page.update()
    
    book_btn = ft.Container(
        content=book_btn_text, 
        bgcolor="#00D1FF",
        padding=ft.padding.symmetric(horizontal=30, vertical=15),
        border_radius=10,
        ink=True, # Ripple effect on click
        on_click=attempt_booking 
    )

    checkout_bar = ft.Row(
        controls=[
            ft.Column([selected_text, total_text], spacing=2),
            book_btn
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=440 
    )

    # --- Layout Assembly ---
    # Wrap everything in a main application card
    app_layout = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("SELECT SEATS", size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Container(height=20),
                screen,
                ft.Container(height=30),
                
                # Unpack the generated rows
                ft.Column(controls=seat_rows, spacing=0),
                
                ft.Container(height=30),
                legend,
                ft.Divider(height=40, color="#2C2C2E"),
                checkout_bar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=550, 
        bgcolor="#1C1C1E",
        padding=40,
        border_radius=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=30, color="#50000000")
    )

    page.add(app_layout)

ft.run(main)