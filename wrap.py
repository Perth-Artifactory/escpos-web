from flask import jsonify
import json
import requests
import io

with open("config.json", "r") as f:
    config = json.load(f)
    
# Utility functions

def format_text(text: str) -> list:
    """Accepts a string and formats it so that each line is no longer than 48 characters"""
    lines = []
    line = ""
    for word in text.split(" "):
        if len(line) + len(word) > 48:
            lines.append(line.strip())
            line = ""
        line += word + " "
    lines.append(line)
    return lines

def resize_image(data: str, width: int, t: str = "local"):
    """take a filename and resize it to a specific width and autoscaled height. Returns the PIL object"""
    
    from PIL import Image
    if t == "local":
        img = Image.open(data)
    elif t == "url":
        img = Image.open(io.BytesIO(data))
    
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), Image.ANTIALIAS)
    return img
    
# Printer functions

def text(local_printer, data):
    if "text" not in data:
        return jsonify({"error": "No text specified"})
    
    if "size" not in data:
        data["size"] = 2
        
    if "newline" not in data:
        data["newline"] = True
    if data["newline"]:
        data["text"] += "\n"
        
    print(f'Printing "{data["text"]}" at size {data["size"]}')
    try:
        local_printer.set(smooth=True,
                        width=data["size"],
                        height=data["size"])
        
        for line in format_text(data["text"])[:-1]:
            local_printer.text(line + "\n")
        local_printer.text(format_text(data["text"])[-1])
        
        return jsonify({"success": True})
    except:
        return jsonify({"error": "Failed to print text"})

def cut(local_printer, data):
    print("Cutting")
    try:
        local_printer.cut()
        return jsonify({"success": True})
    except:
        return jsonify({"error": "Failed to cut"})

def image(local_printer, data):
    if "image" not in data:
        return jsonify({"error": "No image specified"})
    print(f'Printing image {data["image"]}')
    
    # check if data["image"] is a url
    if data["image"].startswith("http"):
        r = requests.get(data["image"])
        if r.status_code != 200:
            return jsonify({"error": f'Failed to download image from {data["image"]}'})
        try:
            local_printer.image(img_source=resize_image(data = r.content,
                                                        width = 576,
                                                        t="url"),
                                impl="bitImageRaster")
            return jsonify({"success": True})
        except:
            return jsonify({"error": f'Failed to print image from {data["image"]}'})
        
    
    elif data["image"] in config["images"]:
        print(f'Image {data["image"]} found in config')
        try:
            local_printer.image(img_source=resize_image(data = './img/' + data["image"],
                                                        width = 576,
                                                        t = "local"),
                                impl="bitImageRaster")
            return jsonify({"success": True})
        except:
            return jsonify({"error": f'Failed to print image {data["image"]}'})
        
    else:
        return jsonify({"error": f'Image {data["image"]} not found'})
    
def qr(local_printer, data):
    if "text" not in data:
        return jsonify({"error": "No text specified"})
    print(f'Printing QR code for "{data["text"]}"')
    try:
        local_printer.qr(data["text"], size=8)
    except:
        return jsonify({"error": "Failed to print QR code"})
    return jsonify({"success": True})

