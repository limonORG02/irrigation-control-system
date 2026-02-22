import sys
import os
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
from tkinter import Tk, Frame, Listbox, Button, Label, Entry, END, messagebox, simpledialog, Scrollbar, RIGHT, Y

# Ensure src on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.zone_service import get_zones
from services.sensor_service import list_sensors, add_sensor, remove_sensor, add_measurement, get_sensors_by_zone
from services.irrigation_service import get_norms
from analysis.decision_engine import analyze_zone
from services.gas_service import record_gas_event, list_unacknowledged, acknowledge


def setup_logging():
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'app.log')
    logger = logging.getLogger('irrigation')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3, encoding='utf-8')
    fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(fmt)
    if not logger.handlers:
        logger.addHandler(handler)
    # JSON line logger
    json_file = os.path.join(logs_dir, 'app.jsonl')
    try:
        jf = open(json_file, 'a', encoding='utf-8')
        # simple JSON line writer wrapper
        class JsonWriter:
            def write(self, msg):
                try:
                    jf.write(msg + '\n')
                    jf.flush()
                except Exception:
                    pass
            def flush(self):
                try:
                    jf.flush()
                except Exception:
                    pass
        # attach a small handler that writes JSON dicts
        class JsonHandler(logging.Handler):
            def emit(self, record):
                try:
                    entry = {
                        'time': self.formatTime(record),
                        'level': record.levelname,
                        'message': record.getMessage()
                    }
                    jf.write(__import__('json').dumps(entry, ensure_ascii=False) + '\n')
                    jf.flush()
                except Exception:
                    pass

        jh = JsonHandler()
        jh.setLevel(logging.INFO)
        logger.addHandler(jh)
    except Exception:
        pass
    return logger


