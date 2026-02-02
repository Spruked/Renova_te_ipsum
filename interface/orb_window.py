import sys
import math
import os
from collections import deque
from PySide6.QtWidgets import (QApplication, QWidget, QGraphicsDropShadowEffect, 
                                QLabel, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import (Qt, QTimer, QPoint, Signal, QObject, QThread, 
                           QRect, QPointF)
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont, QCursor, QRadialGradient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orb_controller import SF_ORB_Controller

class CognitiveWorker(QObject):
    """Background thread for cognitive processing"""
    pulse_signal = Signal(dict)
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.running = True
        self.last_pos = QPoint(0, 0)
        self.last_time = 0
        
    def process_cursor(self, pos):
        if not self.running:
            return
            
        # Calculate velocity
        current_time = os.times().system
        dx = pos.x() - self.last_pos.x()
        dy = pos.y() - self.last_pos.y()
        dt = current_time - self.last_time if self.last_time > 0 else 0.016
        velocity = math.sqrt(dx*dx + dy*dy) / max(dt, 0.001)
        
        self.last_pos = pos
        self.last_time = current_time
        
        stimulus = {
            "type": "cursor_movement",
            "coordinates": [pos.x(), pos.y()],
            "velocity": min(velocity, 50.0),  # Cap velocity
            "intent": "navigation"
        }
        
        thought = self.controller.cognitively_emerge(stimulus)
        if thought:
            self.pulse_signal.emit(thought.pulse())

class FloatingOrb(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = SF_ORB_Controller()
        
        # Window setup
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFixedSize(120, 120)
        
        # Position
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.center() - self.rect().center())
        
        # State
        self.current_pos = self.pos()
        self.target_pos = self.pos()
        self.true_target = self.pos()  # For lerp calculations
        
        # Cognitive state
        self.cognitive_mode = "GUARD"
        self.glow_intensity = 0.5
        self.predictive_offset = QPoint(0, 0)
        self.necessity_vector = (0.0, 0.0)
        self.jump_active = False
        self.field_density = 0
        self.edge_cutter_active = False
        self.purge_phase = 0
        self.proc_time_ms = 0.0
        self.latency_samples = deque(maxlen=40)
        
        # Mode colors
        self.colors = {
            "GUARD": QColor(0, 128, 128),        # Teal
            "GUARD-HABIT": QColor(64, 160, 100), # Teal-Green
            "HABIT": QColor(255, 191, 0),        # Amber
            "INTUITION-JUMP": QColor(143, 0, 255) # Violet
        }
        self.current_color = self.colors["GUARD"]
        self.pulse_phase = 0
        
        # Setup worker thread
        self.worker_thread = QThread()
        self.worker = CognitiveWorker(self.controller)
        self.worker.moveToThread(self.worker_thread)
        self.worker.pulse_signal.connect(self.handle_pulse)
        
        # Timers
        self.track_timer = QTimer()
        self.track_timer.timeout.connect(self.track_cursor)
        self.track_timer.start(16)  # 60fps tracking
        
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(16)
        
        self.cognitive_timer = QTimer()
        self.cognitive_timer.timeout.connect(self.process_cognition)
        self.cognitive_timer.start(100)  # 10Hz cognition
        
        self.last_cursor = QCursor.pos()
        self.setup_ui()
        self.worker_thread.start()
        
    def setup_ui(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(self.current_color)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        self.hud = QLabel(self)
        self.hud.setGeometry(10, 45, 100, 30)
        self.hud.setStyleSheet("""
            color: white; 
            background: rgba(0,0,0,0.7); 
            border-radius: 15px; 
            padding: 5px;
            font-weight: bold;
        """)
        self.hud.setFont(QFont("Consolas", 9))
        self.hud.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hud.setText("GUARD")
        self.hud.hide()
        
    def track_cursor(self):
        self.last_cursor = QCursor.pos()
        
    def process_cognition(self):
        if self.worker_thread.isRunning():
            self.worker.process_cursor(self.last_cursor)
            
    def handle_pulse(self, pulse):
        mode = pulse.get("cognitive_mode", "GUARD")
        self.cognitive_mode = mode
        self.glow_intensity = pulse.get("glow_intensity", 0.5)
        self.field_density = pulse.get("field_density", 0)
        self.proc_time_ms = pulse.get("proc_time_ms", 0.0)
        self.edge_cutter_active = pulse.get("edge_cutter_active", False)
        
        # Handle Humean prediction
        if mode in ["HABIT", "GUARD-HABIT"]:
            pred = pulse.get("predictive_intent", {})
            if pred and "target" in pred:
                quad = pred["target"]
                offsets = {"NW": (-60, -60), "NE": (60, -60), 
                          "SW": (-60, 60), "SE": (60, 60)}
                off = offsets.get(quad, (0, 0))
                self.predictive_offset = QPoint(off[0], off[1])
            else:
                self.predictive_offset = QPoint(0, 0)
        else:
            self.predictive_offset = QPoint(0, 0)
            
        # Handle Spinozan jump
        if mode == "INTUITION-JUMP":
            jump_vec = pulse.get("jump_vector", [0, 0])
            if jump_vec and abs(jump_vec[0]) > 0.01:
                screen = QApplication.primaryScreen().geometry()
                center = screen.center()
                # Map normalized vector to screen space (200px range)
                target_x = center.x() + jump_vec[0] * 200 - 60
                target_y = center.y() + jump_vec[1] * 200 - 60
                self.true_target = QPoint(int(target_x), int(target_y))
                self.jump_active = True
            self.pulse_phase = 0  # Reset pulse for shockwave
        else:
            self.jump_active = False
            # Normal following with prediction
            self.true_target = self.last_cursor + self.predictive_offset - QPoint(60, 60)
            
        self.hud.setText(f"{mode}\n{self.glow_intensity:.2f}")
        self.update()
        
    def update_animation(self):
        # Color lerp
        target_color = self.colors.get(self.cognitive_mode, self.colors["GUARD"])
        r = self.current_color.red() + (target_color.red() - self.current_color.red()) * 0.1
        g = self.current_color.green() + (target_color.green() - self.current_color.green()) * 0.1
        b = self.current_color.blue() + (target_color.blue() - self.current_color.blue()) * 0.1
        self.current_color = QColor(int(r), int(g), int(b))
        
        # Shadow/glow
        self.shadow.setColor(self.current_color)
        base_blur = 20
        blur = base_blur + (60 * self.glow_intensity)
        self.shadow.setBlurRadius(int(blur))
        
        # Position handling
        if self.jump_active:
            # Spinozan snap (instant)
            self.current_pos = self.true_target
        else:
            # Lerp based on mode
            if self.cognitive_mode == "HABIT":
                speed = 0.15  # Faster, eager
            else:
                speed = 0.08  # Slower, deliberate
                
            new_x = self.current_pos.x() + (self.true_target.x() - self.current_pos.x()) * speed
            new_y = self.current_pos.y() + (self.true_target.y() - self.current_pos.y()) * speed
            self.current_pos = QPoint(int(new_x), int(new_y))
            
        self.move(self.current_pos)
        
        # Pulse phase for intuition shockwave
        if self.cognitive_mode == "INTUITION-JUMP":
            self.pulse_phase = (self.pulse_phase + 2) % 30
        elif self.edge_cutter_active:
            # Purge shockwave runs longer and independent of jump
            self.purge_phase = min(self.purge_phase + 3, 120)
        else:
            self.purge_phase = max(self.purge_phase - 4, 0)

        # Track latency samples for sparkline
        self.latency_samples.append(float(self.proc_time_ms))
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Purge shockwave effect when edge-cutter is active
        if self.purge_phase > 0:
            alpha = max(0, 180 - self.purge_phase)
            radius = 60 + self.purge_phase * 1.5
            shock_color = QColor(238, 130, 238, alpha)
            painter.setBrush(QBrush(QColor(238, 130, 238, max(10, alpha // 3))))
            painter.setPen(QPen(shock_color, 3))
            painter.drawEllipse(int(60 - radius/2), int(60 - radius/2), int(radius), int(radius))

        # Shockwave effect for Intuition-Jump
        if self.cognitive_mode == "INTUITION-JUMP" and self.pulse_phase > 0:
            alpha = int(255 * (1 - self.pulse_phase / 30))
            pulse_color = QColor(
                self.current_color.red(),
                self.current_color.green(),
                self.current_color.blue(),
                alpha
            )
            painter.setBrush(QBrush(pulse_color))
            painter.setPen(Qt.PenStyle.NoPen)
            radius = 60 + self.pulse_phase * 3
            painter.drawEllipse(
                int(60 - radius/2), 
                int(60 - radius/2), 
                radius, radius
            )
        
        # Main orb with gradient
        gradient = QRadialGradient(60, 60, 50)
        gradient.setColorAt(0, self.current_color.lighter(150))
        gradient.setColorAt(0.7, self.current_color)
        gradient.setColorAt(1, self.current_color.darker(120))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(10, 10, 100, 100)
        
        # Inner core
        painter.setBrush(QBrush(QColor(255, 255, 255, 100)))
        painter.drawEllipse(30, 30, 60, 60)
        
        # Density ring (maps 0-1000 to arc) and hysteresis band (650-800)
        density_ratio = min(max(self.field_density / 1000.0, 0.0), 1.0)
        painter.setPen(QPen(QColor(0, 200, 200), 4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(6, 6, 108, 108, 90 * 16, -int(density_ratio * 360 * 16))

        trigger, release = 800, 650
        band_start = release / 1000.0 * 360.0
        band_span = (trigger - release) / 1000.0 * 360.0
        painter.setPen(QPen(QColor(120, 220, 120, 180), 3))
        painter.drawArc(10, 10, 100, 100, int((90 - band_start) * 16), -int(band_span * 16))

        # Latency sparkline (bottom area)
        if self.latency_samples:
            samples = list(self.latency_samples)
            max_latency = max(max(samples), 1.0)
            w = 80
            h = 30
            x0 = 20
            y0 = 90
            pts = []
            for i, val in enumerate(samples):
                x = x0 + (i / max(1, len(samples) - 1)) * w
                y = y0 + h - min(h, (val / max_latency) * h)
                pts.append(QPointF(x, y))
            painter.setPen(QPen(QColor(255, 90, 90), 2))
            painter.drawPolyline(pts)

        # Mode indicator ring
        if self.cognitive_mode == "HABIT":
            painter.setPen(QPen(self.colors["HABIT"], 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(5, 5, 110, 110)
            
    def enterEvent(self, event):
        self.hud.show()
        
    def leaveEvent(self, event):
        self.hud.hide()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            self.current_pos = self.pos()
            self.true_target = self.pos()
            event.accept()
            
    def closeEvent(self, event):
        self.worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    orb = FloatingOrb()
    orb.show()
    
    print("SF-ORB Interface Active")
    print("Visual Modes:")
    print("  Teal (Guard)     = Deductive validation, rigid following")
    print("  Amber (Habit)    = Inductive prediction, leads cursor")  
    print("  Violet (Jump)    = Spinozan necessity, instant snap + shockwave")
    print("\nDrag to move | Hover for HUD | Watch it learn...")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()import sys
import math
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsDropShadowEffect, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, Signal, QObject, QThread
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont, QCursor
import numpy as np

# Import controller (adjust path if needed)
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orb_controller import SF_ORB_Controller

class CognitiveWorker(QObject):
    """Background thread for cognitive processing to keep UI smooth"""
    pulse_signal = Signal(dict)
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.running = True
        
    def process_cursor(self, pos, velocity):
        if not self.running:
            return
            
        stimulus = {
            "type": "cursor_movement",
            "coordinates": [pos.x(), pos.y()],
            "velocity": velocity,
            "intent": "navigation"
        }
        
        thought = self.controller.cognitively_emerge(stimulus)
        if thought:
            self.pulse_signal.emit(thought.pulse())

class FloatingOrb(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = SF_ORB_Controller()
        
        # Window setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.WindowStaysOnTopHint | 
                           Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(120, 120)
        
        # Position (center screen initially)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.center() - self.rect().center())
        
        # Orb state
        self.current_pos = self.pos()
        self.target_pos = self.pos()
        self.cursor_history = []
        self.last_cursor_pos = QCursor.pos()
        self.velocity = 0.0
        
        # Cognitive state
        self.cognitive_mode = "GUARD"
        self.glow_intensity = 0.5
        self.predictive_offset = QPoint(0, 0)
        self.necessity_vector = (0.0, 0.0)
        
        # Color mapping for Triad C modes
        self.mode_colors = {
            "GUARD": QColor(0, 128, 128),        # Teal - Deductive validation
            "GUARD-HABIT": QColor(64, 160, 128), # Teal-Green transition
            "HABIT": QColor(255, 191, 0),        # Amber - Humean vivacity
            "INTUITION-JUMP": QColor(143, 0, 255), # Violet - Spinozan necessity
        }
        self.current_color = self.mode_colors["GUARD"]
        self.target_color = self.current_color
        
        # Animation properties
        self.lerp_speed = 0.08  # Base speed
        self.pulse_radius = 40
        self.pulse_expansion = 0
        
        # Setup cognitive worker thread
        self.worker_thread = QThread()
        self.worker = CognitiveWorker(self.controller)
        self.worker.moveToThread(self.worker_thread)
        self.worker.pulse_signal.connect(self.handle_cognitive_pulse)
        
        # Timer for cursor tracking
        self.track_timer = QTimer()
        self.track_timer.timeout.connect(self.track_cursor)
        self.track_timer.start(16)  # ~60fps
        
        # Timer for animation
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(16)
        
        # Timer for cognitive processing (throttled)
        self.cognitive_timer = QTimer()
        self.cognitive_timer.timeout.connect(self.process_cognition)
        self.cognitive_timer.start(100)  # 10Hz cognitive updates
        
        # Setup UI elements
        self.setup_ui()
        
        # Start worker
        self.worker_thread.start()
        
    def setup_ui(self):
        """Setup shadow effects and HUD"""
        # Glow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(self.current_color)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        # HUD Label (for debugging/mode display)
        self.hud = QLabel(self)
        self.hud.setGeometry(10, 10, 100, 20)
        self.hud.setStyleSheet("color: white; background: rgba(0,0,0,0.5); border-radius: 10px; padding: 2px;")
        self.hud.setFont(QFont("Consolas", 8))
        self.hud.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hud.setText("GUARD")
        self.hud.hide()  # Hidden by default, show on hover
        
    def track_cursor(self):
        """Track cursor movement and calculate velocity"""
        current = QCursor.pos()
        dx = current.x() - self.last_cursor_pos.x()
        dy = current.y() - self.last_cursor_pos.y()
        self.velocity = math.sqrt(dx*dx + dy*dy)
        self.cursor_history.append((current, self.velocity))
        if len(self.cursor_history) > 10:
            self.cursor_history.pop(0)
        self.last_cursor_pos = current
        
    def process_cognition(self):
        """Emit cognitive processing to worker thread"""
        if not self.worker_thread.isRunning():
            return
        # Calculate average velocity
        vel = self.velocity if self.velocity > 0 else 0.1
        self.worker.process_cursor(self.last_cursor_pos, vel)
        
    def handle_cognitive_pulse(self, pulse):
        """Receive cognitive pulse from controller"""
        self.cognitive_mode = pulse.get("cognitive_mode", "GUARD")
        self.glow_intensity = pulse.get("glow_intensity", 0.5)
        
        # Handle predictive intent (Humean)
        if "predictive_intent" in pulse and self.cognitive_mode in ["HABIT", "GUARD-HABIT"]:
            pred = pulse["predictive_intent"]
            if pred and "target" in pred:
                # Convert quadrant prediction to offset
                quad_offsets = {
                    "NW": (-50, -50), "NE": (50, -50),
                    "SW": (-50, 50), "SE": (50, 50)
                }
                offset = quad_offsets.get(pred["target"], (0, 0))
                self.predictive_offset = QPoint(offset[0], offset[1])
                # Increase lerp speed for habit (eager following)
                self.lerp_speed = 0.15
            else:
                self.predictive_offset = QPoint(0, 0)
                
        # Handle necessity vector (Spinozan)
        if self.cognitive_mode == "INTUITION-JUMP":
            jump_vec = pulse.get("jump_vector", [0, 0])
            if jump_vec:
                screen = QApplication.primaryScreen().geometry()
                # Map normalized vector to screen coordinates
                target_x = screen.center().x() + jump_vec[0] * 200
                target_y = screen.center().y() + jump_vec[1] * 200
                self.necessity_vector = (target_x, target_y)
                # Instant snap (Spinozan necessity - no lerp)
                self.target_pos = QPoint(int(target_x), int(target_y)) - QPoint(60, 60)
                self.lerp_speed = 1.0  # Instant
        else:
            # Normal cursor following with optional prediction
            cursor_pos = self.last_cursor_pos
            target = cursor_pos + self.predictive_offset - QPoint(60, 60)
            self.target_pos = target
            
        # Update target color based on mode
        self.target_color = self.mode_colors.get(self.cognitive_mode, self.mode_colors["GUARD"])
        
        # Update HUD
        self.hud.setText(f"{self.cognitive_mode} | {self.glow_intensity:.2f}")
        
    def update_animation(self):
        """Lerp animation and visual effects"""
        # Color interpolation
        r = self.current_color.red() + (self.target_color.red() - self.current_color.red()) * 0.1
        g = self.current_color.green() + (self.target_color.green() - self.current_color.green()) * 0.1
        b = self.current_color.blue() + (self.target_color.blue() - self.current_color.blue()) * 0.1
        self.current_color = QColor(int(r), int(g), int(b))
        
        # Update shadow color
        self.shadow.setColor(self.current_color)
        
        # Glow intensity affects blur radius
        base_blur = 20
        max_blur = 60
        current_blur = base_blur + (max_blur - base_blur) * self.glow_intensity
        self.shadow.setBlurRadius(int(current_blur))
        
        # Position lerp (except for Jump mode which snaps)
        if self.cognitive_mode != "INTUITION-JUMP":
            new_x = self.current_pos.x() + (self.target_pos.x() - self.current_pos.x()) * self.lerp_speed
            new_y = self.current_pos.y() + (self.target_pos.y() - self.current_pos.y()) * self.lerp_speed
            self.current_pos = QPoint(int(new_x), int(new_y))
            self.move(self.current_pos)
            
        # Pulse effect for Intuition mode
        if self.cognitive_mode == "INTUITION-JUMP":
            self.pulse_expansion = (self.pulse_expansion + 2) % 20
        else:
            self.pulse_expansion = 0
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw outer pulse for Intuition mode
        if self.cognitive_mode == "INTUITION-JUMP" and self.pulse_expansion > 0:
            pulse_alpha = 255 - (self.pulse_expansion * 10)
            pulse_color = QColor(self.current_color.red(), 
                               self.current_color.green(), 
                               self.current_color.blue(), 
                               max(0, pulse_alpha))
            painter.setBrush(QBrush(pulse_color))
            painter.setPen(Qt.PenStyle.NoPen)
            pulse_radius = 60 + self.pulse_expansion
            painter.drawEllipse(int(60 - pulse_radius/2), int(60 - pulse_radius/2), 
                               pulse_radius, pulse_radius)
        
        # Draw main orb
        gradient = QBrush(self.current_color)
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(10, 10, 100, 100)
        
        # Inner highlight
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.drawEllipse(25, 25, 70, 70)
        
    def enterEvent(self, event):
        """Show HUD on hover"""
        self.hud.show()
        
    def leaveEvent(self, event):
        """Hide HUD"""
        self.hud.hide()
        
    def mousePressEvent(self, event):
        """Allow dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Drag handling"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            self.current_pos = self.pos()
            event.accept()
            
    def closeEvent(self, event):
        """Cleanup threads"""
        self.worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    orb = FloatingOrb()
    orb.show()
    print("SF-ORB Interface Active")
    print("Click and drag to move the orb")
    print("Hover to see cognitive mode HUD")
    print("Watch the color change:")
    print("  Teal = Guard (Deductive validation)")
    print("  Amber = Habit (Inductive prediction)")
    print("  Violet = Intuition (Spinozan jump)")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
