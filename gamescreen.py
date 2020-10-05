import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import numpy as np

class GameScreen:
    def capture():
        window = Gdk.get_default_root_window()
        screen = window.get_screen()
        w=screen.get_active_window()
        p = Gdk.pixbuf_get_from_window(w,*w.get_geometry())     
        w,h,c,r=(p.get_width(), p.get_height(), p.get_n_channels(), p.get_rowstride())
        assert p.get_colorspace() == GdkPixbuf.Colorspace.RGB
        assert p.get_bits_per_sample() == 8
        if  p.get_has_alpha():
            assert c == 4
        else:
            assert c == 3
        assert r >= w * c
        a=np.frombuffer(p.get_pixels(),dtype=np.uint8)
        if a.shape[0] == w*c*h:
            return a.reshape( (h, w, c) )
        else:
            b=np.zeros((h,w*c),'uint8')
            for j in range(h):
                b[j,:]=a[r*j:r*j+w*c]
            return b.reshape( (h, w, c) )
    def geometry():
        window = Gdk.get_default_root_window()
        screen = window.get_screen()
        w=screen.get_active_window()
        return w.get_geometry()