class App:
    def __init__(self, root):
        self.logger = setup_logging()
        self.root = root
        root.title('Irrigation Control GUI')

        left = Frame(root)
        left.pack(side='left', padx=10, pady=10)

        center = Frame(root)
        center.pack(side='left', padx=10, pady=10)

        right = Frame(root)
        right.pack(side='right', padx=10, pady=10)

        Label(left, text='Zones').pack()
        self.zones_list = Listbox(left, width=30)
        self.zones_list.pack()
        self.zones = get_zones()
        for zid, ptype in self.zones:
            self.zones_list.insert(END, f"{zid}: {ptype}")

        Label(center, text='Sensors (selected zone)').pack()
        self.sensors_list = Listbox(center, width=40)
        self.sensors_list.pack()

        btn_frame = Frame(center)
        btn_frame.pack(pady=5)
        Button(btn_frame, text='Add Sensor', command=self.on_add_sensor).pack(side='left')
        Button(btn_frame, text='Remove Sensor', command=self.on_remove_sensor).pack(side='left')
        Button(btn_frame, text='Add Measurement', command=self.on_add_measurement).pack(side='left')

        notif_frame = Frame(right)
        notif_frame.pack(fill='x', padx=10, pady=5)
        Button(notif_frame, text='Simulate Gas Alarm', command=self.on_gas_alarm).pack(side='top', pady=2)
        Button(notif_frame, text='Check Now', command=self.check_all_zones).pack(side='top', pady=2)

        Label(right, text='Gas Events (unacknowledged)').pack()
        events_frame = Frame(right)
        events_frame.pack()
        self.events_list = Listbox(events_frame, width=50, height=10)
        self.events_list.pack(side='left')
        scrollbar = Scrollbar(events_frame, orient='vertical')
        scrollbar.pack(side=RIGHT, fill=Y)
        self.events_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.events_list.yview)

        ack_frame = Frame(right)
        ack_frame.pack(pady=5)
        Button(ack_frame, text='Acknowledge Selected', command=self.on_ack_selected).pack()

        Button(right, text='All Events (history)', command=self.open_events_history).pack(pady=6)

        self.zones_list.bind('<<ListboxSelect>>', lambda e: self.refresh_sensors())

        self.running = True
        t = threading.Thread(target=self.background_check, daemon=True)
        t.start()

        self.refresh_sensors()
        self.refresh_events()

    def get_selected_zone(self):
        sel = self.zones_list.curselection()
        if not sel:
            return None
        idx = sel[0]
        return self.zones[idx][0]

    def refresh_sensors(self):
        self.sensors_list.delete(0, END)
        zid = self.get_selected_zone()
        if zid is None:
            return
        rows = list_sensors(zone_id=zid)
        for r in rows:
            sid, zone_id, stype, active = r
            self.sensors_list.insert(END, f"{sid} | {stype} | {'active' if active else 'inactive'}")

    def refresh_events(self):
        self.events_list.delete(0, END)
        events = list_unacknowledged()
        for eid, zid, level, ts in events:
            self.events_list.insert(END, f"{eid} | zone {zid} | level {level} | {ts}")

    def on_add_sensor(self):
        zid = self.get_selected_zone()
        if zid is None:
            messagebox.showinfo('Info', 'Select a zone first')
            return
        stype = simpledialog.askstring('Sensor type', 'Enter sensor type (moisture/gas):', initialvalue='moisture')
        if not stype:
            return
        sid = add_sensor(zid, stype)
        self.logger.info(f'Added sensor {sid} type={stype} zone={zid}')
        self.refresh_sensors()

    def on_remove_sensor(self):
        sel = self.sensors_list.curselection()
        if not sel:
            messagebox.showinfo('Info', 'Select a sensor to remove')
            return
        line = self.sensors_list.get(sel[0])
        sid = int(line.split('|')[0].strip())
        if messagebox.askyesno('Confirm', f'Remove sensor {sid}?'):
            remove_sensor(sid)
            self.logger.info(f'Removed sensor {sid}')
            self.refresh_sensors()

    def on_add_measurement(self):
        sel = self.sensors_list.curselection()
        if not sel:
            messagebox.showinfo('Info', 'Select a sensor')
            return
        line = self.sensors_list.get(sel[0])
        sid = int(line.split('|')[0].strip())
        val = simpledialog.askfloat('Measurement', 'Enter moisture value (percent):', minvalue=0, maxvalue=100)
        if val is None:
            return
        add_measurement(sid, val)
        self.logger.info(f'Added measurement sensor={sid} value={val}')
        messagebox.showinfo('OK', 'Measurement added')

    def on_gas_alarm(self):
        zid = self.get_selected_zone()
        if zid is None:
            messagebox.showinfo('Info', 'Select a zone to simulate gas alarm')
            return
        level = simpledialog.askfloat('Gas level', 'Enter gas level value:', minvalue=0)
        if level is None:
            return
        eid = record_gas_event(zid, level)
        self.logger.warning(f'Gas alarm recorded id={eid} zone={zid} level={level}')
        messagebox.showwarning('Gas Alarm', f'Gas alarm recorded (id={eid}). Acknowledge in notifications list.')
        self.refresh_events()

    def on_ack_selected(self):
        sel = self.events_list.curselection()
        if not sel:
            messagebox.showinfo('Info', 'Select an event to acknowledge')
            return
        line = self.events_list.get(sel[0])
        eid = int(line.split('|')[0].strip())
        acknowledge(eid)
        self.logger.info(f'Acknowledged gas event {eid}')
        self.refresh_events()

    def open_events_history(self):
        # open a Toplevel window with filters and full event list
        w = Tk() if False else None
        from tkinter import Toplevel, StringVar, OptionMenu
        top = Toplevel(self.root)
        top.title('Events History')
        filter_frame = Frame(top)
        filter_frame.pack(padx=10, pady=6)
        Label(filter_frame, text='Zone ID (empty=all):').grid(row=0, column=0)
        zone_entry = Entry(filter_frame)
        zone_entry.grid(row=0, column=1)
        Label(filter_frame, text='Acknowledged:').grid(row=1, column=0)
        var = StringVar(filter_frame)
        var.set('all')
        OptionMenu(filter_frame, var, 'all', '0', '1').grid(row=1, column=1)

        list_frame = Frame(top)
        list_frame.pack(padx=10, pady=6)
        events_list = Listbox(list_frame, width=90, height=15)
        events_list.pack(side='left')
        sb = Scrollbar(list_frame, orient='vertical')
        sb.pack(side=RIGHT, fill=Y)
        events_list.config(yscrollcommand=sb.set)
        sb.config(command=events_list.yview)

        def load():
            zid_text = zone_entry.get().strip()
            zid = int(zid_text) if zid_text else None
            ack = None
            if var.get() == '0':
                ack = 0
            elif var.get() == '1':
                ack = 1
            events_list.delete(0, END)
            events = list_events(zone_id=zid, acknowledged=ack)
            for eid, zone, level, ts, acknowledged in events:
                events_list.insert(END, f"{eid} | zone {zone} | level {level} | {ts} | ack={acknowledged}")

        def ack_selected():
            sel = events_list.curselection()
            if not sel:
                messagebox.showinfo('Info', 'Select an event')
                return
            line = events_list.get(sel[0])
            eid = int(line.split('|')[0].strip())
            acknowledge(eid)
            self.logger.info(f'Acknowledged event from history {eid}')
            load()

        btns = Frame(top)
        btns.pack(pady=6)
        Button(btns, text='Load', command=load).pack(side='left', padx=6)
        Button(btns, text='Acknowledge Selected', command=ack_selected).pack(side='left', padx=6)


    def check_all_zones(self):
        for zid, ptype in self.zones:
            data = []
            rows = list_sensors(zone_id=zid)
            for r in rows:
                sid, _, stype, active = r
                if stype == 'moisture' and active:
                    data = get_sensors_by_zone(zid)
                    break
            norms = get_norms(ptype)
            if norms:
                status = analyze_zone(zid, ptype, data, norms)
                if status == 'Требуется полив':
                    messagebox.showinfo('Irrigation', f'Zone {zid} ({ptype}) requires watering')
                    self.logger.info(f'Zone {zid} requires watering')

    def background_check(self):
        while self.running:
            # refresh events list periodically
            try:
                self.refresh_events()
            except Exception:
                pass
            time.sleep(10)

    def stop(self):
        self.running = False


def main():
    root = Tk()
    app = App(root)
    try:
        root.mainloop()
    finally:
        app.stop()


if __name__ == '__main__':
    main()
