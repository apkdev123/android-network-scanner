"""
Android Network Security Scanner
Build with Kivy for Android
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import threading
import socket
import subprocess
import platform
import psutil
import json
from datetime import datetime
import os

class NetworkScannerApp(App):
    def build(self):
        # Set window background
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        # Create main layout
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        title = Label(
            text='📱 Network Security Scanner',
            font_size='24sp',
            bold=True,
            size_hint=(1, 0.1),
            color=(0, 0.8, 1, 1)
        )
        self.layout.add_widget(title)
        
        # Create tabs
        self.tabs = TabbedPanel(
            do_default_tab=False,
            tab_height='50sp',
            background_color=(0.15, 0.15, 0.2, 1)
        )
        
        # Tab 1: Network Scanner
        scanner_tab = TabbedPanelItem(text='🔍 Scanner')
        scanner_content = self.create_scanner_tab()
        scanner_tab.add_widget(scanner_content)
        self.tabs.add_widget(scanner_tab)
        
        # Tab 2: System Info
        info_tab = TabbedPanelItem(text='📊 System Info')
        info_content = self.create_info_tab()
        info_tab.add_widget(info_content)
        self.tabs.add_widget(info_tab)
        
        # Tab 3: Port Scanner
        port_tab = TabbedPanelItem(text='🚪 Ports')
        port_content = self.create_port_tab()
        port_tab.add_widget(port_content)
        self.tabs.add_widget(port_tab)
        
        # Tab 4: Settings
        settings_tab = TabbedPanelItem(text='⚙️ Settings')
        settings_content = self.create_settings_tab()
        settings_tab.add_widget(settings_content)
        self.tabs.add_widget(settings_tab)
        
        self.layout.add_widget(self.tabs)
        
        # Status bar
        self.status_label = Label(
            text='Ready',
            size_hint=(1, 0.05),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.layout.add_widget(self.status_label)
        
        return self.layout
    
    def create_scanner_tab(self):
        """Create network scanner tab"""
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        # IP range input
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        input_layout.add_widget(Label(text='IP Range:', size_hint=(0.3, 1)))
        
        self.ip_input = TextInput(
            text='192.168.1.1/24',
            multiline=False,
            size_hint=(0.7, 1),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        input_layout.add_widget(self.ip_input)
        layout.add_widget(input_layout)
        
        # Scan button
        scan_btn = Button(
            text='🔍 Start Network Scan',
            size_hint=(1, 0.15),
            background_color=(0, 0.6, 0.8, 1),
            background_normal=''
        )
        scan_btn.bind(on_press=self.start_network_scan)
        layout.add_widget(scan_btn)
        
        # Results display
        scroll = ScrollView(size_hint=(1, 0.7))
        self.results_label = Label(
            text='Scan results will appear here...\n\n',
            size_hint_y=None,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            color=(1, 1, 1, 1),
            font_size='14sp'
        )
        self.results_label.bind(texture_size=self.results_label.setter('size'))
        scroll.add_widget(self.results_label)
        layout.add_widget(scroll)
        
        return layout
    
    def create_info_tab(self):
        """Create system information tab"""
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Refresh button
        refresh_btn = Button(
            text='🔄 Refresh System Info',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.5, 0, 1)
        )
        refresh_btn.bind(on_press=self.refresh_system_info)
        layout.add_widget(refresh_btn)
        
        # System info display
        scroll = ScrollView()
        self.info_label = Label(
            text='',
            size_hint_y=None,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            color=(1, 1, 1, 1),
            font_size='14sp'
        )
        self.info_label.bind(texture_size=self.info_label.setter('size'))
        scroll.add_widget(self.info_label)
        layout.add_widget(scroll)
        
        # Initial load
        Clock.schedule_once(lambda dt: self.refresh_system_info(None), 0.5)
        
        return layout
    
    def create_port_tab(self):
        """Create port scanner tab"""
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Target input
        target_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        target_layout.add_widget(Label(text='Target IP:', size_hint=(0.3, 1)))
        
        self.target_input = TextInput(
            text='192.168.1.1',
            multiline=False,
            size_hint=(0.7, 1),
            background_color=(0.2, 0.2, 0.2, 1)
        )
        target_layout.add_widget(self.target_input)
        layout.add_widget(target_layout)
        
        # Ports input
        ports_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        ports_layout.add_widget(Label(text='Ports:', size_hint=(0.3, 1)))
        
        self.ports_input = TextInput(
            text='80,443,22,21,25,53,3389',
            multiline=False,
            size_hint=(0.7, 1),
            background_color=(0.2, 0.2, 0.2, 1)
        )
        ports_layout.add_widget(self.ports_input)
        layout.add_widget(ports_layout)
        
        # Scan button
        port_btn = Button(
            text='🔍 Scan Ports',
            size_hint=(1, 0.15),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        port_btn.bind(on_press=self.start_port_scan)
        layout.add_widget(port_btn)
        
        # Results display
        scroll = ScrollView(size_hint=(1, 0.55))
        self.port_results_label = Label(
            text='Port scan results...\n',
            size_hint_y=None,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            color=(1, 1, 1, 1)
        )
        self.port_results_label.bind(texture_size=self.port_results_label.setter('size'))
        scroll.add_widget(self.port_results_label)
        layout.add_widget(scroll)
        
        return layout
    
    def create_settings_tab(self):
        """Create settings tab"""
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        
        # Theme toggle
        theme_btn = Button(
            text='🌙 Toggle Dark/Light Theme',
            size_hint=(1, 0.15),
            background_color=(0.5, 0.3, 0.8, 1)
        )
        theme_btn.bind(on_press=self.toggle_theme)
        layout.add_widget(theme_btn)
        
        # Clear logs
        clear_btn = Button(
            text='🗑️ Clear All Logs',
            size_hint=(1, 0.15),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        clear_btn.bind(on_press=self.clear_logs)
        layout.add_widget(clear_btn)
        
        # Export logs
        export_btn = Button(
            text='📤 Export Scan Results',
            size_hint=(1, 0.15),
            background_color=(0.3, 0.8, 0.3, 1)
        )
        export_btn.bind(on_press=self.export_results)
        layout.add_widget(export_btn)
        
        # About
        about_label = Label(
            text='\n📱 Android Network Scanner v1.0\n\n'
                 'Built with Kivy & Python\n'
                 'GitHub Actions Auto-Build\n'
                 'For security testing only\n\n'
                 '⚠️ Use responsibly!',
            halign='center',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(about_label)
        
        return layout
    
    def start_network_scan(self, instance):
        """Start network scanning in background thread"""
        self.update_status("Scanning network...")
        self.results_label.text = "🔍 Scanning network...\n\n"
        
        def scan_thread():
            try:
                target = self.ip_input.text
                results = []
                
                # Simple ping scan for demo
                if '/' in target:
                    base_ip = target.split('/')[0]
                    base = '.'.join(base_ip.split('.')[:3])
                    
                    for i in range(1, 11):  # Scan first 10 IPs
                        ip = f"{base}.{i}"
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.3)
                            result = sock.connect_ex((ip, 80))
                            sock.close()
                            
                            if result == 0:
                                hostname = self.get_hostname(ip)
                                results.append(f"✅ {ip} - {hostname}")
                            else:
                                results.append(f"❌ {ip} - Offline")
                                
                            # Update UI progressively
                            Clock.schedule_once(lambda dt, r=results.copy(): 
                                                self.update_scan_results(r), 0)
                                
                        except:
                            pass
                
                # Update final results
                Clock.schedule_once(lambda dt: self.finalize_scan(results), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_error(str(e)), 0)
        
        threading.Thread(target=scan_thread).start()
    
    def start_port_scan(self, instance):
        """Start port scanning"""
        self.update_status("Scanning ports...")
        self.port_results_label.text = "Scanning ports...\n\n"
        
        def port_scan_thread():
            try:
                target = self.target_input.text
                ports = [int(p.strip()) for p in self.ports_input.text.split(',')]
                
                open_ports = []
                for port in ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((target, port))
                        
                        if result == 0:
                            service = self.get_service_name(port)
                            open_ports.append(f"🚪 Port {port} OPEN - {service}")
                        else:
                            open_ports.append(f"🔒 Port {port} closed")
                        
                        sock.close()
                        
                        # Update progress
                        Clock.schedule_once(lambda dt, p=port: 
                                          self.update_port_scan(p, ports), 0)
                                          
                    except:
                        pass
                
                # Show results
                Clock.schedule_once(lambda dt, op=open_ports: 
                                  self.show_port_results(op), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_port_error(str(e)), 0)
        
        threading.Thread(target=port_scan_thread).start()
    
    def refresh_system_info(self, instance):
        """Refresh system information"""
        info_lines = []
        
        # System info
        info_lines.append("=== SYSTEM INFORMATION ===\n")
        info_lines.append(f"Platform: {platform.system()} {platform.release()}")
        info_lines.append(f"Architecture: {platform.machine()}")
        info_lines.append(f"Python: {platform.python_version()}")
        
        # Network info
        info_lines.append("\n=== NETWORK ===\n")
        try:
            hostname = socket.gethostname()
            info_lines.append(f"Hostname: {hostname}")
            
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            info_lines.append(f"Local IP: {local_ip}")
        except:
            info_lines.append("Network: Unavailable")
        
        # Memory info
        info_lines.append("\n=== MEMORY ===\n")
        try:
            mem = psutil.virtual_memory()
            info_lines.append(f"Total: {mem.total // (1024**2)} MB")
            info_lines.append(f"Available: {mem.available // (1024**2)} MB")
            info_lines.append(f"Used: {mem.percent}%")
        except:
            info_lines.append("Memory info: Unavailable")
        
        # CPU info
        info_lines.append("\n=== CPU ===\n")
        try:
            info_lines.append(f"Cores: {psutil.cpu_count()}")
            info_lines.append(f"Usage: {psutil.cpu_percent()}%")
        except:
            info_lines.append("CPU info: Unavailable")
        
        self.info_label.text = "\n".join(info_lines)
        self.update_status("System info refreshed")
    
    def get_hostname(self, ip):
        """Get hostname for IP"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"
    
    def get_service_name(self, port):
        """Get service name for port"""
        services = {
            20: "FTP Data",
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            8080: "HTTP Proxy"
        }
        return services.get(port, "Unknown")
    
    def update_scan_results(self, results):
        """Update scan results progressively"""
        self.results_label.text = "Scanning...\n\n" + "\n".join(results)
    
    def finalize_scan(self, results):
        """Finalize scan results"""
        if results:
            self.results_label.text = f"✅ Scan Complete!\n\nFound {len([r for r in results if '✅' in r])} online devices\n\n" + "\n".join(results)
        else:
            self.results_label.text = "❌ No devices found or scan failed"
        self.update_status("Scan completed")
    
    def update_port_scan(self, port, all_ports):
        """Update port scan progress"""
        progress = all_ports.index(port) + 1
        total = len(all_ports)
        self.port_results_label.text = f"Scanning... {progress}/{total}\nPort: {port}"
    
    def show_port_results(self, results):
        """Show port scan results"""
        open_count = len([r for r in results if "OPEN" in r])
        self.port_results_label.text = f"Port Scan Complete!\n\nOpen ports: {open_count}\n\n" + "\n".join(results)
        self.update_status("Port scan completed")
    
    def show_error(self, error):
        """Show error message"""
        self.results_label.text = f"❌ Error:\n{error}"
        self.update_status("Scan failed")
    
    def show_port_error(self, error):
        """Show port scan error"""
        self.port_results_label.text = f"❌ Port scan error:\n{error}"
        self.update_status("Port scan failed")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.text = f"Status: {message}"
    
    def toggle_theme(self, instance):
        """Toggle dark/light theme"""
        if Window.clearcolor == [0.1, 0.1, 0.15, 1]:
            Window.clearcolor = (0.95, 0.95, 0.95, 1)
            self.status_label.color = (0.1, 0.1, 0.1, 1)
            self.update_status("Light theme activated")
        else:
            Window.clearcolor = (0.1, 0.1, 0.15, 1)
            self.status_label.color = (0.7, 0.7, 0.7, 1)
            self.update_status("Dark theme activated")
    
    def clear_logs(self, instance):
        """Clear all logs"""
        self.results_label.text = ""
        self.port_results_label.text = ""
        self.update_status("Logs cleared")
    
    def export_results(self, instance):
        """Export scan results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}.txt"
            
            data = f"""
            Network Security Scan Results
            =============================
            Time: {datetime.now()}
            
            Network Scan:
            {self.results_label.text}
            
            Port Scan:
            {self.port_results_label.text}
            
            System Info:
            {self.info_label.text}
            """
            
            # On Android, we can't save directly, so show content
            self.results_label.text = f"📋 Export ready:\n\nCopy this content:\n\n{data[:500]}..."
            self.update_status("Results ready for copy")
            
        except Exception as e:
            self.update_status(f"Export failed: {str(e)}")

if __name__ == '__main__':
    NetworkScannerApp().run()