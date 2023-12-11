import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango

class TrafficMonitorApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Proyecto final")
        self.set_default_size(800, 600)

        # Main Container
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_bg_color = Gdk.RGBA(1, 1, 1, 1)
        self.override_background_color(main_container, main_bg_color)

        # Navbar
        navbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        navbar_bg_color = Gdk.RGBA(0, 0, 0, 0)
        self.override_background_color(navbar_box, navbar_bg_color)

        toggle_button = Gtk.Button(label="☰")
        toggle_button.connect("clicked", self.toggle_sidebar)
        toggle_button_color = Gdk.RGBA(0, 0, 0, 1)
        toggle_button.override_color(Gtk.StateFlags.NORMAL, toggle_button_color)
        toggle_button.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))  # Fondo blanco
        navbar_box.pack_start(toggle_button, False, False, 0)

        program_name_label = Gtk.Label(label="Monitor de tráfico")
        program_name_label.set_margin_start(20)
        program_name_label.set_margin_end(20)
        program_name_label.set_margin_top(10)
        program_name_label.set_margin_bottom(10)
        text_color = Gdk.RGBA(0, 0, 0, 1)
        program_name_label.override_color(Gtk.StateFlags.NORMAL, text_color)
        program_name_label.override_font(Pango.FontDescription("Karla 24"))
        program_name_label.set_alignment(0, 0.5)
        navbar_box.pack_start(program_name_label, True, True, 0)

        main_container.pack_start(navbar_box, False, False, 0)

        # Sidebar
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sidebar_bg_color = Gdk.RGBA(0, 0, 0, 0.05)
        self.override_background_color(sidebar_box, sidebar_bg_color)
        sidebar_box.set_visible(False)  # Oculta la barra lateral por defecto

        text_color_sidebar = Gdk.RGBA(0, 0, 0, 1)
        self.add_sidebar_item(sidebar_box, "📅", "Gráfica 1", text_color_sidebar)
        self.add_sidebar_item(sidebar_box, "📅", "Gráfica 2", text_color_sidebar)
        self.add_sidebar_item(sidebar_box, "📅", "Gráfica 3", text_color_sidebar)

        sidebar_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        sidebar_container.pack_start(sidebar_box, False, False, 0)

        main_container.pack_start(sidebar_container, False, False, 0)

        # Content
        content_box = Gtk.Box(spacing=20)
        content_bg_color = Gdk.RGBA(1, 1, 1, 1)
        self.override_background_color(content_box, content_bg_color)

        # Rest of your content code...

        main_container.pack_start(content_box, True, True, 0)

        # Show the window
        self.add(main_container)
        self.show_all()

    def override_background_color(self, widget, rgba_color):
        widget.override_background_color(Gtk.StateFlags.NORMAL, rgba_color)

    def add_sidebar_item(self, parent_box, icon, label_text, text_color):
        item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        item_box.set_margin_start(20)
        item_box.set_margin_end(20)
        item_box.set_margin_top(20)
        item_box.set_margin_bottom(20)

        icon_label = Gtk.Label(label=icon)
        icon_label.set_markup(f"<span size='normal' weight='bold'>{icon}</span>")
        icon_label.override_color(Gtk.StateFlags.NORMAL, text_color)
        icon_label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))  # Fondo blanco
        item_box.pack_start(icon_label, False, False, 0)

        graph_label = Gtk.Label(label=label_text)
        graph_label.set_markup(f"<span size='normal' weight='normal'>{label_text}</span>")
        graph_label.override_font(Pango.FontDescription("Karla 14"))
        graph_label.override_color(Gtk.StateFlags.NORMAL, text_color)
        item_box.pack_start(graph_label, True, True, 0)

        parent_box.pack_start(item_box, False, False, 0)

    def toggle_sidebar(self, button):
        sidebar = self.get_child().get_children()[1].get_children()[0]
        sidebar.set_visible(not sidebar.get_visible())

if __name__ == "__main__":
    app = TrafficMonitorApp()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()
