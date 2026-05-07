
import gradio as gr
import numpy as np
from PIL import Image
import tensorflow as tf
import json
from datetime import datetime

model = tf.keras.models.load_model("best_model.keras")
with open("class_names.json", "r") as f:
    class_indices = json.load(f)
classes = [k for k, v in sorted(class_indices.items(), key=lambda x: x[1])]

recycling_tips = {
    "cardboard": ("Recyclable",     "Flatten and place in the recycling bin.",   "recyclable"),
    "glass":     ("Recyclable",     "Rinse and place in the glass bin.",         "recyclable"),
    "metal":     ("Recyclable",     "Clean and place in the metal bin.",         "recyclable"),
    "paper":     ("Recyclable",     "Keep dry and place in the paper bin.",      "recyclable"),
    "plastic":   ("Check Label",    "Check recycling number on packaging.",      "caution"),
    "trash":     ("Non-Recyclable", "Place in the general waste bin.",           "nonrecyclable"),
}
co2_savings   = {"cardboard":0.9,"glass":0.3,"metal":1.5,"paper":0.7,"plastic":0.4,"trash":0.0}
impact_scores = {"cardboard":8,"glass":7,"metal":9,"paper":8,"plastic":5,"trash":0}
fun_facts = {
    "cardboard": "Recycling 1 ton of cardboard saves 17 trees!",
    "glass":     "Glass takes ~1 million years to decompose in landfill.",
    "metal":     "Aluminium can be recycled infinitely without quality loss!",
    "paper":     "Recycling 1 ton of paper saves ~26,000 litres of water.",
    "plastic":   "Plastic takes up to 500 years to decompose.",
    "trash":     "Proper waste management can cut greenhouse gases by 20%.",
}
bin_locations = {
    "recyclable":    [{"name":"Blue Recycling Bin - Sector 1","lat":28.4744,"lon":77.5040},
                      {"name":"Blue Recycling Bin - Sector 4","lat":28.4780,"lon":77.5060},
                      {"name":"Community Recycle Center","lat":28.4720,"lon":77.5020}],
    "caution":       [{"name":"Plastic Collection Point","lat":28.4744,"lon":77.5040},
                      {"name":"Plastic Recycling Drop-off","lat":28.4760,"lon":77.5070}],
    "nonrecyclable": [{"name":"General Waste Bin - Block A","lat":28.4730,"lon":77.5030},
                      {"name":"General Waste Bin - Block C","lat":28.4755,"lon":77.5055},
                      {"name":"Municipal Waste Collection","lat":28.4710,"lon":77.5010}],
}

history_log = []
classify_count = [0]
total_co2 = [0.0]

def get_history_html():
    if not history_log:
        return "<p style='color:#333;text-align:center;padding:20px;'>No classifications yet.</p>"
    rows = ""
    for i, e in enumerate(reversed(history_log[-10:])):
        bg = "#f0f0f0" if i % 2 == 0 else "#ffffff"
        rows += f"<tr style='background:{bg};'><td style='padding:10px;color:#111;text-align:center;'>{e['time']}</td><td style='padding:10px;color:#111;text-align:center;font-weight:bold;'>{e['item']}</td><td style='padding:10px;color:#111;text-align:center;'>{e['confidence']}</td><td style='padding:10px;color:#111;text-align:center;'>{e['emoji']} {e['status']}</td><td style='padding:10px;color:#111;text-align:center;'>{e['co2']} kg</td></tr>"
    return f"<div style='font-family:Arial;padding:10px;'><h3 style='color:#2E7D32;'>Classification History (Last 10)</h3><table style='width:100%;border-collapse:collapse;border:1px solid #ddd;'><thead><tr style='background:#2E7D32;color:white;'><th style='padding:10px;'>Time</th><th style='padding:10px;'>Item</th><th style='padding:10px;'>Confidence</th><th style='padding:10px;'>Status</th><th style='padding:10px;'>CO2 Saved</th></tr></thead><tbody>{rows}</tbody></table><p style='color:#333;margin-top:10px;'>Total CO2 saved: <strong>{total_co2[0]:.2f} kg</strong></p></div>"

def get_map_html(category):
    locs = bin_locations.get(category, bin_locations["nonrecyclable"])
    label = "Recycling Bins" if category=="recyclable" else "Plastic Drop-off Points" if category=="caution" else "General Waste Bins"
    color = "#1B5E20" if category=="recyclable" else "#E65100" if category=="caution" else "#B71C1C"
    markers = "".join([f"<div style='background:white;border:2px solid #4CAF50;border-radius:10px;padding:12px;margin:8px 0;'><strong style='color:#111;'>📍 {l['name']}</strong><br><span style='color:#555;font-size:0.85em;'>Lat: {l['lat']}, Lon: {l['lon']}</span></div>" for l in locs])
    return f"<div style='font-family:Arial;padding:10px;'><h3 style='color:{color};'>Nearest {label}</h3><p style='color:#555;'>Galgotias University, Greater Noida area</p>{markers}<div style='margin-top:12px;padding:12px;background:#E3F2FD;border-radius:10px;'><strong style='color:#111;'>Tip:</strong> <span style='color:#333;'>Search "{label} near me" on Google Maps!</span></div></div>"

