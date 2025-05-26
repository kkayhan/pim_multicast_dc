import json, time

ROUTE_PATH = ("network-instance vrflite_multicast static-routes "
              "route 10.55.0.1/32 admin-state")

def event_handler_main(event):
    d = event if isinstance(event, dict) else json.loads(event)
    paths      = d.get("paths", [])
    opts       = d.get("options", {})
    st         = d.get("persistent-data", {})

    cnt_now    = int(paths[0].get("value", 0)) if paths else 0
    interval_s = int(opts.get("interval_seconds", 1))      # used only for 1-shot delay
    thresh_pps = int(opts.get("threshold_pps", 0))

    cnt_prev   = int(st.get("prev_cnt", cnt_now))
    ts_prev    = int(st.get("prev_ts", int(time.time()*1000)))
    armed      = bool(st.get("reinvoke_armed", False))

    ts_now     = int(time.time()*1000)
    actions    = []

    # first run → just set baseline
    if "prev_cnt" not in st:
        return json.dumps({
            "actions": [],
            "persistent-data": {
                "prev_cnt": cnt_now,
                "prev_ts":  ts_now,
                "reinvoke_armed": False
            }
        })

    # PPS calculation (integer math)
    delta_ms   = ts_now - ts_prev
    pps        = (cnt_now - cnt_prev) * 1000 // delta_ms if delta_ms > 0 else 0

    if pps > thresh_pps:
        actions.append({"set-cfg-path": {
            "path": ROUTE_PATH, "value": "enable", "always-execute": False}})
        armed = False                                    # cancel any pending idle check

    else:
        if not armed:                                   # start 1-shot confirmation
            actions.append({"reinvoke-with-delay": interval_s * 1000})
            armed = True
        else:                                           # confirmation run → disable
            actions.append({"set-cfg-path": {
                "path": ROUTE_PATH, "value": "disable", "always-execute": False}})
            armed = False                               # done; no further reinvoke

    return json.dumps({
        "actions": actions,
        "persistent-data": {
            "prev_cnt": cnt_now,
            "prev_ts":  ts_now,
            "reinvoke_armed": armed
        }
    })