def predict_waste(image):
    if image is None:
        return {}, "<p style='color:#333;'>Please upload an image or use webcam.</p>", get_history_html()
    img = Image.fromarray(image).resize((224, 224))
    arr = np.expand_dims(np.array(img) / 255.0, axis=0)
    preds = model.predict(arr, verbose=0)
    confs = {classes[i]: float(preds[0][i]) for i in range(len(classes))}
    top = max(confs, key=confs.get)
    conf_pct = confs[top] * 100
    status, tip, cat = recycling_tips.get(top, ("Unknown","Unknown","nonrecyclable"))
    co2 = co2_savings.get(top, 0)
    score = impact_scores.get(top, 0)
    fact = fun_facts.get(top, "")
    classify_count[0] += 1
    total_co2[0] += co2
    if cat == "recyclable": bg,border,badge,emoji = "#E8F5E9","#4CAF50","#1B5E20","🟢"
    elif cat == "caution":  bg,border,badge,emoji = "#FFF3E0","#FF9800","#E65100","🟡"
    else:                   bg,border,badge,emoji = "#FFEBEE","#F44336","#B71C1C","🔴"
    score_bar = "🟩" * score + "⬜" * (10 - score)
    history_log.append({"time":datetime.now().strftime("%H:%M:%S"),"item":top.upper(),"confidence":f"{conf_pct:.1f}%","status":status,"emoji":emoji,"co2":co2})
    html = f"<div style='background:{bg};border:3px solid {border};border-radius:16px;padding:20px;font-family:Arial;color:#111;'><div style='background:{badge};color:white;border-radius:10px;padding:10px 18px;font-size:1.3em;font-weight:bold;margin-bottom:14px;display:inline-block;'>{emoji} {status} — {top.upper()}</div><p><strong>Confidence:</strong> {conf_pct:.1f}%</p><p><strong>Tip:</strong> {tip}</p><p><strong>CO2 Saved:</strong> {co2} kg</p><hr style='border:1px solid {border};'><p><strong>Impact Score:</strong> {score}/10 {score_bar}</p><p style='color:#444;font-size:0.9em;'>💡 {fact}</p><hr style='border:1px solid {border};'><p style='color:#444;font-size:0.85em;'>Total classified: <strong>{classify_count[0]}</strong> | Total CO2 saved: <strong>{total_co2[0]:.2f} kg</strong></p></div>"
    return confs, html, get_history_html()

with gr.Blocks(theme=gr.themes.Soft(), title="Waste Classifier") as demo:
    gr.HTML("<div style='text-align:center;padding:22px;background:linear-gradient(135deg,#2E7D32,#1565C0);border-radius:16px;color:white;margin-bottom:20px;'><h1>🌍 Automated Waste Classification System</h1><p>Galgotias University | Khushi Dubey &amp; Suhani</p></div>")
    gr.HTML("<div style='display:flex;gap:12px;justify-content:center;margin-bottom:16px;'><span style='background:#E8F5E9;border:2px solid #4CAF50;border-radius:8px;padding:6px 14px;color:#111;'>🟢 Recyclable</span><span style='background:#FFF3E0;border:2px solid #FF9800;border-radius:8px;padding:6px 14px;color:#111;'>🟡 Check Label</span><span style='background:#FFEBEE;border:2px solid #F44336;border-radius:8px;padding:6px 14px;color:#111;'>🔴 Non-Recyclable</span></div>")
    with gr.Tabs():
        with gr.Tab("📁 Upload Image"):
            with gr.Row():
                with gr.Column():
                    up_img = gr.Image(label="Upload Waste Image", type="numpy")
                    up_btn = gr.Button("🔍 Classify!", variant="primary", size="lg")
                with gr.Column():
                    up_lbl = gr.Label(num_top_classes=6, label="Confidence Scores")
                    up_res = gr.HTML()
        with gr.Tab("📷 Webcam"):
            with gr.Row():
                with gr.Column():
                    wc_img = gr.Image(label="Point camera at waste item", sources=["webcam"], type="numpy", mirror_webcam=False, interactive=True)
                    wc_btn = gr.Button("🔍 Classify Snapshot!", variant="primary", size="lg")
                with gr.Column():
                    wc_lbl = gr.Label(num_top_classes=6, label="Confidence Scores")
                    wc_res = gr.HTML()
        with gr.Tab("📋 History"):
            hist = gr.HTML(value="<p style='color:#333;text-align:center;padding:20px;'>No classifications yet.</p>")
        with gr.Tab("🗺️ Nearest Bin"):
            bin_radio = gr.Radio(choices=["recyclable","caution","nonrecyclable"], value="recyclable", label="Select waste category")
            map_out = gr.HTML(value=get_map_html("recyclable"))
            bin_radio.change(fn=get_map_html, inputs=bin_radio, outputs=map_out)
    up_btn.click(predict_waste, inputs=up_img, outputs=[up_lbl, up_res, hist])
    wc_btn.click(predict_waste, inputs=wc_img, outputs=[wc_lbl, wc_res, hist])

demo.launch()
